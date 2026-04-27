############################
# PARSER
############################  
from errors import *
from tokens import *
from parse_result import *
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens=tokens
        self.tok_idx=-1
        self.advance()
    def advance(self):
        self.tok_idx+=1
        self.update_current_tok()
        return self.current_tok
    def reverse(self, amount=1):
        self.tok_idx-=amount
        self.update_current_tok()

    def update_current_tok(self):
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

=======
=======
>>>>>>> parent of 64a8eac (new)
        if self.tok_idx>=0 and self.tok_idx<len(self.tokens):
            self.current_tok=self.tokens[self.tok_idx]
    
    
<<<<<<< HEAD
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
>>>>>>> parent of 64a8eac (new)
    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', '/', 'VAR', 'IF', 'FOR', 'WHILE', 'DEF', int, float, identifier, or '('"
            ))
        return res
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py

=======
    
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
    
>>>>>>> parent of 64a8eac (new)
    def statements(self):
        res=ParseResult()
        statements=[]
        pos_start=self.current_tok.pos_start.copy()

        while self.current_tok.type==TT_NEWLINE:
            res.register_advancement()
            self.advance()

<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py
        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                break
            statements.append(statement)

        return res.success(ListNode(statements, pos_start, self.current_tok.pos_end.copy()))

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, 'RETURN'):
            res.register_advancement()
            self.advance()
            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'CONTINUE'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'BREAK'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error: return res
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))
            var_name = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'DEF', int, float, identifier, '+', '-', or '('"
            ))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(', or 'NOT'"
            ))
        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            op_tok = tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (TT_POW,), self.factor)  # ← fixed tuple and func_b

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
=======
=======
>>>>>>> parent of 64a8eac (new)
        statement=res.register(self.expr())
        if res.error: return res
        statements.append(statement)

        more_statements=True

        while True:
            newline_count=0
            while self.current_tok.type==TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count+=1
            if newline_count==0:
                more_statements=False
            if not more_statements: break
            statement=res.register(self.expr())
            if res.error: return res
            statements.append(statement)

        return res.success(ListNode(statements, pos_start, self.current_tok.pos_end.copy()))

    def call(self):
        res=ParseResult()
        atom=res.register(self.atom())
<<<<<<< HEAD
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
>>>>>>> parent of 64a8eac (new)
        if res.error: return res

        if self.current_tok.type==TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes=[]

            if self.current_tok.type==TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'DEF', int, float, identifier, '+', '-', or '('"
                    ))
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py

                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()
                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res
=======
=======
>>>>>>> parent of 64a8eac (new)
                
                while self.current_tok.type==TT_COMMA:
                    res.register_advancement()
                    self.advance()
<<<<<<< HEAD
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
>>>>>>> parent of 64a8eac (new)

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res
                
                if self.current_tok.type!=TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ',' or ')'"
                    ))
                
                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res=ParseResult()
        tok=self.current_tok
        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        
        elif tok.type in (TT_INT, TT_FLOAT, TT_STRING):
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))
        
        elif tok.type==TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
            
        
        elif tok.type == TT_LSQUARE:
            list_expr=res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)
        
        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr=res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        
        elif tok.matches(TT_KEYWORD, 'FOR'):
            for_expr=res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)
        
        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr=res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)
        
        elif tok.matches(TT_KEYWORD, 'DEF'):
            func_def=res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '*', '/', or '('"
        ))
    
    def list_expr(self):
        res=ParseResult()
        element_nodes=[]
        pos_start=self.current_tok.pos_start.copy()
        if self.current_tok.type!=TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))
        res.register_advancement()
        self.advance()

        if self.current_tok.type==TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error: return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'DEF', int, float, identifier, '+', '-', or '('"
            ))

            while self.current_tok.type==TT_COMMA:
                res.register_advancement()
                self.advance()

<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)
=======
=======
>>>>>>> parent of 64a8eac (new)
                element_nodes.append(res.register(self.expr()))
                if res.error: return res
            
            if self.current_tok.type!=TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ']'"
                ))
            
            res.register_advancement()
            self.advance()
        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy()))
<<<<<<< HEAD
>>>>>>> parent of 64a8eac (new):proiect/parser.py

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:  # ← fixed: was duplicating INT/FLOAT check
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'DEF'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, string, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE', or 'DEF'"
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'DEF', int, float, identifier, '+', '-', or '('"
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ']'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(element_nodes, pos_start, self.current_tok.pos_end.copy()))
=======
>>>>>>> parent of 64a8eac (new)

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None
        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'THEN'"
            ))
        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'THEN'"
                ))
            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res
            cases.append((condition, expr))

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error: return res

<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py
        return res.success((cases, else_case))  # ← was missing from single-line path
=======
        return res.success(IfNode(cases, else_case))
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
        return res.success(IfNode(cases, else_case))
>>>>>>> parent of 64a8eac (new)

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'FOR'"
            ))
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py

=======
        
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
        
>>>>>>> parent of 64a8eac (new)
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            ))
        
        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '='"
            ))
        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'TO'"
            ))
        
        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res


        if self.current_tok.matches(TT_KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'THEN'"
            ))
        
        res.register_advancement()
        self.advance()

<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py
        if self.current_tok.type == TT_NEWLINE:  # ← multiline support added
            res.register_advancement()
            self.advance()
            body = res.register(self.statements())
            if res.error: return res
            if not self.current_tok.matches(TT_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'END'"
                ))
            res.register_advancement()
            self.advance()
            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

=======
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
>>>>>>> parent of 64a8eac (new)
        body = res.register(self.expr())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))
    
    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'WHILE'"
            ))
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py

=======
        
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
        
>>>>>>> parent of 64a8eac (new)
        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'THEN'"
            ))
        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error: return res

        return res.success(WhileNode(condition, body))

    def power(self):
        return self.bin_op(self.call, (TT_POW,self.factor))

    def factor(self):
        res = ParseResult()
        tok=self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            op_tok=tok
            res.register_advancement()
            self.advance()
            factor=res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, factor))
        
        return self.power()
    
    def comp_expr(self):
        res=ParseResult()
        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok=self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        node=res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '*', '/', '(', or 'NOT'"
            ))

        return res.success(node)
    
    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'DEF'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'DEF'"
            ))
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py

=======
        
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
        
>>>>>>> parent of 64a8eac (new)
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py
                    "Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier or '('"
=======
                    f"Expected '('"
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
                    f"Expected '('"
>>>>>>> parent of 64a8eac (new)
                ))

        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))
        
        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier"
                    ))
                
                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ')'"
                ))

        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier or ')'"
                ))
            
        res.register_advancement()
        self.advance()#
        if self.current_tok.type != TT_ARROW:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
<<<<<<< HEAD
<<<<<<< HEAD:proiect/my_parser.py
                "Expected '->' or NEWLINE"
=======
                "Expected '->'"
>>>>>>> parent of 64a8eac (new):proiect/parser.py
            ))
        res.register_advancement()
        self.advance()
<<<<<<< HEAD:proiect/my_parser.py

        body = res.register(self.statements())
=======
        node_to_return = res.register(self.expr())
>>>>>>> parent of 64a8eac (new):proiect/parser.py
        if res.error: return res
        return res.success(FuncDefNode(var_name_tok, arg_name_toks, node_to_return))

<<<<<<< HEAD:proiect/my_parser.py
        if not self.current_tok.matches(TT_KEYWORD, 'END'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'END'"
            ))

        res.register_advancement()
        self.advance()
        return res.success(FuncDefNode(var_name_tok, arg_name_toks, body, True))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while (self.current_tok is not None and
               (self.current_tok.type in ops or
                (self.current_tok.type, self.current_tok.value) in ops)):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
=======
=======
                "Expected '->'"
            ))
        res.register_advancement()
        self.advance()
        node_to_return = res.register(self.expr())
        if res.error: return res
        return res.success(FuncDefNode(var_name_tok, arg_name_toks, node_to_return))

>>>>>>> parent of 64a8eac (new)
    def bin_op(self, func_a, ops, func_b=None):
        if func_b==None:
            func_b=func_a
        res = ParseResult()
        left= res.register(func_a())
        if res.error: return res
        while self.current_tok!=None and self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok=self.current_tok
            res.register_advancement()
            self.advance()
            right=res.register(func_b())
            if res.error: return res
            left=BinOpNode(left, op_tok, right)
        return res.success(left)
    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    def expr(self):
        res=ParseResult()
        if self.current_tok.matches(TT_KEYWORD, 'IF'):
            if_expr=res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()
            if self.current_tok.type!=TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))
            var_name=self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type!=TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))
            res.register_advancement()
            self.advance()
            expr=res.register(self.expr()) 
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))
        
        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'VAR', int, float, identifier, '+', '-', or '('"
            ))
<<<<<<< HEAD
        return res.success(node)
>>>>>>> parent of 64a8eac (new):proiect/parser.py
=======
        return res.success(node)
>>>>>>> parent of 64a8eac (new)
