import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__))))  # noqa

import pytest

from oops_parser import parse
from oops_parser.libs.parsy import ParseError


def test_parse():
    code = '''
($x on $y)
($y left_of $z)
-{($z color red)
  ($z on $w)
  -{($z color red)
    ($z on $y)}}
    '''
    ast = parse(code)
    assert '$x.on == $y AND $y.left_of == $z AND NOT ($z.color == red AND $z.on == $w AND NOT ($z.color == red AND $z.on == $y))' == str(ast)  # noqa


def test_parse_error():
    code = '''
($x on table
    '''
    with pytest.raises(ParseError):
        parse(code)


def test_nega():
    code = '''
($x on table)
-($x color red)
'''
    ast = parse(code)
    assert '$x.on == table AND $x.color != red' == str(ast)
