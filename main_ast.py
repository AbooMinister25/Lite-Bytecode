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


instructions = Instructions.instructions


class BinOp(Ast):
    def __init__(self, left, op, right):
        self.left = int(left)
        self.right = int(right)
        self.op = op

    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["numbers"].append(self.left)
        instructions["instructions"].append(("LOAD_VALUE", 1))
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


class AssignVariable(Ast):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def compile(self):
        self.value.compile()
        instructions["instructions"].append(("STORE_NAME", 0))
        instructions["names"].append(self.name)


class GetVariable(Ast):
    def __init__(self, name):
        self.name = name

    def compile(self):
        instructions["instructions"].append(("LOAD_NAME", 0))


class GetIndexValue():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def compile(self):
        instructions["instructions"].append(("LOAD_INDEX", 0))
        instructions["names"].append(self.name)


class Start(Ast):
    def __init__(self, statements):
        self.statements = statements

    def compile(self):
        for statement in self.statements:
            statement.compile()

    def __repr__(self):
        return f"Start({self.statements})"
