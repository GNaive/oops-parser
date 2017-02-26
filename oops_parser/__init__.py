import re
from oops_parser.libs.parsy import string, regex, generate, r


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


class Has(object):
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


class Nega(Has):
    def __str__(self):
        return '%s.%s != %s' % (self.id, self.attr, self.value)

    def get_result(self, ctx):
        return not super(Nega, self).get_result(ctx)


whitespace = regex(r'\s*', re.MULTILINE)


def lexeme(p):
    return p << whitespace


lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
lbrack = lexeme(string('('))
rbrack = lexeme(string(')'))
negtive = lexeme(string('-'))

re_var_name = r'[a-zA-Z_][a-zA-Z0-9_]*'

id = lexeme(regex(r'\$' + re_var_name))
attr = lexeme(regex(re_var_name))
value = lexeme(regex(re_var_name))


@generate
def has():
    yield lbrack
    _id = yield id
    _attr = yield attr
    _value = yield id | value
    yield rbrack
    r(Has(_id, _attr, _value))


@generate
def nega():
    yield negtive
    _has = yield has
    r(Nega(_has.id, _has.attr, _has.value))


@generate
def al():
    yield lbrace
    _l = yield (whitespace >> (has | nega | al | nal)).many()
    yield rbrace
    r(AL(_l))


@generate
def nal():
    yield negtive
    _l = yield al
    r(NAL(_l))


oops = whitespace >> (
    has | nega | al | nal
)


def parse(code):
    return oops.parse('{%s}' % code)
