from Consts import Consts
from Token import Token
from Error import Error

class Lexer:
    def __init__(self, source_code):
        self.code = source_code
        self.current = None
        self.indice, self.coluna, self.linha = -1, -1, 0
        self.__advance()

    def __advance(self):
        self.__advanceCalc(self.current)
        self.current = self.code[self.indice] if self.indice < len(self.code) else None

    def __advanceCalc(self, _char=None):
        self.indice += 1
        self.coluna += 1
        if _char == '\n':
                self.linha += 1
                self.coluna = 0
        return self

    def peek(self):
        peekIndex = self.indice + 1
        if peekIndex < len(self.code):
            return self.code[peekIndex]
        return '\0'
#atualizado para receber novos simbolos
    def makeTokens(self):
        tokens = []
        while self.current is not None:
            if self.current in ' \t':
                self.__advance()

            elif self.current in Consts.DIGITOS:
                tokens.append(self.__makeNumber())

            elif self.current == '"':
                tokens.append(self.__MakeString())

            # Operadores compostos devem vir antes dos simples
            elif self.current == '=' and self.peek() == '=':
                self.__advance()
                self.__advance()
                tokens.append(Token(Consts.EQEQ))

            elif self.current == '!' and self.peek() == '=':
                self.__advance()
                self.__advance()
                tokens.append(Token(Consts.NE))

            elif self.current == '<' and self.peek() == '=':
                self.__advance()
                self.__advance()
                tokens.append(Token(Consts.LE))

            elif self.current == '>' and self.peek() == '=':
                self.__advance()
                self.__advance()
                tokens.append(Token(Consts.GE))

            # Operadores simples
            elif self.current == Consts.EQ:
                tokens.append(Token(Consts.EQ))
                self.__advance()

            elif self.current == '<':
                self.__advance()
                tokens.append(Token(Consts.LT))

            elif self.current == '>':
                self.__advance()
                tokens.append(Token(Consts.GT))

            elif self.current == Consts.PLUS:
                tokens.append(Token(Consts.PLUS))
                self.__advance()

            elif self.current == Consts.MINUS:
                tokens.append(Token(Consts.MINUS))
                self.__advance()

            elif self.current == Consts.MUL:
                tokens.append(Token(Consts.MUL))
                self.__advance()

            elif self.current == Consts.DIV:
                tokens.append(Token(Consts.DIV))
                self.__advance()

            elif self.current == Consts.POW:
                tokens.append(Token(Consts.POW))
                self.__advance()

            elif self.current == Consts.LPAR:
                tokens.append(Token(Consts.LPAR))
                self.__advance()

            elif self.current == Consts.RPAR:
                tokens.append(Token(Consts.RPAR))
                self.__advance()

            elif self.current == Consts.LSQUARE:
                tokens.append(Token(Consts.LSQUARE))
                self.__advance()

            elif self.current == Consts.RSQUARE:
                tokens.append(Token(Consts.RSQUARE))
                self.__advance()

            elif self.current == Consts.COMMA:
                tokens.append(Token(Consts.COMMA))
                self.__advance()

            elif self.current in Consts.LETRAS + Consts.UNDER:
                tokens.append(self.__makeId())

            else:
                return [], Error(f"{Error.lexerError}: lex-symbol '{self.current}' fail!")

        tokens.append(Token(Consts.EOF))
        return tokens, None

    def __makeNumber(self):
        strNumber = ''
        dotCount = 0
        while self.current != None and self.current in Consts.DIGITOS + '.':
            if self.current == '.':
                if dotCount == 1: break
                dotCount += 1
                strNumber += '.'
            else:
                strNumber += self.current
            self.__advance()

        if dotCount == 0:
            return Token(Consts.INT, int(strNumber))
        else:
            return Token(Consts.FLOAT, float(strNumber))
    
    def __MakeString(self):
        stri = ""
        bypass = False
        self.__advance()
        specialChars = {'n':'\n', 't': '\t'}
        while (self.current != None and (self.current != '"' or bypass)):
            if (bypass):
                c = specialChars.get(self.current, self.current)
                stri += c
                bypass = False
            else:
                if (self.current == '\\'):
                    bypass = True
                else:
                    stri += self.current
            self.__advance()

        self.__advance()
        return Token(Consts.STRING, stri)

    ##############################
    #atualizado para receber as constantes de TRUE e FALSE
    def __makeId(self):
        lexema = ''
        while self.current != None and self.current in Consts.LETRAS_DIGITOS + Consts.UNDER:
            lexema += self.current
            self.__advance()
        if lexema in Consts.KEYS:
            if lexema == Consts.TRUE or lexema == Consts.FALSE:
                tokType = Consts.BOOL
            else:
                tokType = Consts.KEY # Isso já cobre FOR, IN, RANGE
        else:
            tokType = Consts.ID
        return Token(tokType, lexema)
    ##############################
