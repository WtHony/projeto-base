from Consts import Consts
from SemanticVisitor import *

class Grammar:
    def __init__(self, parser):
        self.parser = parser
    def Rule(self):
        return self.GetParserManager().fail(f"{Error.parserError}: Implementar suas regras de producao (Heranca de Grammar)!")
    
    def CurrentToken(self):
        return self.parser.CurrentTok()
    
    def NextToken(self):
        return self.parser.NextTok()
    
    def GetParserManager(self):
        return self.parser.Manager()

    @staticmethod
    def StartSymbol(parser): # Start Symbol S from Grammar G(V, T, S, P)
        resultado = Exp(parser).Rule()
        if parser.CurrentTok().type != Consts.EOF: return resultado.fail(f"{Error.parserError}: Erro sintatico")
        return resultado


"""
nome da classe exp trocado para ExpAritmetica para melhor leitura do codigo
"""
class ExpAritmetica(Grammar): # A variable from Grammar G
    def Rule(self):
        ast = self.GetParserManager()
        if self.CurrentToken().matches(Consts.KEY, Consts.IF):
            return IfExp(self.parser).Rule()
        if self.CurrentToken().matches(Consts.KEY, Consts.LET):
            self.NextToken()
            if self.CurrentToken().type != Consts.ID:
                return ast.fail(f"{Error.parserError}: Esperado '{Consts.ID}'")
            varName = self.CurrentToken()
            self.NextToken()
            if self.CurrentToken().type != Consts.EQ:
                return ast.fail(f"{Error.parserError}: Esperado '{Consts.EQ}'")
            return self.varAssign(ast, varName)
        #trecho alterado para aceitar '()' da tupla
        if (self.CurrentToken().type == Consts.ID):
            if (self.parser.Lookahead(1).type == Consts.EQ):
                varName = self.CurrentToken()
                self.NextToken()
                return self.varAssign(ast, varName)
        node = ast.registry(NoOpBinaria.Perform(Term(self.parser), (Consts.PLUS, Consts.MINUS)))
        if ast.error:
            return ast.fail(f"{Error.parserError}: Esperado a '{Consts.INT}', '{Consts.FLOAT}', '{Consts.ID}', '{Consts.LET}', '{Consts.PLUS}', '{Consts.MINUS}', '{Consts.LPAR}'")
        return ast.success(node)

    def varAssign(self, ast, varName):
        self.NextToken()
        expr = ast.registry(Exp(self.parser).Rule())
        if ast.error: return ast
        return ast.success(NoVarAssign(varName, expr))

class Term(Grammar): # A variable from Grammar G
    def Rule(self):
        return NoOpBinaria.Perform(Factor(self.parser), (Consts.MUL, Consts.DIV))

class Factor(Grammar): # A variable from Grammar G
    def Rule(self):
        ast = self.GetParserManager()
        tok = self.CurrentToken()

        if tok.type in (Consts.PLUS, Consts.MINUS):
            self.NextToken()
            factor = ast.registry(Factor(self.parser).Rule())
            if ast.error: return ast
            return ast.success(NoOpUnaria(tok, factor))
        return Pow(self.parser).Rule()

class Pow(Grammar): # A variable from Grammar G
    def Rule(self):
        return NoOpBinaria.Perform(Atom(self.parser), (Consts.POW, ), Factor(self.parser))

#atom atualizado para receber novas funções
class Atom(Grammar): # A variable from Grammar G
    def Rule(self):
        ast = self.GetParserManager()
        tok = self.CurrentToken()
        if tok.type in (Consts.INT, Consts.FLOAT):
            self.NextToken()
            return ast.success(NoNumber(tok))
        elif tok.type == Consts.ID:
            self.NextToken()
            return ast.success(NoVarAccess(tok))
        elif(tok.type == Consts.STRING):
            self.NextToken()
            return ast.success(NoString(tok))
        elif tok.type == Consts.BOOL:
            self.NextToken()
            return ast.success(NoBoolean(tok))

        ##############################
        elif tok.type == Consts.LSQUARE:
            listExp = ast.registry(ListExp(self.parser).Rule())
            if (ast.error!=None): return ast
            return ast.success(listExp)
        ##############################
        elif tok.type == Consts.LPAR:
            if self.parser.Lookahead(1).type != Consts.RPAR and self.parser.Lookahead(2).type == Consts.COMMA:
                return TupleExp(self.parser).Rule()  # Trata como tupla

            self.NextToken()  # Consome '('
            exp = ast.registry(Exp(self.parser).Rule())
            if ast.error: return ast

            if self.CurrentToken().type == Consts.RPAR:
                self.NextToken()
                return ast.success(exp)
            else:
                return ast.fail(f"{Error.parserError}: Esperando por '{Consts.RPAR}'")

        return ast.fail(f"{Error.parserError}: Esperado por '{Consts.INT}', '{Consts.FLOAT}', '{Consts.PLUS}', '{Consts.MINUS}', '{Consts.LPAR}'")

##############################
class ListExp(Grammar):
    def Rule(self):
        ast = self.GetParserManager()
        elementNodes = []
        self.NextToken()

        if (self.CurrentToken().type == Consts.RSQUARE): # TList vazia
            self.NextToken()
        else:
            elementNodes.append(ast.registry(Exp(self.parser).Rule()))
            if (ast.error!=None):
                return ast.fail(f"{Error.parserError}: Esperando por '{Consts.RSQUARE}', '{Consts.KEYS[Consts.LET]}', '{Consts.INT}', '{Consts.FLOAT}', '{Consts.ID}', '{Consts.PLUS}', '{Consts.MINUS}', '{Consts.LPAR}', '{Consts.LSQUARE}'")
            
            while (self.CurrentToken().type == Consts.COMMA):
                self.NextToken()

                elementNodes.append(ast.registry(Exp(self.parser).Rule()))
                if (ast.error!=None): return ast

            if (self.CurrentToken().type != Consts.RSQUARE):
                return ast.fail(f"{Error.parserError}: Esperando por '{Consts.COMMA}' ou '{Consts.RSQUARE}'")
            self.NextToken()
        
        return ast.success(NoList(elementNodes))
#tupla implementada aqui
class TupleExp(Grammar):
    def Rule(self):
        ast = self.GetParserManager()
        elements = []

        self.NextToken()  # consome '('

        if self.CurrentToken().type == Consts.RPAR:
            # tupla vazia: ()
            self.NextToken()
            return ast.success(NoTuple([]))

        # primeira expressão
        elements.append(ast.registry(Exp(self.parser).Rule()))
        if ast.error: return ast

        while self.CurrentToken().type == Consts.COMMA:
            self.NextToken()
            elements.append(ast.registry(Exp(self.parser).Rule()))
            if ast.error: return ast

        if self.CurrentToken().type != Consts.RPAR:
            return ast.fail(f"{Error.parserError}: Esperando por '{Consts.RPAR}'")

        self.NextToken()
        return ast.success(NoTuple(elements))

#IF implementado
class IfExp(Grammar):
    def Rule(self):
        ast = self.GetParserManager()

        if not self.CurrentToken().matches(Consts.KEY, Consts.IF):
            return ast.fail(f"{Error.parserError}: Esperado '{Consts.IF}'")
        self.NextToken()
        condition = ast.registry(Exp(self.parser).Rule())

        if ast.error: return ast

        if not self.CurrentToken().matches(Consts.KEY, Consts.THEN):
            return ast.fail(f"{Error.parserError}: Esperado '{Consts.THEN}'")

        self.NextToken()
        then_branch = ast.registry(Exp(self.parser).Rule())
        if ast.error: return ast

        else_branch = None
        if self.CurrentToken().matches(Consts.KEY, Consts.ELSE):
            self.NextToken()
            else_branch = ast.registry(Exp(self.parser).Rule())
            if ast.error: return ast

        return ast.success(NoIf(condition, then_branch, else_branch))

"""
nova classe criada para uso de expreções relacionadas
"""
class ExpRelacional(Grammar):
    def Rule(self):
        return NoOpBinaria.Perform(ExpAritmetica(self.parser),
            (Consts.EQEQ, Consts.NE, Consts.LT, Consts.GT, Consts.LE, Consts.GE))

"""
nova classe EXP para atuar como ponto de entrada principal, ela despacha o parsing para duas possibilidades 
Se a expressão começa com if, ela encaminha para IfExp, que trata o if ... then ... else ...

Caso contrário, ela envia para ExpRelacional, que trata as outras expreções (+, -, >, <= ,....)
"""
class Exp(Grammar):
    def Rule(self):
        ast = self.GetParserManager()

        if self.CurrentToken().matches(Consts.KEY, Consts.IF):
            return IfExp(self.parser).Rule()

        if self.CurrentToken().matches(Consts.KEY, Consts.WHILE):
            return WhileExp(self.parser).Rule()

        return ExpRelacional(self.parser).Rule()

class WhileExp(Grammar):
    def Rule(self):
        ast = self.GetParserManager()

        if not self.CurrentToken().matches(Consts.KEY, Consts.WHILE):
            return ast.fail(f"{Error.parserError}: Esperado '{Consts.WHILE}'")

        self.NextToken()

        cond = ast.registry(Exp(self.parser).Rule())
        if ast.error: return ast

        if not self.CurrentToken().matches(Consts.KEY, Consts.DO):
            return ast.fail(f"{Error.parserError}: Esperado '{Consts.DO}'")

        self.NextToken()

        body = ast.registry(Exp(self.parser).Rule())
        if ast.error: return ast

        return ast.success(NoWhile(cond, body))
