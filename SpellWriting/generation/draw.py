# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:33:40 2026

@author: trent
"""

from types import MappingProxyType
import typing
import re
import copy
import itertools

import numpy as np

#---------File for defining spell bases----------#
# every base must haave an input of n and return (x,y)

class Nodes:
    """
    Generic method for generating the n and k possible lines given some 
    generative input.
    
    """
    SAFE_MATH = MappingProxyType({
        k: getattr(np, k) for k in ["sin", "cos", "tan", "arcsin", "arccos", 
                                    "arctan", "sinh", "cosh", "tanh", "exp", 
                                    "log", "log10", "sqrt", "abs", "fabs",
                                    "floor", "ceil", "pi", "e"]
        })
    PREDEFINED = MappingProxyType({
        'polygon' : ('radius', 
                     'start_angle',
                     'ccw'),
        'golden' : tuple()})
  
    #---- Numpy overrides
    def __iter__(self):
        return iter(self.nodes)
    
    def __array__(self, dtype=None, copy=False):
        nodes = self.nodes
        if dtype:
            nodes = nodes.astype(dtype)
        if copy:
            nodes = nodes.copy()
        return nodes
    
    @property
    def shape(self):
        return self.nodes.shape
    
    @property
    def T(self):
        new = copy.deepcopy(self)
        new.nodes = new.nodes.T
        return new
    
    def __getitem__(self, item):
        if isinstance(item, typing.Iterable):
            return self.nodes[*item]
        return self.nodes[item]
    
    def __init__(self, 
                 nodes: np.ndarray = None,
                 n_points: int = 13,
                 expression: str | tuple[str] = None,
                 domain_min: float = -1,
                 domain_max: float = 1,
                 **kwargs):
        
        self.nodes = nodes
        self.n_points = n_points
        self.expression = expression
        self.domain_min = domain_min
        self.domain_max = domain_max
        self.kwargs = kwargs
        
        if nodes is None and not expression:
            self.nodes = type(self).polygon().nodes
            return
        
        if nodes is not None:
            self.nodes = np.array([*nodes])
            return
        
        if isinstance(expression, str) and expression not in self.PREDEFINED:
            # Simple Function
            domain = np.linspace(domain_min, domain_max, n_points)
            env = {'__builtins__': {}, 
                   **self.SAFE_MATH, 
                   'domain': domain}
            ys = eval(expression, env)
            self.nodes = np.array([domain, ys])
            return
        elif isinstance(expression, str) and expression in self.PREDEFINED:
            func = getattr(type(self), expression, lambda *args, **kwargs: f'No function {expression}')
            res = func(nodes=nodes, n_points=n_points, expression=expression,
                       domain_min=domain_min, domain_max=domain_max, **kwargs)
            if isinstance(res, type(self)):
                self.nodes = res.nodes
            else:
                raise NotImplementedError(f"No predefined shape function for '{expression}'")
                
        elif isinstance(expression, tuple) and len(expression) == 2:
            # Parametric function
            domain = np.linspace(domain_min, domain_max, n_points)
            env = {'__builtins__': {}, **self.SAFE_MATH, 'domain': domain}
            xs = eval(expression[0], env)
            ys = eval(expression[1], env)
            self.nodes = np.array([xs, ys])
            return
    
    def __repr__(self):
        arg = [f'{attr_name}={getattr(self, attr_name)}' 
               for attr_name in list(getattr(self, '__dict__', {})) 
               if not re.search('__.*__', attr_name)]
        arg_str = ', '.join(arg)
        return f'{type(self).__name__}({arg_str})'
    
    @classmethod
    def polygon(cls, 
                n_points: int = 13,
                radius: float = 1,
                start_angle:float = None,
                ccw: bool = False,
                **kwargs) -> typing.Self:
        """
        Default polygon generation, equivalent to 
        
        expression = ('radius*cos(start_angle + 2*pi/n_points)',
                      'radius*sin(start_angle + 2*pi/n_points)')
        where radius would be a float
              start_angle is a float
              n_points is an integer

        Parameters
        ----------
        n_points : int, optional
            Number of vertices. The default is 13.
        radius : float, optional
            Radius of the inscribed circle. The default is 1.
        start_angle : float, optional
            Angle from the circle's center to its first vertex. 
            The default is np.pi/n_points.
        ccw: bool, optional
            Counter clockwise flag for vertex order, the default is True

        Returns
        -------
        Nodes

        """
        if start_angle is None:
            start_angle = np.pi/n_points
        
        angles = start_angle + np.linspace(0, 2*np.pi, n_points, endpoint=False)
        xs = radius*np.cos(angles)
        ys = radius*np.sin(angles)
        
        if ccw:
            xs = xs[::-1]
            ys = ys[::-1]
            
        kwargs.pop('nodes')
        kwargs.pop('expression')
        kwargs.pop('domain_min')
        kwargs.pop('domain_max')
            
        return cls(nodes=np.array([xs, ys]), 
                   expression='polygon',
                   domain_min=-np.abs(radius),
                   domain_max=np.abs(radius),
                   **kwargs)
    
    @classmethod
    def golden(cls,
               n_points: int = 13,
               domain_max: float = 3*np.pi,
               **kwargs) -> typing.Self:
        domain = np.linspace(0, domain_max, n_points)
        
        g  = (1 + 5 ** 0.5) / 2 #golden ratio
        f = g**(domain*g/(2*np.pi)) #factor
        xs = np.cos(domain)*f
        ys = np.sin(domain)*f
        
        kwargs.pop('nodes')
        kwargs.pop('expression')
        
        return cls(nodes=np.array([xs,ys]),
                   domain_max=domain_max,
                   expression='golden',
                   **kwargs)


def binary_strings_to_list(all_binaries):
    final_output = [[int(b) for b in list(ab)] for ab in all_binaries]
    return(final_output)

def generate_necklace(n = 13):

    #stolen from https://github.com/Ernesti04/necklace_projects/blob/main/necklace_gen_v2.py
    x = 1						# start at 1, avoid all 0s case
    uniques = ["".join(["0"]*n)]
    while (x < 2**n): 			# for each possible number
        s = str(bin(x)[2:].zfill(n)) 	# get binary of number
        cycle = [] 				# get blank list to check rotations
        for i in range(len(s)-1): 	# for each bit in the sequence
            #rot = cycle[i][-1] + cycle[i][:-1] #slightly slower
            rot = s[i:] + s[:i] 		# rotate by i bits
            cycle.append(rot) 		# add each rotation
            if rot < s : 				# if rotation found that is smaller
                break 				# stop searching
        if min(cycle) == s : 		# if the number is already minimum
            uniques.append(s) 		# add to the list
            #print(f'\t{s}') # print results (slow)
        x += 2 					# count odds, halves time
    uniques = binary_strings_to_list(uniques)
    return(uniques)


class Edges:
    
    SAFE_MATH = MappingProxyType({
        k: getattr(np, k) for k in ["sin", "cos", "tan", "arcsin", "arccos", 
                                    "arctan", "sinh", "cosh", "tanh", "exp", 
                                    "log", "log10", "sqrt", "abs", "fabs",
                                    "floor", "ceil", "pi", "e"]
        })
    
    PREDEFINED = MappingProxyType({})
    
    def __init__(self, 
                 nodes: Nodes,
                 expression: str = 'line', # Simple or predefined only, no parametric
                 resolution: int = 20) -> typing.Self:
        
        self.nodes = nodes
        self.x_coords = nodes[0]
        self.y_coords = nodes[1]
        
        self.necklace = generate_necklace(nodes.shape[1])
        
        # Use numpy array to preserve fancy indexing later
        n = nodes.shape[1]
        # (6, 13, 2) is default where 6 orders, 13 nodes, and node pairs
        self.line_pairings = np.array([
            [(i, (i + order) % n) for i in range(13)]
            for order in range(int((n-1)/2))])
    
        