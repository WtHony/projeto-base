#nada foi alterado
from RuntimeMemory import MemoryManager

class CodeGEN:
	def run(self, semanticNode):
		res = semanticNode.visit(MemoryManager.instanceOfMemoryManager())
		return res

