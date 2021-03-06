class Ast:
    pass


class Instructions:
    instructions = {
        "instructions": [],
        "numbers": [],
        "strings": [],
        "arrays": [],
        "dicts": [],
        "names": []
    }


class VariableValue:
    def __init__(self):
        self.locals = {}


variable_value = VariableValue()


instructions = Instructions.instructions

local_counter = 0


class BinOp(Ast):
    def __init__(self, left, op, right):
        self.left = int(left)
        self.right = int(right)
        self.op = op

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["numbers"].append(self.left)
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["numbers"].append(self.right)
        if self.op == "+":
            instructions["instructions"].append(("ADD_TWO_VALUES", None))
        elif self.op == "-":
            instructions["instructions"].append(("SUB_TWO_VALUES", None))
        elif self.op == "*":
            instructions["instructions"].append(("MUL_TWO_VALUES", None))
        elif self.op == "/":
            instructions["instructions"].append(("DIV_TWO_VALUES", None))


class StringAdd(Ast):
    def __init__(self, left, right):
        self.left = str(left).strip('"')
        self.right = str(right).strip('"')

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["strings"].append(self.left)
        instructions["instructions"].append(("LOAD_VALUE", 1))
        instructions["strings"].append(self.right)
        instructions["instructions"].append(("ADD_STRINGS", None))


class Print(Ast):
    def __init__(self, value):
        self.value = value

    def compile(self):
        self.value.compile()
        instructions["instructions"].append(("PRINT_VALUE", None))


class Input():
    def __init__(self, value):
        self.value = value

    def compile(self):
        self.value.compile()
        instructions["instructions"].append(("INPUT_VALUE", None))


class String(Ast):
    def __init__(self, value):
        self.value = str(value).strip('"')

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["strings"].append(self.value)


class TripleQuoteString(Ast):
    def __init__(self, value):
        self.value = value.strip()
        self.value = value.strip('"')

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["strings"].append(self.value)


class Integer(Ast):
    def __init__(self, value):
        self.value = int(value)

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["numbers"].append(self.value)


class Array(Ast):
    def __init__(self, value):
        self.value = []
        for val in value:
            if type(val) == Integer:
                self.value.append(val.value)
            elif type(val) == String:
                self.value.append(val.value)
            elif type(val) == Array:
                self.value.append(val.value)

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["arrays"].append(list([val for val in self.value]))


class Dict(Ast):
    def __init__(self, key, value):
        self.key = key.value
        self.value = value.value

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["dicts"].append(dict({self.key: self.value}))


class Name(Ast):
    def __init__(self, value):
        self.value = value

    def compile(self):
        instructions["names"].append(str(self.value[0]))


class AssignVariable(Ast):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def compile(self):
        global local_counter
        self.value.compile()
        instructions["instructions"].append(("DEFINE_LOCAL", local_counter))
        instructions["names"].append(self.name)
        variable_value.locals[self.name] = local_counter
        local_counter += 1


class GetVariable(Ast):
    def __init__(self, name, index=None):
        self.name = name
        self.index = index

    def compile(self):
        if self.index is not None:
            self.index.compile()
            instructions["instructions"].append(
                ("LOAD_INDEX", variable_value.locals[self.name]))
        else:
            instructions["instructions"].append(
                ("LOAD_LOCAL", variable_value.locals[self.name]))


class GetIndexValue():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def compile(self):
        self.value.compile()
        instructions["instructions"].append(("LOAD_INDEX", 0))


class Start(Ast):
    def __init__(self, statements):
        self.statements = statements

    def compile(self):
        for statement in self.statements:
            statement.compile()

    def __repr__(self):
        return f"Start({self.statements})"
