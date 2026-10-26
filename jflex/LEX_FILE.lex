/***************************/
/* FILE NAME: LEX_FILE.lex */
/***************************/

/*************/
/* USER CODE */
/*************/

import java_cup.runtime.*;

/******************************/
/* DOLLAR DOLLAR - DON'T TOUCH! */
/******************************/

%%

/************************************/
/* OPTIONS AND DECLARATIONS SECTION */
/************************************/
   
/*****************************************************/ 
/* Lexer is the name of the class JFlex will create. */
/* The code will be written to the file Lexer.java.  */
/*****************************************************/ 
%class Lexer

/********************************************************************/
/* The current line number can be accessed with the variable yyline */
/* and the current column number with the variable yycolumn.        */
/********************************************************************/
%line
%column

/*******************************************************************************/
/* Note that this has to be the EXACT same name of the class the CUP generates */
/*******************************************************************************/
%cupsym TokenNames

/******************************************************************/
/* CUP compatibility mode interfaces with a CUP generated parser. */
/******************************************************************/
%cup

/****************/
/* DECLARATIONS */
/****************/
/*****************************************************************************/   
/* Code between %{ and %}, both of which must be at the beginning of a line, */
/* will be copied verbatim (letter to letter) into the Lexer class code.     */
/* Here you declare member variables and functions that are used inside the  */
/* scanner actions.                                                          */  
/*****************************************************************************/   
%{
	/*********************************************************************************/
	/* Create a new java_cup.runtime.Symbol with information about the current token */
	/*********************************************************************************/
	private Symbol symbol(int type)               {return new Symbol(type, yyline, yycolumn);}
	private Symbol symbol(int type, Object value) {return new Symbol(type, yyline, yycolumn, value);}

	/*******************************************/
	/* Enable line number extraction from main */
	/*******************************************/
	public int getLine() { return yyline + 1; } 

	/**********************************************/
	/* Enable token position extraction from main */
	/**********************************************/
	public int getTokenStartPosition() { return yycolumn + 1; } 
%}

/***********************/
/* MACRO DECLARATIONS */
/***********************/
LineTerminator	= \r|\n|\r\n
WhiteSpace		= {LineTerminator} | [ \t]
INTEGER			= 0 | [1-9][0-9]*
LETTER          = [a-z]|[A-Z]
DIGIT           = [0-9]
ZEROINTAGER     = 0[0-9]+
BIGINTEGER      = [4-9]{DIGIT}{4} | 3[3-9]{DIGIT}{3} | 32[8-9]{DIGIT}{2} | 327[7-9]{DIGIT} | 3276[8-9] | [1-9]{DIGIT}{4}{DIGIT}+
ID  			= {LETTER}({LETTER}|{DIGIT})*
STRING 			= \"{LETTER}*\"
BAD_STRING      = \"[^\r\n\"]*\"

COMMENT_LEGAL_CHAR     = {LETTER} | {DIGIT} | [ \t] | [()\[\]{}?!+\-*/.;]
COMMENT_ONE            = "//" {COMMENT_LEGAL_CHAR}* {LineTerminator}
BAD_COMMENT_ONE        = "//" [^\r\n]* {LineTerminator}

NO_STAR                = {LETTER} | {DIGIT} | [ \t\r\n] | [()\[\]{}?!/.;\-+]
NO_STAR_NO_SLASH       = {LETTER} | {DIGIT} | [ \t\r\n] | [()\[\]{}?!.;\-+]
COMMENT_TWO            = "/*" ( {NO_STAR} | "*"+ {NO_STAR_NO_SLASH} )* "*"+ "/"
ANY_NO_STAR            = [^*]
ANY_NO_STAR_NO_SLASH    = [^*/]
BAD_COMMENT_TWO        = "/*" ( {ANY_NO_STAR} | "*"+ {ANY_NO_STAR_NO_SLASH} )* "*"+ "/"
/******************************/
/* DOLLAR DOLLAR - DON'T TOUCH! */
/******************************/

%%

/************************************************************/
/* LEXER matches regular expressions to actions (Java code) */
/************************************************************/

/**************************************************************/
/* YYINITIAL is the state at which the lexer begins scanning. */
/* So these regular expressions will only be matched if the   */
/* scanner is in the start state YYINITIAL.                   */
/**************************************************************/

<YYINITIAL> {
{WhiteSpace}		{/* skip */}
"+"					{ return symbol(TokenNames.PLUS);}
"-"					{ return symbol(TokenNames.MINUS);}
"*" 				{ return symbol(TokenNames.TIMES);}
"/"					{ return symbol(TokenNames.DIVIDE);}
"="					{ return symbol(TokenNames.EQ);}
"<"					{ return symbol(TokenNames.LT);}
">"					{ return symbol(TokenNames.GT);}
"and"				{ return symbol(TokenNames.AND);}
"or" 				{ return symbol(TokenNames.OR);}
"("					{ return symbol(TokenNames.LPAREN);}
")"					{ return symbol(TokenNames.RPAREN);}
"["					{ return symbol(TokenNames.LBRACK);}
"]"					{ return symbol(TokenNames.RBRACK);}
"{"					{ return symbol(TokenNames.LBRACE);}
"}"					{ return symbol(TokenNames.RBRACE);}
","					{ return symbol(TokenNames.COMMA);}
"."					{ return symbol(TokenNames.DOT);}
";"					{ return symbol(TokenNames.SEMICOLON);}
":="				{ return symbol(TokenNames.ASSIGN);}
"array"				{ return symbol(TokenNames.ARRAY);}
"class"				{ return symbol(TokenNames.CLASS);}
"extends"			{ return symbol(TokenNames.EXTENDS);}
"new"				{ return symbol(TokenNames.NEW);}
"nil"				{ return symbol(TokenNames.NIL);}
"if"				{ return symbol(TokenNames.IF);}
"else"				{ return symbol(TokenNames.ELSE);}
"while"				{ return symbol(TokenNames.WHILE);}
"return"			{ return symbol(TokenNames.RETURN);}
"int"				{ return symbol(TokenNames.TYPE_INT);}
"string"			{ return symbol(TokenNames.TYPE_STRING);}
"void"				{ return symbol(TokenNames.TYPE_VOID);}
{ZEROINTAGER}		{ return symbol(TokenNames.ERROR);}
{BIGINTEGER}		{ return symbol(TokenNames.ERROR);}
{INTEGER}			{ return symbol(TokenNames.INT, Integer.valueOf(yytext()));}
{ID}				{ return symbol(TokenNames.ID,     yytext());} 
{STRING} 			{ return symbol(TokenNames.STRING,yytext());}
{BAD_STRING}        { return symbol(TokenNames.ERROR);} 
{COMMENT_ONE}		{/* skip */}
{BAD_COMMENT_ONE}	{ return symbol(TokenNames.ERROR);}
{COMMENT_TWO}       {/* skip */}
{BAD_COMMENT_TWO}   { return symbol(TokenNames.ERROR);}
[^]                 { return symbol(TokenNames.ERROR);}
<<EOF>>				{ return symbol(TokenNames.EOF);}

}
