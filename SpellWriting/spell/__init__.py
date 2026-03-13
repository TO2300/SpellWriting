# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 17:01:51 2026

@author: trent
"""
import typing
from types import MappingProxyType
import re
import inspect
import sys

import numpy as np

from SpellWriting.attributes import SpellAttributes_5e
from SpellWriting.generation import SpellShape, Necklace




class SpellAttribute:
    
    def __init__(self, 
                 order: int,
                 options: typing.Iterable,
                 default: typing.Any = None,
                 notation: bool = True):
        assert not isinstance(options, str)
        
        self.order = order
        self.options = tuple(options)
        self.default = options[0] if default is None else default
        self.notation = notation
        self.name = None
    
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
                f'notation={self.notation})')
    

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
        src = f'def __init__(self, {param_str}):\n\t{body}'
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
                   for name in dir(target)
                   if isinstance(getattr(target, name), SpellAttribute)}
        return options
    
    
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

@spelldata
class SpellData_5e:
    """
    Data container for Spell information
    
    """
       
    level = SpellAttribute(0, SpellAttributes_5e.Level)
    school = SpellAttribute(1, SpellAttributes_5e.School)
    damage_type = SpellAttribute(2, SpellAttributes_5e.DamageType)
    area_of_effect = SpellAttribute(3, SpellAttributes_5e.AreaOfEffect)
    range = SpellAttribute(4, SpellAttributes_5e.Range)
    duration = SpellAttribute(5, SpellAttributes_5e.Duration)
    concentration = SpellAttribute(-1, [True, False], notation=False)
    ritual = SpellAttribute(-1, [True, False], notation=False)
    
    def __str__(self):
        return f'<SpellData: {self.name}>'


class SpellNotationConfiguration:
    """
    Data container for Spell Notation configuration
    
    """
    
    node_count: int = 13
    node_shape: typing.Literal[*SpellShape.Node] | int = 'Polygon'
    node_shape_parameters: dict = MappingProxyType(dict(n=13))
    edge_shape : typing.Literal[*SpellShape.Edge] | int = 'Linear'
    edge_thetas : str = ''
    
    def __init__(self, *args, **kwargs) -> typing.Self:
        super().__init__(*args, **kwargs)
        
        self._necklace = Necklace(13)
        self._nodes = np.array(
            SpellShape.Node[self.node_shape](**self.node_shape_parameters))
        
        
    def __str__(self):
        return f'<SpellNotationConfiguration: {self.node_count}>'
            
    
    
    

class SpellNotation:
    """
    Functional organization for generating spells
    
    """
    
    def __init__(self, 
                 spell_data:SpellData = SpellData_5e(''),
                 spell_shape:SpellNotationConfiguration = SpellNotationConfiguration()
                 ) -> typing.Self:
        self.data = spell_data
        self.shape = spell_shape
        
        self.build_edges()
    
    def build_edges(self):
        self._edges = []
        
        
# %% Helpers
    