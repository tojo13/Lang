from python.ast import *
from python.token import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

        self.pos = -1
        self.token = None

    def eat(self):
        self.pos += 1
        if self.pos > len(self.tokens):
            raise RuntimeError("Unexpected end of file")
        self.token = self.tokens[self.pos]

    def eat_expecting(self, category):
        if self.token.category == category:
            self.eat()
        else:
            self.err_expecting(category)

    def err_expecting(self, *categories):
        if len(categories) == 1:
            category = categories[0]
            expectation = f"Expecting {category}"
        else:
            expectation = "Expecting one of [" + ", ".join(categories) + "]"
        raise SyntaxError(
            f"{expectation}, got {self.token.category} "
            f"at line={self.token.line} col={self.token.col}"
        )

    def parse(self):
        self.eat()
        ast = self.parse_program()
        return ast

    def parse_program(self):
        stmts = []
        while self.token.category in {NAME, PRINT}:
            stmt = self.parse_stmt()
            stmts.append(stmt)
        if self.token.category != EOF:
            self.err_expecting(EOF)
        program = Program(stmts)
        return program

    def parse_stmt(self):
        stmt = self.parse_simple_stmt()
        self.eat_expecting(NEWLINE)
        return stmt

    def parse_simple_stmt(self):
        if self.token.category == NAME:
            return self.parse_assignment_stmt()
        elif self.token.category == PRINT:
            return self.parse_print_stmt()
        else:
            self.err_expecting(NAME, PRINT)

    def parse_assignment_stmt(self):
        value = self.token.lexeme
        self.eat()
        self.eat_expecting(EQ)
        expr = self.parse_expr()
        return Assign(Name(value, ctx=NameCtx.STORE), expr)

    def parse_print_stmt(self):
        self.eat()
        self.eat_expecting(LPAREN)
        expr = self.parse_expr()
        self.eat_expecting(RPAREN)
        return Print(expr)

    def parse_expr(self):
        node = self.parse_term()
        while self.token.category in {PLUS, MINUS}:
            op_token = self.token
            self.eat()
            left_node = node
            right_node = self.parse_term()
            node = BinOp(left=left_node, op=op_token, right=right_node)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.token.category == TIMES:
            times_token = self.token
            self.eat()
            left_node = node
            right_node = self.parse_factor()
            node = BinOp(left=left_node, op=times_token, right=right_node)
        return node

    def parse_factor(self):
        if self.token.category == PLUS:
            plus_token = self.token
            self.eat()
            operand = self.parse_factor()
            return UnaryOp(op=plus_token, operand=operand)
        elif self.token.category == MINUS:
            minus_token = self.token
            self.eat()
            operand = self.parse_factor()
            return UnaryOp(op=minus_token, operand=operand)
        elif self.token.category == INT:
            value = self.token.lexeme
            self.eat()
            return Integer(int(value))
        elif self.token.category == NAME:
            value = self.token.lexeme
            self.eat()
            return Name(value, ctx=NameCtx.LOAD)
        elif self.token.category == LPAREN:
            self.eat()
            expr = self.parse_expr()
            self.eat_expecting(RPAREN)
            return expr
        else:
            raise SyntaxError("Expecting factor")
