oops-parser
============

[![Build Status](https://api.travis-ci.org/GNaive/oops-parser.svg?branch=master)](https://travis-ci.org/GNaive/oops-parser)

Oops parser! 🌊

```python
code = '''
($x on $y)
($y left_of $z)
  -{($z color red)
    ($z on $w)
    -{($z color red)
    ($z on $y)}}'''
tokens = tokenize(code)
ast = parse(tokens)
# >> $x.on == $y AND $y.left_of == $z AND NOT ($z.color == red AND $z.on == $w AND NOT ($z.color == red AND $z.on == $y))
print ast
# >> False
print execute_ast(ast, {
    '$x': Var(on=1),
    '$y': Var(left_on=1),
    '$z': Var(color=1, on=1),
    '$w': Var(),
    'red': 1
})
```
