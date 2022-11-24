#!/usr/bin/env python

from lark import Lark, Transformer

class TypeTransformer(Transformer):
    def type(self, value):
        return {'name': value[1], 'def': value[0]}

    def type_def(self, value):
        return str(value[0])

    def type_name(self, value):
        return str(value[0])


class FunctionTransformer(Transformer):
    out = {'args': [], 'varargs': False}

    def function(self, value):
        ret = self.out.copy()
        self.out = {'args': [], 'varargs': False}

        return ret
    
    def name(self, value):
        self.out['name'] = str(value[0])

    def return_type(self, value):
        self.out['return_type'] = str(value[0])

    def varargs(self, value):
        self.out['varargs'] = True

    def args(self, value):
        if self.out['varargs']:
            value = value[:-1]

        self.out['args'] = value

    def arg(self, value):
        if len(value) == 2:
            return {'attrs': [],
                    'type': value[0],
                    'name': value[1]}
        
        else:
            return {'attrs': value[0],
                    'type': value[1],
                    'name': value[2]}

    def arg_type(self, value):
        return str(value[0])
    
    def arg_name(self, value):
        return str(value[0])
    
    def attrs(self, value):
        return value

    def attr(self, value):
        return {'name': str(value[0]), 'params': value[1:]}
    
    def attr_params(self, value):
        return value[0]

    def attr_param(self, value):
        if len(value) == 1:
            return {'name': str(value[0])}

        else:
            return {'name': str(value[0]), 'value': str(value[1])}


with open('grammar.lark') as f:
    grammar = f.read()

function_parser = Lark(grammar, parser='lalr', transformer=FunctionTransformer(), start="function")
type_parser = Lark(grammar, parser='lalr', transformer=TypeTransformer(), start="type")

parse_function = lambda s: function_parser.parse(s)
parse_type = lambda s: type_parser.parse(s)