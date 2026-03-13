#
import inspect

from SpellWriting.generation import edge, node, necklace
from SpellWriting.abstract import IterEnum

def _get_functions(module): 
    ordering = {}
    for name, func in inspect.getmembers(module, inspect.isfunction):
        name = ''.join(map(str.capitalize, name.split('_'))).rstrip('s')
        ordering[name] = func
    return ordering

SpellShape = IterEnum('SpellShape', 
                      {'Node' : _get_functions(node),
                       'Edge' : _get_functions(edge)})
Necklace = necklace.generate_binary_necklace