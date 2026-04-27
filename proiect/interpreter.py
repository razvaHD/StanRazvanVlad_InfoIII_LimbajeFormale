############################
# INTERPRETER
############################

import os
from unicodedata import name

from parser import *
from rtresult import *
from results import *
from context import *
from symbol_table import *

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
            self.pos_start, self.pos_end,
            f"{len(args) - len(arg_names)} too many args passed into {self}",
            self.context
        ))
        
        if len(args) < len(arg_names):
            return res.failure(RTError(
            self.pos_start, self.pos_end,
            f"{len(arg_names) - len(args)} too few args passed into {self}",
            self.context
        ))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.error: return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.error: return res

        return_value = res.register(method(exec_ctx))
        if res.error: return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')
    
    def __repr__(self):
        return f"<built-in function {self.name}>"
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number.null)
    execute_print.arg_names = ['value']

    def execute_print_ret(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print_ret.arg_names = ['value']

    def execute_input(self, exec_ctx):
        text = input()
        return RTResult().success(String(text))
    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        while True:
            text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))
    execute_input_int.arg_names = []

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'cls')
        return RTResult().success(Number.null)
    execute_clear.arg_names = []

    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Number.true if is_number else Number.false)
    execute_is_function.arg_names = ["value"]

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        list_.elements.append(value)
        return RTResult().success(Number.null)
    execute_append.arg_names = ["list", "value"]

    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number",
                exec_ctx
            ))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)
    execute_pop.arg_names = ["list", "index"]

    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))

        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list",
                exec_ctx
            ))

        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)
    execute_extend.arg_names = ["listA", "listB"]

BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.print_ret   = BuiltInFunction("print_ret")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.input_int   = BuiltInFunction("input_int")
BuiltInFunction.clear       = BuiltInFunction("clear")
BuiltInFunction.is_number   = BuiltInFunction("is_number")
BuiltInFunction.is_string   = BuiltInFunction("is_string")
BuiltInFunction.is_list     = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append      = BuiltInFunction("append")
BuiltInFunction.pop         = BuiltInFunction("pop")
BuiltInFunction.extend      = BuiltInFunction("extend")

class Function:
    def __init__(self, name, body_node, arg_names):
        self.name=name or '<anonymous>'
        self.body_node=body_node
        self.arg_names=arg_names
        self.set_pos()
        self.set_context()
    
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start=pos_start
        self.pos_end=pos_end
        return self
    
    def set_context(self, context=None):
        self.context=context
        return self
    
    def copy(self):
        copy=Function(self.name, self.body_node, self.arg_names)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def execute(self, args):
        res=RTResult()
        interpreter=Interpreter()
        new_context=Context(self.name, self.context, self.pos_start)
        new_context.symbol_table=SymbolTable(new_context.parent.symbol_table)

        if len(args)>len(self.arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args)-len(self.arg_names)} too many args passed into '{self.name}'",
                self.context
            ))
        
        if len(args)<len(self.arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(self.arg_names)-len(args)} too few args passed into '{self.name}'",
                self.context
            ))
        
        for i in range(len(args)):
            arg_name=self.arg_names[i]
            arg_value=args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value=res.register(interpreter.visit(self.body_node, new_context))
        if res.error: return res
        return res.success(value)
    def __repr__(self):
        return f"<function {self.name}>"

class Interpreter():
    def visit(self, node, context):
        method_name=f'visit_{type(node).__name__}'
        method=getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    

    def visit_NumberNode(self, node, context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_StringNode(self, node, context):
        return RTResult().success(String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_ListNode(self, node, context):
        res=RTResult()
        elements=[]

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res
        
        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node, context):
        res=RTResult()
        var_name=node.var_name_tok.value
        value=context.symbol_table.get(var_name)

        if value==None:
            return res.failure(RTError(node.pos_start, node.pos_end, f"'{var_name}' is not defined", context))
        value=value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    
    def visit_VarAssignNode(self, node, context):
        res=RTResult()
        var_name=node.var_name_tok.value
        value=res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res=RTResult()
        left =res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.op_tok.pos_start, node.op_tok.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res=RTResult()
        number = res.register(self.visit(node.node, context))

        error=None

        if res.error: return res
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))

        elif node.op_tok.type == TT_PLUS:
            pass

        elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
            number, error = number.notted()
            if error: return res.failure(error)
        if error:
            return res.failure(error)
        return RTResult().success(number.set_pos(node.op_tok.pos_start, node.op_tok.pos_end))
    
    def visit_IfNode(self, node, context):
        res=RTResult()

        for condition, expr in node.cases:
            condition_value=res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value=res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)
        
        if node.else_case:
            else_value=res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)
        
        return res.success(None)
    
    def visit_ForNode(self, node, context):
        res=RTResult()
        element = []

        start_value=res.register(self.visit(node.start_value_node, context))
        if res.error: return res

        end_value=res.register(self.visit(node.end_value_node, context))
        if res.error: return res

        if node.step_value_node:
            step_value=res.register(self.visit(node.step_value_node, context))
            if res.error: return res
        else:
            step_value=Number(1)

        i=start_value.value

        if step_value.value >= 0:
            condition=lambda: i < end_value.value
        else:
            condition=lambda: i > end_value.value
        
        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i+=step_value.value

            element.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res
        
        return res.success(List(element).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_WhileNode(self, node, context):
        res=RTResult()
        element = []

        while True:
            condition=res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.is_true():
                break
            
            element.append(res.register(self.visit(node.body_node, context)))
            if res.error: return res
        
        return res.success(List(element).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_FuncDefNode(self, node, context):
        res=RTResult()

        func_name=node.var_name_tok.value if node.var_name_tok else None
        body_node=node.body_node
        arg_names=[arg_name.value for arg_name in node.arg_name_toks]
        func_value=Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res=RTResult()
        args=[]

        value_to_call=res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call=value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res
        
        return_value=res.register(value_to_call.execute(args))
        if res.error: return res
        return res.success(return_value)