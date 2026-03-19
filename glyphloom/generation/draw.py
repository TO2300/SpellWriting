# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:23:40 2026

@author: trent
"""
import typing

import matplotlib.pyplot as plt

from glyphloom.generation import data, geometry


class Glyph:
    
    def __init__(self,
                 spelldata: data.SpellData = None,
                 leylines: geometry.Leylines = None) -> typing.Self:
    
        self.spelldata = spelldata
        if leylines:
            self.leylines = leylines
        else:
            self.leylines = geometry.Leylines(
                geometry.Founts(n=len(spelldata.collect_attributes())))
        
    
    def draw(self, legend: bool = False, legend_kwargs: dict = {}):
        # TODO: Add thematic colors
        plt.figure()
        cmap = plt.get_cmap('tab10')
        
        
        for attr in self.spelldata.collect_attributes().values():
            if not attr.glyph: continue
            order = attr.order
            options = attr.options
            value = getattr(self.spelldata, attr.name)
            
            if value is None: continue
            index = list(options).index(value)
        
            binary = self.leylines.necklace[index]
            paths = self.leylines.default_curves[order, binary.astype(bool)]
            for i, path in enumerate(paths):
                if i:
                    plt.plot(*path, color=cmap.colors[order])
                else:
                    plt.plot(*path, color=cmap.colors[order], label=attr.name)
        plt.plot(*self.leylines.founts[:,1:], 'pk', fillstyle='bottom', markersize=8)
        plt.plot(*self.leylines.founts[:,0], 'pk', fillstyle='top', markersize=8)
        plt.title(self.spelldata.name)
        if legend:
            plt.legend(**legend_kwargs)
        plt.axis('off')
            
if __name__ == '__main__':
    from glyphloom.data.fifth_edition import SpellData_5e
    
    spelldata = SpellData_5e.get_spell('Fireball')
    leylines = geometry.Leylines(geometry.Founts(n_points=13),
                                 expression='exponential')
    Glyph(spelldata, leylines).draw()