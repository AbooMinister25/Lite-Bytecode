class Env():
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.arg_functions = {}
        self.args = {}

    def get_variable(self, name):
        return self.variables[name]

    def assign_variable(self, name, value):
        self.variables[name] = value

    def define_function(self, name, eval_expr, args):
        self.functions[name] = {"eval": eval_expr, "args": args}

    def assign_args(self, name, args):
        self.args[name] = args

    def define_args_function(self, name, eval_expr):
        self.arg_functions[name] = eval_expr

    def call_function(self, name, args):
        try:
            if self.functions[name]["args"] == None:
                if args != None:
                    raise TypeError("Invalid Arguments Given")
                return self.functions[name]["eval"].eval(self)
            len_args = len(self.functions[name]["args"].eval(self))
            if args is None:
                pass
            else:
                if len_args == len(args):
                    eval_args = [arg.eval(self) for arg in args]
                    for arg in eval_args:
                        self.functions[name]["eval"].local.assign_variable(self.functions[name]["args"].eval(self)[eval_args.index(arg)], arg)
                else:
                    return Exception("Invalid Number Of Arguments Given")
        except Exception as e:
            raise e
        return self.functions[name]["eval"].eval(self)

    def call_args_function(self, name, args):
        try:
            return self.arg_functions[name](args)
        except:
            raise Exception(f"Function {name} not found")

    def get_array_index(self, name, index):
        return self.variables[name]
    
    def get_dict_keys(self, name):
        return [key for key in self.variables[name].keys()]
    
    def get_index(self, name, value):
        return self.variables[name].index(value)
