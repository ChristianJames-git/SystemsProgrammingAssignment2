import re
from functools import *

"""
Single Programmer Affidavit
I the undersigned promise that the attached assignment is my own work. While I was 
free to discuss ideas with others, the work contained is my own. I recognize that 
should this not be the case, I will be subject to penalties as outlined in the course 
syllabus. 
Christian James - 823672623
CS530 Section 01 (T/TH)
"""

"""
Assignment 2 - 
A LL(1) recursive descent parser for validating simple expressions.
# Task A:
You would need to first write the grammar rules (non-terminal) in EBNF 
according to the token patterns and grammar rules specified in the prompt,
put the rules in a separate PDF file, see prompt. 
(Refer to the EBNF example in Figure 5.15)
# Task B:
You would then write the recursive descent parsing procedures for the 
validation parsing according to the rules from Task A. 
(Refer to the parsing algorithm in Figure 5.17)
It implements one parsing procedure for each one of the 
non-terminals (grammar rules), starting from the top of the parse tree, 
then drilling into lower hierachical levels.
The procedures work together to handle all combinations of the grammar 
rules, and they automatically handle the nested compositions of terms 
with multi-level priority brackets. 
----------------------------------------------------------------------------
Usage (Refer to the prompt for more examples - both positive and negative cases)
r = recDecsent('7 - 17')
print(r.validate()) # will print True as '7 - 17' is a valid expression
r = recDecsent('7 - ')
print(r.validate()) # will print False as '7 - ' is an invalid expression
"""


class recDescent:
    # IMPORTANT:
    # You MUST NOT change the signatures of
    # the constructor, lex(self) and validate(self)
    # Otherwise, autograding tests will FAIL
    # constructor to initialize and set class level variables
    def __init__(self, expr=""):
        # string to be parsed
        self.expr = expr
        # tokens from lexer tokenization of the expression
        self.tokens = []
        # variable to track current token index
        self.token = 0

    # lexer - tokenize the expression into a list of tokens
    # the tokens are stored in an list which can be accessed by self.tokens
    # do not edit any piece of code in this function
    def lex(self):
        self.tokens = re.findall("[-\(\)=]|[!<>]=|[<>]|\w+|[^ +]\W+", self.expr)
        # transform tokens to lower case, and filter out possible spaces in the tokens
        self.tokens = list(filter((lambda x: len(x)), list(map((lambda x: x.strip().lower()), self.tokens))))

    # parser - determine if the input expression is valid or not

    # validate() function will return True if the expression is valid, False otherwise
    # do not change the method signature as this function will be called by the autograder

    def validate(self):
        # Using the tokens from lex() tokenization,
        # your validate would first call lex() to first tokenize the expression
        self.lex()
        # then call the top level parsing procedure and go from there
        return self.exp()
    # parsing procedures corresponding to the grammar rules - follow Figure 5.17

    # <exp> ::= <term> { <op> <term> }
    def exp(self):
        found = False
        # store if currently in the <exp> of '( <exp> )'
        inparen = False
        if self.gettoken(self.token - 1) == '(':
            inparen = True
        # handles '<term>'
        if self.term():
            found = True
            # handles '{ ; <op> <term> }'
            while self.op():
                if not self.term():
                    found = False
            # if not in '( <exp> )' and still have tokens remaining, return False as not all tokens fit the rules
            if self.arrayleft(self.token) != 0 and not inparen:
                found = False
        return found

    # <op> ::= and | or | nand | xor | xnor
    def op(self):
        ops = {'and', 'or', 'nand', 'xor', 'xnor'}
        if self.gettoken(self.token) in ops:  # check for current token in ops
            self.token += 1  # next token after op
            return True
        return False

    # <term> ::= <relop> int | int - int | ( <exp> )
    def term(self):
        found = False
        # handles '<relop> int'
        if self.relop():
            if self.gettoken(self.token).isdigit():
                self.token += 1  # next token after 'int'
                found = True
        # handles 'int - int'
        elif self.gettoken(self.token).isdigit():
            # check if token after 'int' is '-' and if the token after '-' is 'int'
            if self.gettoken(self.token + 1) == '-' and self.gettoken(self.token + 2).isdigit():
                self.token += 3  # skip to token after 'int - int'
                found = True
        # handles '( <exp> )'
        elif self.gettoken(self.token) == '(':
            self.token += 1  # next token after '('
            if self.exp():
                if self.gettoken(self.token) == ')':
                    self.token += 1  # next token after ')'
                    found = True
        return found

    # <relop> ::= < | > | <= | >= | = | != | not
    def relop(self):
        relops = {'<', '>', '<=', '>=', '=', '!=', 'not'}
        if self.gettoken(self.token) in relops:  # check for current token in relops
            self.token += 1  # next token after relop
            return True
        return False

    # helper function that returns the token at the given index
    # this prevents index out of bounds errors
    # returns 'invalid' if the index is out of bounds as that string will fail all checks
    def gettoken(self, index):
        if self.arrayleft(index) < 1 or index < 0:
            return 'invalid'
        return self.tokens[index]

    # helper function to check # of remaining tokens including the current one
    def arrayleft(self, token):
        return len(self.tokens) - token
