import abc

from Consts import Consts
from Error import Error
from TTypes import TNumber, TString, TList, TTuple, TBoolean

"""
# * Aqui são incluídos os NO's da AST (Abstract Syntax Tree).
# * Eles aceitam visitas de operadores de memoria, visando semantica e controle de tipos (para execucao ou compilacao).
# * Tipos: - criamos a classe TValue especializada em tratar tipos e valores.
#         - Partimos da ideia de que todo dado possui um tipo e valor.

"""
class Visitor(metaclass=abc.ABCMeta): # OBS: os parametros "operator" sao do tipo "MemoryManager", para "runtime" e acesso a memória/tabela de simbolos
	@abc.abstractmethod
	def visit(self, operator): operator.fail(Error(f"{Error.runTimeError}: Nenhum metodo visit para a classe '{Error.classNameOf(self)}' foi definido!"))

	def __repr__(self): (f"TODO: implements __repr__ of '{Error.classNameOf(self)}' class")
	
class NoNumber(Visitor):
	def __init__(self, tok):
		self.tok = tok

	def visit(self, operator):
		return operator.success(TNumber(self.tok.value).setMemory(operator))

	def __repr__(self):
		return f'{self.tok}'
	
class NoOpUnaria(Visitor):
	def __init__(self, opTok, node):
		self.opTok = opTok
		self.node = node

	def visit(self, operator):
		num = operator.registry(self.node.visit(operator))
		if operator.error: return operator
		error = None
		if self.opTok.type == Consts.MINUS:
			num, error = num.mult(TNumber(-1))
		if error:
			return operator.fail(error)
		else:
			return operator.success(num)

	def __repr__(self):
		return f'({self.opTok}, {self.node})'

class NoOpBinaria(Visitor):
	def __init__(self, leftNode, opTok, rightNode):
		self.noEsq = leftNode
		self.opTok = opTok
		self.noDir = rightNode
	
	def __repr__(self):
		return f'({self.noEsq}, {self.opTok}, {self.noDir})'
	
	@staticmethod
	def Perform(GVar1, ops, GVar2=None): # Grammar Var (GVar), Operator options (ops=+,- ou *, /)
		if GVar2==None: GVar2 = GVar1
		ast = GVar1.GetParserManager()
		op_bin_ou_esq = ast.registry(GVar1.Rule())
		if ast.error: return ast
		while GVar1.CurrentToken().type in ops:
			token_operador = GVar1.CurrentToken()
			GVar1.NextToken()
			lado_direito = ast.registry(GVar2.Rule())
			if ast.error: return ast
			op_bin_ou_esq = NoOpBinaria(op_bin_ou_esq, token_operador, lado_direito)
		return ast.success(op_bin_ou_esq)
	
	def visit(self, operator):
		esq = operator.registry(self.noEsq.visit(operator))
		if operator.error: return operator
		dir = operator.registry(self.noDir.visit(operator))
		if operator.error: return operator

		if self.opTok.type == Consts.PLUS:
			result, error = esq.add(dir)
		elif self.opTok.type == Consts.MINUS:
			result, error = esq.sub(dir)
		elif self.opTok.type == Consts.MUL:
			result, error = esq.mult(dir)
		elif self.opTok.type == Consts.DIV:
			result, error = esq.div(dir)
		elif self.opTok.type == Consts.POW:
			result, error = esq.pow(dir)
		elif self.opTok.type == Consts.EQEQ:
			result, error = TBoolean(esq == dir), None
		elif self.opTok.type == Consts.NE:
			result, error = TBoolean(esq != dir), None
		elif self.opTok.type == Consts.LT:
			result, error = TBoolean(esq.value < dir.value), None
		elif self.opTok.type == Consts.GT:
			result, error = TBoolean(esq.value > dir.value), None
		elif self.opTok.type == Consts.LE:
			result, error = TBoolean(esq.value <= dir.value), None
		elif self.opTok.type == Consts.GE:
			result, error = TBoolean(esq.value >= dir.value), None

		if error:
			return operator.fail(error)
		else:
			return operator.success(result)
##############################
class NoVarAssign(Visitor):
	def __init__(self, varNameTok, valueNode):
		self.varNameTok = varNameTok
		self.valueNode = valueNode

	def visit(self, operator):
		varName = self.varNameTok.value
		value = operator.registry(self.valueNode.visit(operator))
		if operator.error: return operator

		operator.symbolTable.set(varName, value)
		return operator.success(value)

	def __repr__(self):
		return f'({self.varNameTok}, {self.valueNode})'
	
class NoVarAccess(Visitor):
	def __init__(self, varNameTok):
		self.varNameTok = varNameTok

	def visit(self, operator):
		varName = self.varNameTok.value
		value = operator.symbolTable.get(varName)

		if not value: return operator.fail(Error(f"{Error.runTimeError}: '{varName}' nao esta definido"))

		value = value.copy()
		return operator.success(value)

	def __repr__(self):
		return f'({self.varNameTok})'
class NoString(Visitor):
	def __init__(self, tok):
		self.tok = tok

	def visit(self, operator):
		return operator.success(TString(self.tok.value).setMemory(operator))

	def __repr__(self):
		return f'{self.tok}'
##############################
class NoList(Visitor):
	def __init__(self, tok):
		self.elements = tok

	def visit(self, operator):
		return operator.success(TList(self.elements.value).setMemory(operator))

	def visit(self, operator):
		lValue = []

		for element_node in self.elements:
			lValue.append(operator.registry(element_node.visit(operator)))
		
		return operator.success(TList(lValue).setMemory(operator))

	def __repr__(self):
		return f'{self.elements}'

#implementação do NO da tupla
class NoTuple(Visitor):
	def __init__(self, elements):
		self.elements = elements

	def visit(self, operator):
		values = []
		for elem in self.elements:
			values.append(operator.registry(elem.visit(operator)))
		return operator.success(TTuple(values).setMemory(operator))

	def __repr__(self):
		return f"({', '.join(map(str, self.elements))})"

#implementa~çao do NO booleano
class NoBoolean(Visitor):
	def __init__(self, tok):
		self.tok = tok

	def visit(self, operator):
		value = True if self.tok.value == Consts.TRUE else False
		return operator.success(TBoolean(value).setMemory(operator))

	def __repr__(self):
			return f'{self.tok}'

#implementa~çao do NO IF
class NoIf(Visitor):
	def __init__(self, conditionNode, thenNode, elseNode=None):
		self.conditionNode = conditionNode
		self.thenNode = thenNode
		self.elseNode = elseNode

	def visit(self, operator):
		cond = operator.registry(self.conditionNode.visit(operator))
		if operator.error: return operator

		if not isinstance(cond, TBoolean):
			return operator.fail(Error(f"{Error.runTimeError}: condição não é booleana"))

		branch = self.thenNode if cond.value else self.elseNode
		if branch is None:
			return operator.success(TString("null"))
		return operator.registry(branch.visit(operator))

	def __repr__(self):
		return f"(if {self.conditionNode} then {self.thenNode} else {self.elseNode})"

class NoWhile(Visitor):
	def __init__(self, conditionNode, bodyNode):
		self.conditionNode = conditionNode
		self.bodyNode = bodyNode

	def visit(self, operator):
		while True:
			condValue = operator.registry(self.conditionNode.visit(operator))
			if operator.error: return operator

			if not isinstance(condValue, TBoolean):
				return operator.fail(Error(f"{Error.runTimeError}: condição do while não é booleana"))

			if not condValue.value:
				break

			operator.registry(self.bodyNode.visit(operator))
			if operator.error: return operator

		return operator.success(TString("ok"))

	def __repr__(self):
		return f"(while {self.conditionNode} do {self.bodyNode})"

class NoFor(Visitor):
    def __init__(self, varNameTok, startNode, endNode, bodyNode):
        self.varNameTok = varNameTok
        self.startNode = startNode  # Pode ser None se for apenas 'range(end)'
        self.endNode = endNode
        self.bodyNode = bodyNode

    def visit(self, operator):
        var_name = self.varNameTok.value

        # Avalia o valor final do range
        end_val_obj = operator.registry(self.endNode.visit(operator))
        if operator.error: return operator
        if not isinstance(end_val_obj, TNumber):
            return operator.fail(Error(f"{Error.runTimeError}: O valor final do range deve ser um número"))
        end_value = int(end_val_obj.value)

        # Avalia o valor inicial do range
        start_value = 0
        if self.startNode:
            start_val_obj = operator.registry(self.startNode.visit(operator))
            if operator.error: return operator
            if not isinstance(start_val_obj, TNumber):
                return operator.fail(Error(f"{Error.runTimeError}: O valor inicial do range deve ser um número"))
            start_value = int(start_val_obj.value)

        # Executa o loop
        for i in range(start_value, end_value):
            # Define a variável de iteração na tabela de símbolos
            operator.symbolTable.set(var_name, TNumber(i).setMemory(operator))

            # Avalia o corpo do loop e imprime o valor de i
            result = operator.registry(self.bodyNode.visit(operator))
            if operator.error: return operator  # Se houver erro no corpo, propaga

            # Imprime o resultado de i
            print(i)

        return operator.success(TString("ok"))  # Retorna "ok" ou outro valor indicando sucesso

    def __repr__(self):
        if self.startNode:
            return f"(for {self.varNameTok} in range({self.startNode}, {self.endNode}) do {self.bodyNode})"
        else:
            return f"(for {self.varNameTok} in range({self.endNode}) do {self.bodyNode})"
