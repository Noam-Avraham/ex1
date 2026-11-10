import os, random, subprocess, sys

# Run this from inside the ex1/ directory itself, e.g.:
#   cd ex1
#   python3 ziptest/mytests/gen_and_check.py [seed]
#
# It builds the lexer with `make`, then generates 100 fresh random/edge-case
# test programs, runs LEXER on each, and compares against an independently
# computed expected output (not derived from the lexer itself).

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 42
random.seed(SEED)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTDIR = os.path.join(SCRIPT_DIR, "test100")
os.makedirs(TESTDIR, exist_ok=True)

EX1 = os.getcwd()          # expected to be the ex1/ directory
JAVA = "java"               # assumed to be on PATH
CP_SEP = os.pathsep         # ':' on Linux/nova, ';' on Windows

OPS = [
    ("+", "PLUS"), ("-", "MINUS"), ("*", "TIMES"), ("/", "DIVIDE"),
    ("=", "EQ"), ("<", "LT"), (">", "GT"), ("and", "AND"), ("or", "OR"),
    ("(", "LPAREN"), (")", "RPAREN"), ("[", "LBRACK"), ("]", "RBRACK"),
    ("{", "LBRACE"), ("}", "RBRACE"), (",", "COMMA"), (".", "DOT"),
    (";", "SEMICOLON"), (":=", "ASSIGN"),
]

KEYWORDS = [
    ("array", "ARRAY"), ("class", "CLASS"), ("extends", "EXTENDS"),
    ("new", "NEW"), ("nil", "NIL"), ("if", "IF"), ("else", "ELSE"),
    ("while", "WHILE"), ("return", "RETURN"), ("int", "TYPE_INT"),
    ("string", "TYPE_STRING"), ("void", "TYPE_VOID"),
]

IDS = ["x", "y", "foo", "bar", "numPts", "myVar", "abc", "Z", "Q9",
       "longIdentifierName", "a1b2c3", "Counter", "tmp", "Node", "list1",
       "p", "i", "j", "head", "tail"]

INTS = ["0", "1", "5", "7", "9", "10", "42", "100", "255", "999",
        "1000", "12345", "31999", "32767", "2024"]

STRINGS = ['""', '"Dan"', '"Hello"', '"World"', '"abc"', '"Compiler"', '"a"']

VALID_COMMENTS = [
    "// a legal line comment\n",
    "// nums 1 2 3 (ok) [yes]\n",
    "/* a block comment */",
    "/**/",
    "/* a ** b *** c */",
    "/* multi\nline\ncomment */",
]

ERROR_ATOMS = [
    "00", "007", "0100",
    "32768", "40000", "99999", "50123",
    "100000", "123456",
    '"Da3n"', '"Hi!"', '"A_B"',
    "// bad $ comment\n", "// bad @ thing\n",
    "/* bad $ comment */", "/* bad @ thing */",
    ":",
    "@", "#", "~",
]
UNCLOSED_ERROR_ATOMS = ['"Dan', "/* unclosed"]  # must be placed last, no suffix


def all_atoms():
    atoms = []
    for lit, name in OPS:
        atoms.append((lit, name, None))
    for lit, name in KEYWORDS:
        atoms.append((lit, name, None))
    for v in IDS:
        atoms.append((v, "ID", v))
    for v in INTS:
        atoms.append((v, "INT", str(int(v))))
    for v in STRINGS:
        atoms.append((v, "STRING", v))
    return atoms


ATOMS = all_atoms()


def advance(line, col, text):
    for ch in text:
        if ch == "\n":
            line += 1
            col = 1
        else:
            col += 1
    return line, col


def random_ws():
    choices = [" ", "  ", "\t", "\n", " \n", "\n\n", "\t "]
    return random.choice(choices)


def build_valid_program(n_atoms, trace=None):
    text = ""
    line, col = 1, 1
    expected = []
    prev_lit = None
    for idx in range(n_atoms):
        # separator before this atom (always at least one char, except very first atom)
        sep = ""
        if idx > 0 or random.random() < 0.3:
            # never place a comment (always starts with '/') directly after a
            # token ending in '/' (DIVIDE) -- that would accidentally form
            # "//" or "/*" and get swallowed into a much larger comment than
            # intended. Plain whitespace never starts with '/', so it's always safe.
            can_use_comment = not (prev_lit is not None and prev_lit.endswith("/"))
            if can_use_comment and random.random() < 0.25:
                sep = random.choice(VALID_COMMENTS)
            else:
                sep = random_ws()
            text += sep
            line, col = advance(line, col, sep)

        lit, name, value = random.choice(ATOMS)
        start_line, start_col = line, col
        text += lit
        line, col = advance(line, col, lit)
        expected.append((name, value, start_line, start_col))
        if trace is not None:
            trace.append((repr(sep), repr(lit), name))
        prev_lit = lit

    return text, expected


def format_expected(tokens):
    lines = []
    for name, value, l, c in tokens:
        if value is not None:
            lines.append(f"{name}({value})[{l},{c}]")
        else:
            lines.append(f"{name}[{l},{c}]")
    return "\n".join(lines)


def build_error_program(error_atom, unclosed=False, prefix_atoms=0):
    text = ""
    line, col = 1, 1
    for _ in range(prefix_atoms):
        sep = random_ws()
        text += sep
        line, col = advance(line, col, sep)
        lit, name, value = random.choice(ATOMS)
        text += lit
        line, col = advance(line, col, lit)

    sep = random_ws()
    text += sep
    line, col = advance(line, col, sep)
    text += error_atom

    if not unclosed:
        # optional valid suffix, should not matter
        if random.random() < 0.5:
            sep2 = random_ws()
            text += sep2
            lit, name, value = random.choice(ATOMS)
            text += lit
    return text


def write(path, content):
    with open(path, "w", newline="\n", encoding="ascii") as f:
        f.write(content)


def main():
    print(f"Building lexer with 'make' in {EX1} ...")
    r = subprocess.run(["make"], cwd=EX1)
    if r.returncode != 0:
        print("BUILD FAILED - aborting tests")
        sys.exit(1)

    tests = []  # (name, input_text, expected_text_or_ERROR)

    # 60 valid random programs, varying sizes
    for i in range(60):
        n = random.randint(4, 18)
        text, expected = build_valid_program(n)
        tests.append((f"valid_{i+1:03d}", text, format_expected(expected)))

    # 40 error programs cycling through error categories
    for i in range(32):
        atom = ERROR_ATOMS[i % len(ERROR_ATOMS)]
        text = build_error_program(atom, unclosed=False, prefix_atoms=random.randint(0, 4))
        tests.append((f"error_{i+1:03d}", text, "ERROR"))

    for i in range(8):
        atom = UNCLOSED_ERROR_ATOMS[i % len(UNCLOSED_ERROR_ATOMS)]
        text = build_error_program(atom, unclosed=True, prefix_atoms=random.randint(0, 4))
        tests.append((f"error_unclosed_{i+1:03d}", text, "ERROR"))

    assert len(tests) == 100, len(tests)

    for name, text, expected in tests:
        write(os.path.join(TESTDIR, name + ".txt"), text)

    passed = 0
    failed = []
    classpath = f"LEXER{CP_SEP}external_jars/java-cup-11b-runtime.jar"
    for name, text, expected in tests:
        inp = os.path.join(TESTDIR, name + ".txt")
        out = os.path.join(TESTDIR, name + ".out.txt")
        subprocess.run([JAVA, "-cp", classpath, "Main", inp, out], cwd=EX1, check=True)
        with open(out, "r", encoding="utf-8", errors="replace") as f:
            actual = f.read().replace("\r\n", "\n").strip("\n")
        exp_norm = expected.replace("\r\n", "\n").strip("\n")
        if actual == exp_norm:
            passed += 1
        else:
            failed.append((name, text, exp_norm, actual))

    print(f"PASSED: {passed}/100")
    if failed:
        print(f"FAILED: {len(failed)}")
        for name, text, exp, act in failed:
            print("=" * 60)
            print("TEST:", name)
            print("INPUT:")
            print(repr(text))
            print("EXPECTED:")
            print(exp)
            print("ACTUAL:")
            print(act)
        sys.exit(1)


if __name__ == "__main__":
    main()
