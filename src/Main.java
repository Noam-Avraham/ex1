import java.io.*;
import java.io.PrintWriter;

import java_cup.runtime.Symbol;
   
public class Main
{
	static public void main(String argv[])
	{
		Lexer l;
		Symbol s;
		FileReader fileReader;
		PrintWriter fileWriter;
		String inputFileName = argv[0];
		String outputFileName = argv[1];
		
		try
		{
			/********************************/
			/* [1] Initialize a file reader */
			/********************************/
			fileReader = new FileReader(inputFileName);

			/********************************/
			/* [2] Initialize a file writer */
			/********************************/
			fileWriter = new PrintWriter(outputFileName);
			
			/******************************/
			/* [3] Initialize a new lexer */
			/******************************/
			l = new Lexer(fileReader);

			/***********************/
			/* [4] Read next token */
			/***********************/
			s = l.next_token();

			/********************************/
			/* [5] Main reading tokens loop */
			/********************************/
			StringBuilder output = new StringBuilder();
			boolean error = false;
			while (s.sym != TokenNames.EOF)
			{
				/************************/
				/* [6] Print to console */
				/************************/
				if (s.sym == TokenNames.ERROR) {
					error=true;
					break;
				}
				output.append(tokenName(s.sym));
				if (hasValue(s.sym))
					output.append("(" + s.value + ")");
				output.append("[");
				output.append(l.getLine());
				output.append(",");
				output.append(l.getTokenStartPosition());
				output.append("]\n");

				/***********************/
				/* [8] Read next token */
				/***********************/
				s = l.next_token();
			}
			
			/******************************/
			/* [9] Close lexer input file */
			/******************************/
			l.yyclose();
			if (error)
			{
				fileWriter.print("ERROR");
			}
			else
			{
				String result = output.toString();
				if (result.endsWith("\n"))
					result = result.substring(0, result.length() - 1);
				fileWriter.print(result);
			}

			/**************************/
			/* [10] Close output file */
			/**************************/
			fileWriter.close();
    	}
			     
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}
	//return true if token sym has a value (INT, ID, STRING)
	static boolean hasValue(int s)
	{
		if (s == TokenNames.INT || s == TokenNames.ID || s == TokenNames.STRING)
			return true;
		else
			return false;
	}
	//return name for token sym (except for EOF and ERROR)
	 static String tokenName(int sym)
          {		
                  switch (sym)
				  {

                          case TokenNames.PLUS:         return "PLUS";
                          case TokenNames.MINUS:        return "MINUS";
                          case TokenNames.TIMES:        return "TIMES";
                          case TokenNames.DIVIDE:       return "DIVIDE";
                          case TokenNames.EQ:           return "EQ";
                          case TokenNames.LT:           return "LT";
                          case TokenNames.GT:           return "GT";
                          case TokenNames.AND:          return "AND";
                          case TokenNames.OR:           return "OR";
                          case TokenNames.LPAREN:       return "LPAREN";
                          case TokenNames.RPAREN:       return "RPAREN";
                          case TokenNames.LBRACK:       return "LBRACK";
                          case TokenNames.RBRACK:       return "RBRACK";
                          case TokenNames.LBRACE:       return "LBRACE";
                          case TokenNames.RBRACE:       return "RBRACE";
                          case TokenNames.COMMA:        return "COMMA";
                          case TokenNames.DOT:          return "DOT";
                          case TokenNames.SEMICOLON:    return "SEMICOLON";
                          case TokenNames.ASSIGN:       return "ASSIGN";
                          case TokenNames.ARRAY:        return "ARRAY";
                          case TokenNames.CLASS:        return "CLASS";
                          case TokenNames.EXTENDS:      return "EXTENDS";
                          case TokenNames.NEW:          return "NEW";
                          case TokenNames.NIL:          return "NIL";
                          case TokenNames.IF:           return "IF";
                          case TokenNames.ELSE:         return "ELSE";
                          case TokenNames.WHILE:        return "WHILE";
                          case TokenNames.RETURN:       return "RETURN";
                          case TokenNames.TYPE_INT:     return "TYPE_INT";
                          case TokenNames.TYPE_STRING:  return "TYPE_STRING";
                          case TokenNames.TYPE_VOID:    return "TYPE_VOID";
                          case TokenNames.INT:          return "INT";
                          case TokenNames.ID:           return "ID";
                          case TokenNames.STRING:       return "STRING";
                          default:                      return "UNKNOWN";
                  }
          }
}


