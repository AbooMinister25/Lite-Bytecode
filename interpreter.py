from transformer import LiteTransformer, instructions
from lark import Lark
import time

class Machine:
    def __init__(self):
        self.stack = []
        self.environment = {}
    
    def LOAD_VALUE(self, value):
        self.stack.append(value)
    
    def PRINT_VALUE(self):
        answer = self.stack.pop()
        print(answer)
    
    def INPUT_VALUE(self):
        answer = self.stack.pop()
        input(answer)
    
    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.environment[name] = val
    
    def LOAD_NAME(self, name):
        val = self.environment[name]
        self.stack.append(val)
    
    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)
    
    def SUB_TWO_VALUES(self):
        second_num = self.stack.pop()
        first_num = self.stack.pop()
        total = first_num - second_num
        self.stack.append(total)

    def MUL_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num * second_num
        self.stack.append(total)

    def DIV_TWO_VALUES(self):
        print(self.stack)
        second_num = self.stack.pop()
        first_num = self.stack.pop()
        total = first_num / second_num
        self.stack.append(total)
    
    def parse_argument(self, instruction, argument, what_to_execute):
        values = ["LOAD_VALUE"]
        names = ["LOAD_NAME", "STORE_NAME"]
        
        if instruction in values:
            try:
                argument = what_to_execute["numbers"][argument]
            except:
                argument = what_to_execute["strings"][argument]
        elif instruction in names:
            argument = what_to_execute["names"][argument]
        
        return argument
    
    def execute(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)                

parser = Lark.open('grammar.lark', parser="lalr")


with open("test.lite", "r") as f:
    lite_code = f.read()
before = time.time()
tree = parser.parse(lite_code)
x = LiteTransformer().transform(tree)
x.compile()
interpreter = Machine()
interpreter.execute(instructions)
difference = time.time() - before
print(difference)