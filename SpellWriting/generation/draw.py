# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:23:40 2026

@author: trent
"""
import typing

import matplotlib.pyplot as plt

from SpellWriting.generation import data, geometry
from SpellWriting.data.fifth_edition import SpellData_5e


class Glyph:
    
    def __init__(self,
                 spelldata: data.SpellData = SpellData_5e.get_spell('Fireball'),
                 geometry_override: geometry.Leylines = None) -> typing.Self:
    
        self.spelldata = spelldata
        if geometry_override:
            self.leylines = geometry_override
        else:
            self.leylines = geometry.Leylines(
                geometry.Founts(n=len(spelldata.collect_attributes())))
        
    
    def plot(self):
        plt.figure()
        cmap = plt.get_cmap('tab20')
        
        
        for attr in self.spelldata.collect_attributes().values():
            if not attr.glyph: continue
            order = attr.order
            options = attr.options
            value = getattr(self.spelldata, attr.name)
            
            index = list(options).index(value)
        
            binary = self.leylines.necklace[index]
            paths = self.leylines.default_curves[order, binary.astype(bool)]
            for i, path in enumerate(paths):
                if i:
                    plt.plot(*path, color=cmap.colors[order])
                else:
                    plt.plot(*path, color=cmap.colors[order], label=attr.name)
        plt.plot(*self.leylines.founts, 'bo')
        plt.plot(*self.leylines.founts[:,0], 'ro')
        plt.title(self.spelldata.name)
        plt.legend()