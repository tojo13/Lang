class ASTNode:
    pass


class Module(ASTNode):
    def __init__(self, stmts):
        self.stmts = stmts


class Assign(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr


class Pass(ASTNode):
    pass


class If(ASTNode):
    def __init__(self, test, body, or_else):
        self.test = test
        self.body = body
        self.or_else = or_else


class While(ASTNode):
    def __init__(self, test, body):
        self.test = test
        self.body = body


class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class BoolOp(ASTNode):
    """`a or b or c` has `op='or'` and `values=[a, b, c]`"""
    def __init__(self, op, values):
        self.op = op
        self.values = values


class Compare(ASTNode):
    def __init__(self, left, op, comparators):
        self.left = left
        self.op = op
        self.comparators = comparators


class ConstantKind:
    NONE = "None"
    STR = "str"
    INT = "int"
    FLOAT = "float"
    TRUE = "True"
    FALSE = "False"


class Constant(ASTNode):
    def __init__(self, value, kind):
        self.value = value
        self.kind = kind


class NameCtx:
    LOAD = "LOAD"
    STORE = "STORE"


class Name(ASTNode):
    def __init__(self, id, ctx):
        self.id = id
        self.ctx = ctx
