from lark import Lark, Transformer, v_args
from main_ast import *
import os.path
import sys

@v_args(inline=True)
class LiteTransformer(Transformer):
    def __init__(self):
        ...

    def number(self, value):
        return Integer(value)

    def string(self, value):
        value = str(value).strip('"')
        return String(value)
    
    def triple_string(self, value):
        return TripleQuoteString(value)
    
    def array(self, *value):
        return Array(value)
    
    def dictionary(self, key, value):
        return Dict(key, value)
    
    def number(self, value):
        return Integer(value)

    def add(self, val1, val2):
        return BinOp(val1, "+", val2)

    def sub(self, val1, val2):
        return BinOp(val1, "-", val2)

    def mul(self, val1, val2):
        return BinOp(val1, "*", val2)

    def div(self, val1, val2):
        return BinOp(val1, "/", val2)
    
    def str_add(self, val1, val2):
        return StringAdd(val1, val2)

    def print_statement(self, value, semicolon):
        return Print(value)
    
    def input_statement(self, value):
        return Input(value)
    
    def assign_var(self, name, value):
        return AssignVariable(name, value)
    
    def var_add_value(self, name, expr1, expr2):
        return AssignVarOp(name, expr1, expr2, "+")
    
    def get_var(self, name):
        return GetVariable(name)
    
    def get_index_value(self, name, index):
        return GetVariable(name, index)
    
    def start(self, *statements):
        return Start(statements)


instructions = instructions
