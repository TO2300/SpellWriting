# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 21:46:26 2026

@author: trent
"""
import typing
import re
import sys
from itertools import product, combinations, chain

import yaml
import numpy as np

def powerset(iterable: typing.Iterable, max_r: int = 3) -> list:
    """
    Generates the powerset of sequence

    """
    sequence = list(iterable)
    result = chain.from_iterable(combinations(sequence, r)
                                 for r in range(max_r+1))
    return list(result)
    

class SpellAttribute:
    
    def __init__(self, 
                 order: int,
                 options: typing.Iterable,
                 default: typing.Any = None,
                 glyph: bool = True):
        assert not isinstance(options, str)
        
        self.order = order
        self.options = options
        if isinstance(options, dict):
            self.default = None
        else:
            self.default = options[0] if default is None else default
        self.glyph = glyph
        self.name = None
        self.value = None
            
    def __set_name__(self, owner, name):
        self.name = name
        return
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    
    def __repr__(self) -> str:
        return (f'SpellAttribute('
                f'order={self.order}, options={self.options}, '
                f'glyph={self.glyph})')
    
    def __str__(self) -> str:
        return f'<{self.name}-SpellAttribute = {self.value}>'
    

class SpellData:
    """
    Generic data container for n-attribute defined spells
    
    """
    
    def __init_subclass__(cls, **kwargs):
        attributes = cls.collect_attributes(cls)
        fields = []
        for name, value in attributes.items():
            type_hint = typing.Literal[*value.options]
            default = value.default
            fields.append((name, type_hint, default))
            
        #---- Define __init__
        params = ['name:str = ""']
        body_data = ['self.name = name']
        for name, tp, default in fields:
            search = re.search("<class '(.*)'>", str(tp))
            if search:
                tp = (search.group(1))
            if default is ...:
                params.append(f'{name}:{tp}')
            else:
                params.append(f'{name}:{tp} = {default}')
            body_data.append(f'self.{name} = {name}')
            
        
        param_str = ', '.join(params)
        body = '\n\t'.join(body_data)
        src = f'def __init__(self, {param_str}, **kwargs):\n\t{body}'
        module = sys.modules[cls.__module__]
        namespace = module.__dict__.copy()
        exec(src, namespace)
        setattr(cls, '__init__', namespace['__init__'])

        return
    
    @classmethod
    def collect_attributes(cls, target:type = None) -> dict[str, SpellAttribute]:
        if target is None:
            target = cls
        options = {name: getattr(target, name) 
                   for name in target.__dict__.keys()
                   if isinstance(getattr(target, name), SpellAttribute)}
        return options
    
    @classmethod
    def from_yaml(cls, yaml_filepath: str) -> type:
        with open(yaml_filepath, 'r') as fid:
            data = yaml.safe_load(fid)
            
        config = data['SpellDataConfig']
        name = config['name']
        class_name = f'SpellData_{name}'
        class_map = {'system' : name}
        for i, (attribute, attr_data) in enumerate(config['attributes'].items()):
            option_type = attr_data['option_type']
            options = attr_data['options']
            if option_type == 'range':
                options = tuple(range(*options))
            elif option_type == 'map':
                option_list = []
                for key, value in options.items():
                    if any(isinstance(i, list) for i in value):
                        # Nested
                        value = list(product(*value))
                        option_list.extend(list(map(
                            lambda t: f'{key} {str(t)}',
                            value)))
                    else:
                        option_list.extend(list(map(
                            lambda t: f'{key} ({str(t)})',
                            value)))
                options = option_list
            elif option_type == 'powerset':
                power_set = powerset(options)
                if 'None' in options:
                    options = ['None', *[opt[0] if len(opt) == 1 else opt 
                                         for opt in power_set
                                         if 'None' not in opt and opt]]
                else:
                    options = power_set
                
                
            default = attr_data['default']
            glyph = attr_data.get('glyph', True)
            attr = SpellAttribute(i, options, default=default, glyph=glyph)
            setattr(attr, 'name', attribute)
            class_map[attribute] = attr
        
        target = type(class_name, (SpellData,), class_map)
        
        return target
    
    @classmethod
    def yaml_spell(cls, yaml_file:str) -> typing.Self:
        with open(yaml_file, 'r') as fid:
            data = yaml.safe_load(fid)
        if data['system'] != cls.system:
            return None
        return cls(**data)
    
    def draw(self, nodes: np.ndarray):
        attributes = self.collect_attributes()
        
        
        return
    
    
    def __repr__(self):
        arg = [f'{attr_name}={getattr(self, attr_name)}' 
               for attr_name in list(getattr(self, '__dict__', {})) 
               if not re.search('__.*__', attr_name)]
        arg_str = ', '.join(arg)
        return f'{type(self).__name__}({arg_str})'
    

def spelldata(target:type) -> SpellData:
    new_class = type(target.__name__, 
                     (SpellData, target),
                     {})
    return new_class