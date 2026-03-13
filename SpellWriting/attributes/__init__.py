# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 20:47:22 2026

@author: trent
"""
from pathlib import Path

from SpellWriting.abstract import IterEnum          

ROOT = Path(__file__).parent.absolute()

ordering = {}
for file in ROOT.glob('*.txt'):
    name = ''.join(map(str.capitalize, file.stem.split('_'))).rstrip('s')
    with open(file, 'r') as fid:
        lines = fid.read().split('\n')
        while '' in lines:
            lines.remove('')
        if 'None' in lines:
            idx = lines.index('None')
            lines[idx] = None
        ordering[name] = lines

SpellAttributes_5e = IterEnum('SpellAttributes', ordering)