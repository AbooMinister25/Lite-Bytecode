from transformer import LiteTransformer, instructions
from environment import Env
from lark import Lark
import time

class Machine:
    def __init__(self, env):
        self.stack = []
        self.env = env
        self.environment = {}
    
    def LOAD_VALUE(self, value):
        self.stack.append(value)
    
    def PRINT_VALUE(self):
        answer = self.stack.pop()
        print(answer)
    
    def INPUT_VALUE(self):
        answer = self.stack.pop()
        input(answer)
    
    def DEFINE_LOCAL(self, name):
        value = self.stack[-1]
        self.env.assign_variable(name, value)
    
    def LOAD_LOCAL(self, name):
        val = self.env.get_variable(name)
        self.stack.append(val)
    
    def LOAD_INDEX(self, name):
        self.stack.append(self.env.get_array_index(name, self.stack.pop()))
    
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
        second_num = self.stack.pop()
        first_num = self.stack.pop()
        total = first_num / second_num
        self.stack.append(total)
    
    def ADD_STRINGS(self):
        second_num = self.stack.pop()
        first_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)
    
    def parse_argument(self, instruction, argument, what_to_execute):
        values = ["LOAD_VALUE"]
        names = ["LOAD_LOCAL", "DEFINE_LOCAL", "LOAD_INDEX"]     
        if instruction in values:
            try:
                argument = what_to_execute["arrays"][argument]
                try:
                    what_to_execute["arrays"].remove(what_to_execute["arrays"][0])
                except:
                    pass
            except:
                try:
                    argument = what_to_execute["numbers"][argument]
                    try:
                        what_to_execute["numbers"].remove(what_to_execute["numbers"][0])
                    except:
                            pass
                except:
                    try:
                        argument = what_to_execute["strings"][argument]
                        try:
                            what_to_execute["strings"].remove(what_to_execute["strings"][0])
                        except:
                            pass
                    except:
                        argument = what_to_execute["dicts"][argument]
                        try:
                            what_to_execute["dicts"].remove(what_to_execute["dicts"][0])
                        except:
                            pass
                        
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
                
    
    def test_execute(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        print(f"Instructions:   {what_to_execute}")
        print("")
        counter = 0
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            print(f"Cycle_{counter}(Current Step: {each_step}, Current Stack: {self.stack}, Current Argument: {argument})")
            bytecode_method = getattr(self, instruction)
            print("Code Output:")
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)
            print("\n----------------- \n")
            counter += 1
    
    def debug(self, what_to_execute):
        instructions = what_to_execute["instructions"]
        for each_step in instructions:
            instruction, argument = each_step
            argument = self.parse_argument(instruction, argument, what_to_execute)
            bytecode_method = getattr(self, instruction)
            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)
                
            for i in self.stack:
                print(f"[ {i} ]")

parser = Lark.open('grammar.lark', parser="lalr")


with open("test.lite", "r") as f:
    lite_code = f.read()
tree = parser.parse(lite_code)
x = LiteTransformer().transform(tree)
x.compile()
interpreter = Machine(Env())
interpreter.execute(instructions)
