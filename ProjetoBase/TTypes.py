from Consts import Consts
from Error import Error
"""
o motivo de criar esse arquivo
TValue define o comportamento comum a todos os tipos de valor: como adicionar, 
copiar, ou lançar erros se algo não for suportado.

Evita duplicação de código. Ex: todos os tipos implementam setMemory(), copy(), __repr__(), etc., 
e esses padrões são herdados.
"""
class TValue():
    def __init__(self):
        self.value = None

    def setMemory(self, memory=None):
        return self.exceptionError(f"The 'setMemory({memory})' method not supported on the {Error.classNameOf(self)} class!")

    def add(self, other):
        return self.exceptionError(f"The 'add({self}{Consts.PLUS}{other})' method not supported on the {Error.classNameOf(self)} class!")

    def sub(self, other):
        return self.exceptionError(f"The 'sub({self}{Consts.MINUS}{other})' method not supported on the {Error.classNameOf(self)} class!")

    def mult(self, other):
        return self.exceptionError(f"The 'mult({self}{Consts.MUL}{other})' method not supported on the {Error.classNameOf(self)} class!")

    def div(self, other):
        return self.exceptionError(f"The 'div({self}{Consts.DIV}{other})' method not supported on the {Error.classNameOf(self)} class!")

    def pow(self, other):
        return self.exceptionError(f"The 'pow({self}{Consts.POW}{other})' method not supported on the {Error.classNameOf(self)} class!")

    def copy(self):
        return self.exceptionError("The 'copy()' method not supported on the " + Error.classNameOf(self) + " class!")

    def exceptionError(self, error_msn: str):
        return None, Error(f"{Error.runTimeError}: {error_msn}")

    def __eq__(self, value: object) -> bool:
        if isinstance(value, TValue):
            return self.value == value.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

# -------------------- TNumber --------------------

class TNumber(TValue):
    def __init__(self, value):
        self.value = value
        self.setMemory()

    def setMemory(self, memory=None):
        self.memory = memory
        return self

    def add(self, other):
        if isinstance(other, TNumber):
            return TNumber(self.value + other.value).setMemory(self.memory), None
        return super().add(other)

    def sub(self, other):
        if isinstance(other, TNumber):
            return TNumber(self.value - other.value).setMemory(self.memory), None
        return super().sub(other)

    def mult(self, other):
        if isinstance(other, TNumber):
            return TNumber(self.value * other.value).setMemory(self.memory), None
        return super().mult(other)

    def div(self, other):
        if isinstance(other, TNumber):
            if other.value == 0:
                return self.exceptionError("Divisão por zero")
            return TNumber(self.value / other.value).setMemory(self.memory), None
        return super().div(other)

    def pow(self, other):
        if isinstance(other, TNumber):
            return TNumber(self.value ** other.value).setMemory(self.memory), None
        return super().pow(other)

    def copy(self):
        return TNumber(self.value).setMemory(self.memory)

    def __repr__(self):
        return str(self.value)

# -------------------- TString --------------------

class TString(TValue):
    def __init__(self, value):
        self.value = value
        self.setMemory()

    def setMemory(self, memory=None):
        self.memory = memory
        return self

    def add(self, other):
        if isinstance(other, TString):
            return TString(self.value + other.value).setMemory(self.memory), None
        return super().add(other)

    def copy(self):
        return TString(self.value).setMemory(self.memory)

    def __repr__(self):
        return f'"{str(self.value)}"'

# -------------------- TList --------------------

class TList(TValue):
    def __init__(self, value):
        self.value = value
        self.setMemory()

    def setMemory(self, memory=None):
        self.memory = memory
        return self

    def add(self, other):
        if isinstance(other, TList):
            return TList(self.value + other.value).setMemory(self.memory), None
        return super().add(other)

    def copy(self):
        return TList(self.value).setMemory(self.memory)

    def __repr__(self):
        return f"{str(self.value)}"

# -------------------- TTuple --------------------

class TTuple(TValue):
    def __init__(self, value):
        self.value = tuple(value)
        self.setMemory()

    def setMemory(self, memory=None):
        self.memory = memory
        return self

    def copy(self):
        return TTuple(self.value).setMemory(self.memory)

    def __repr__(self):
        return f"({', '.join(map(str, self.value))})"

# -------------------- TBoolean --------------------

class TBoolean(TValue):
    def __init__(self, value):
        self.value = value
        self.setMemory()

    def setMemory(self, memory=None):
        self.memory = memory
        return self

    def copy(self):
        return TBoolean(self.value).setMemory(self.memory)

    def __repr__(self):
        return "true" if self.value else "false"
