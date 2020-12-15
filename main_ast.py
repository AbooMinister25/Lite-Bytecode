class Ast:
    pass

class Instructions:
    instructions = {
        "instructions": [],
        "numbers": [],
        "strings": []
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


class Print(Ast):
    def __init__(self, value):
        self.value = value

    def compile(self):
        self.value.compile()
        instructions["instructions"].append(("PRINT_VALUE", None))


class String(Ast):
    def __init__(self, value):
        self.value = str(value).strip('"')
    
    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["strings"].append(self.value)


class Integer(Ast):
    def __init__(self, value):
        self.value = int(value)
    
    def compile(self):
        instructions["instructions"].append(("LOAD_VALUE", 0))
        instructions["numbers"].append(self.value)


class Start():
    def __init__(self, statements):
        self.statements = statements

    def compile(self):
        for statement in self.statements:
            statement.compile()

    def __repr__(self):
        return f"Start({self.statements})"