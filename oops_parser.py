class State(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class AL(list):
    def __str__(self):
        return ' AND '.join(map(str, self))

    def get_result(self, ctx):
        return reduce(
            lambda p, c: p and c.get_result(ctx),
            self,
            True,
        )


class NAL(AL):
    def __str__(self):
        s = super(NAL, self).__str__()
        return 'NOT (%s)' % s

    def get_result(self, ctx):
        r = super(NAL, self).get_result(ctx)
        return not r


class Node(object):
    def __init__(self, id=None, attr=None, value=None):
        self.id = id
        self.attr = attr
        self.value = value

    def __str__(self):
        return '%s.%s == %s' % (self.id, self.attr, self.value)

    def get_result(self, ctx):
        id = ctx.get(self.id.value)
        left = getattr(id, self.attr.value)
        right = ctx.get(self, self.value.value)
        return left == right


class Token(object):
    def __init__(self, value, ln, cn):
        self.value = value
        self.ln = ln
        self.cn = cn

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        return self.value == other

    def __str__(self):
        return self.value


class Id(Token):
    pass


class Attr(Token):
    pass


class Value(Token):
    pass


def parse(code):
    return list(scan(code))


def scan(code):
    l = len(code)

    s = State(
        ln=0,
        cn=0,
        c=None,
        pc=None,
        bf=[],
        idx=0,
    )

    def raise_exception():
        raise Exception(
            'Parse Error!\nline number: %s, char number: %s' % (
                s.ln, s.cn
            )
        )

    def build_token(token_cls=None):
        token_cls = token_cls or get_token_cls()
        value = ''.join(s.bf)
        s.bf = []
        return token_cls(value, s.ln, s.cn - len(value))

    def get_token_cls():
        return [Id, Attr, Value][s.idx]

    for i in xrange(l):
        c = code[i]
        if i + 1 <= l - 1:
            nc = code[i + 1]
        else:
            nc = None
        s.c = c
        s.cn += 1

        if c == ' ':
            if s.bf:
                yield build_token()
                s.idx += 1
            s.pc = c
            continue
        elif c == '\n':
            s.ln += 1
            s.cn = 0
            s.pc = c
            continue
        elif c in {'(', ')', '-', '{', '}'}:
            if c == '-' and nc != '{':
                raise_exception()

            if s.bf:
                yield build_token()

            s.idx = 0
            s.bf.append(c)
            yield build_token(Token)
            s.pc = c
            continue

        s.bf.append(c)
        s.pc = c


def get_ast(tokens):
    if not tokens:
        return

    s = State(
        pt=None,
        rl=NAL() if tokens[0] == '-' else AL(),
        cl=None,
        cn=None
    )
    s.cl = s.rl

    for t in tokens:
        s.t = t
        if t == '(':
            s.cn = Node()
            s.cl.append(s.cn)
        elif t == '{':
            if s.pt == '-':
                l = NAL()
            else:
                l = AL()
            s.cl.append(l)
            s.cl = l
        elif isinstance(t, Id):
            s.cn.id = t
        elif isinstance(t, Attr):
            s.cn.attr = t
        elif isinstance(t, Value):
            s.cn.value = t

        s.pt = t
    return s.rl


def execute_ast(ast, ctx):
    return ast.get_result(ctx)


class Var(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if __name__ == '__main__':
    code = '''
($x on $y)
($y left_of $z)
-{($z color red)
  ($z on $w)
  -{($z color red)
    ($z on $y)}}'''
    tokens = parse(code)
    ast = get_ast(tokens)
    print ' '.join(map(str, tokens))
    print ast
    print execute_ast(ast, {
        '$x': Var(on=1),
        '$y': Var(left_on=1),
        '$z': Var(color=1, on=1),
        '$w': Var(),
        'red': 1
    })
