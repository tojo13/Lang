from python.token import *


class IndentStack:
    def __init__(self):
        self.indents = [0]

    def peek(self):
        return self.indents[-1]

    def pop(self):
        if len(self.indents) == 1:
            raise IndentationError("Can not dedent from no indent.")
        return self.indents.pop()

    def push(self, num_spaces):
        self.indents.append(num_spaces)


class Lexer:
    def __init__(self, src):
        self.src = src
        self.tokens = []

        self.pos = -1
        self.line = 0
        self.col = -1

        self.indent_stack = IndentStack()

        self.cur_char = None

    def lex(self):
        self.eat()
        while self.cur_char is not None:
            if self.col == 0:
                self.eat_indentation()

            if self.cur_char in " \t":
                self.eat()
            elif self.cur_char.isalpha() or self.cur_char == "_":
                self.eat_identifier()
            elif self.cur_char.isdigit():
                self.eat_int()
            elif self.cur_char == "\n":
                newline = Token(self.line, self.col, NEWLINE, self.cur_char)
                self.tokens.append(newline)
                self.line += 1
                self.col = -1
                self.eat()
            elif self.cur_char == ":":
                colon = Token(self.line, self.col, COLON, self.cur_char)
                self.tokens.append(colon)
                self.eat()
            elif self.cur_char == "(":
                lparen = Token(self.line, self.col, LPAREN, self.cur_char)
                self.tokens.append(lparen)
                self.eat()
            elif self.cur_char == ")":
                rparen = Token(self.line, self.col, RPAREN, self.cur_char)
                self.tokens.append(rparen)
                self.eat()
            elif self.cur_char == "*":
                times = Token(self.line, self.col, TIMES, self.cur_char)
                self.tokens.append(times)
                self.eat()
            elif self.cur_char == "/":
                div = Token(self.line, self.col, DIV, self.cur_char)
                self.tokens.append(div)
                self.eat()
            elif self.cur_char == "+":
                plus = Token(self.line, self.col, PLUS, self.cur_char)
                self.tokens.append(plus)
                self.eat()
            elif self.cur_char == "-":
                minus = Token(self.line, self.col, MINUS, self.cur_char)
                self.tokens.append(minus)
                self.eat()
            elif self.cur_char == "=":
                start_line = self.line
                start_col = self.col
                start_char = self.cur_char
                self.eat()
                if self.cur_char == "=":
                    eeq = Token(start_line, start_col, EEQ, start_char + self.cur_char)
                    self.tokens.append(eeq)
                    self.eat()
                else:
                    eq = Token(start_line, start_col, EQ, start_char)
                    self.tokens.append(eq)
            elif self.cur_char == "!":
                start_line = self.line
                start_col = self.col
                start_char = self.cur_char
                self.eat()
                if self.cur_char == "=":
                    neq = Token(start_line, start_col, NEQ, start_char + self.cur_char)
                    self.tokens.append(neq)
                    self.eat()
                else:
                    error = Token(start_line, start_col, error, start_char)
                    self.tokens.append(error)
            elif self.cur_char == "<":
                start_line = self.line
                start_col = self.col
                start_char = self.cur_char
                self.eat()
                if self.cur_char == "=":
                    leq = Token(start_line, start_col, LEQ, start_char + self.cur_char)
                    self.tokens.append(geq)
                    self.eat()
                else:
                    lt = Token(start_line, start_col, LT, start_char)
                    self.tokens.append(lt)
            elif self.cur_char == ">":
                start_line = self.line
                start_col = self.col
                start_char = self.cur_char
                self.eat()
                if self.cur_char == "=":
                    geq = Token(start_line, start_col, GEQ, start_char + self.cur_char)
                    self.tokens.append(geq)
                    self.eat()
                else:
                    gt = Token(start_line, start_col, GT, start_char)
                    self.tokens.append(gt)
            elif self.cur_char in "'\"":
                self.eat_string(self.cur_char)
            else:
                error = Token(self.line, self.col, ERROR, self.cur_char)
                self.tokens.append(error)
                self.eat()

        while self.indent_stack.peek() > 0:
            self.indent_stack.pop()
            dedent = Token(self.line, self.col, DEDENT, None)
            self.tokens.append(dedent)

        eof = Token(self.line, self.col, EOF, "")
        self.tokens.append(eof)
        return self.tokens

    # TODO comments
    # TODO floats

    def eat_indentation(self):
        num_spaces = 0
        while self.cur_char in " \t":
            num_spaces += 1
            self.eat()
        if num_spaces > self.indent_stack.peek():
            self.indent_stack.push(num_spaces)
            indent = Token(self.line, 0, INDENT, None)
            self.tokens.append(indent)
        elif num_spaces < self.indent_stack.peek():
            while self.indent_stack.peek() != num_spaces:
                try:
                    self.indent_stack.pop()
                except IndentationError:
                    print(f"Indentation error on line: {self.line}")
                    exit()
                dedent = Token(self.line, 0, DEDENT, None)
                self.tokens.append(dedent)

    def eat_string(self, start_char):
        # TODO: handle string with escapes
        start_line = self.line
        start_col = self.col
        literal = ""
        self.eat()
        while self.cur_char is not None and self.cur_char != start_char:
            literal += self.cur_char
            self.eat()
        string = Token(start_line, start_col, STR, literal)
        self.tokens.append(string)
        self.eat()

    def eat_identifier(self):
        ident = self.cur_char
        start_col = self.col
        self.eat()
        while self.cur_char is not None and (
            self.cur_char.isalpha() or self.cur_char == "_"
        ):
            ident += self.cur_char
            self.eat()
        if ident in keywords:
            keyword = Token(self.line, start_col, keywords[ident], ident)
            self.tokens.append(keyword)
        else:
            name = Token(self.line, start_col, NAME, ident)
            self.tokens.append(name)

    def eat_int(self):
        integer = self.cur_char
        start_col = self.col
        self.eat()
        while self.cur_char is not None and self.cur_char.isdigit():
            integer += self.cur_char
            self.eat()
        int_tkn = Token(self.line, start_col, INT, integer)
        self.tokens.append(int_tkn)

    def eat(self):
        self.pos += 1
        self.col += 1
        if self.pos < len(self.src):
            self.cur_char = self.src[self.pos]
        else:
            self.cur_char = None
