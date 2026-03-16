# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:33:40 2026

@author: trent
"""

from types import MappingProxyType
import typing
import re
import copy

import numpy as np
import matplotlib.pyplot as plt

#---------File for defining spell bases----------#
# every base must haave an input of n and return (x,y)

class Founts:
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
                     'cw'),
        'golden' : tuple()})
  
    #---- Numpy overrides
    def __iter__(self):
        return iter(self.nodes)
    
    def __array__(self, dtype=None, copy=False):
        founts = self.nodes
        if dtype:
            founts = founts.astype(dtype)
        if copy:
            founts = founts.copy()
        return founts
    
    @property
    def shape(self):
        return self.nodes.shape
    
    @property
    def T(self):
        new = copy.deepcopy(self)
        new.founts = new.founts.T
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
                cw: bool = True,
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
<<<<<<< HEAD
            The default is 2*np.pi/n_points.
=======
            The default is np.pi/n_points.
>>>>>>> e5fbb8165d4cf9a63b0443b319e2065e5906b8d8
        cw: bool, optional
            Clockwise flag for vertex order, the default is True

        Returns
        -------
        Founts

        """
        if start_angle is None:
            start_angle = 2*np.pi/n_points
        print(f'{cw=:} {start_angle=:}')
        
        # CCW Generation
        if cw:
            angles = start_angle + np.linspace(2*np.pi, 0, n_points, endpoint=False)
        else:
            angles = np.linspace(0, 2*np.pi, n_points, endpoint=False) - start_angle
        
        xs = radius*np.cos(angles)
        ys = radius*np.sin(angles)
<<<<<<< HEAD
=======
        
        if cw:
            xs = xs[::-1]
            ys = ys[::-1]
>>>>>>> e5fbb8165d4cf9a63b0443b319e2065e5906b8d8
            
        kwargs.pop('nodes', None)
        kwargs.pop('expression', None)
        kwargs.pop('domain_min', None)
        kwargs.pop('domain_max', None)
            
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
        
        kwargs.pop('nodes', None)
        kwargs.pop('expression', None)
        
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
    return np.array(uniques)


class Leylines:
    
    SAFE_MATH = MappingProxyType({
        k: getattr(np, k) for k in ["sin", "cos", "tan", "arcsin", "arccos", 
                                    "arctan", "sinh", "cosh", "tanh", "exp", 
                                    "log", "log10", "sqrt", "abs", "fabs",
                                    "floor", "ceil", "pi", "e"]
        })
    
    PREDEFINED = MappingProxyType({
        'linear' : ('domain', '0*domain'),
        'centre-circle' : ('cos(pi*domain)', 'sin(pi*domain)'),
        'non-centre-circle' : ('b + r*cos(theta0 + domain*((theta1-theta0) % (2*pi)))',
                               'b + r*sin(theta0 + domain*((theta1-theta0) % (2*pi)))'),
        'exponential' : ('domain', 
                         '(exp(10 * domain) - 1) / (exp(10 * domain_max) - 1)'),
        'inverse-exponential': (
            'domain', 
            '-(exp(12 * domain) - 1) / (exp(12 * domain_max) - 1)'),
        })
    PREFEDEFINED_KWARGS = MappingProxyType({
        'non-centre-circle' : {'b' : 0,
                               'r' : 1,
                               'theta0' : 0,
                               'theta1' : 2*np.pi/3}
        })
    
    def __init__(self, 
                 founts: Founts = Founts(),
                 expression: str | tuple[str] = ('domain', '0*domain'),
                 domain_min: float = 0,
                 domain_max: float = 1,
                 resolution: int = 20,
                 **kwargs) -> typing.Self:
        
        n = founts.shape[1]
        self.founts = founts
        # Use numpy array to preserve fancy indexing later
        # (6, 13, 2) is default where 6 orders, 13 founts, and node pairs
        self.line_pairings = np.array([
            [(i, (i + order + 1) % n) for i in range(n)]
            for order in range(int((n-1)/2))])
        self.domain_min = domain_min
        self.domain_max = domain_max
        self.resolution = resolution
        self.kwargs = kwargs
        self.expression = expression
        self.necklace = generate_necklace(n)
    
    
    @property
    def expression(self) -> str | tuple[str]:
        return self._expression
    
    @expression.setter
    def expression(self, expression: str | tuple[str]):
        if isinstance(expression, str) and expression in self.PREDEFINED:
            override = self.PREFEDEFINED_KWARGS.get(expression, {}).copy()
            for key in self.kwargs:
                if key in override:
                    override[key] = self.kwargs[key]
            self.kwargs.update(override)
            expression = self.PREDEFINED[expression]
            
        elif isinstance(expression, str):
            expression = (expression, '0*domain')
        self._expression = expression
        self.default_curves = self.generate_curves()
        return        
        
    def _eval_parametric(self, samples: int = None) -> np.ndarray:
        if samples is None:
            samples = self.resolution
        domain = np.linspace(self.domain_min, self.domain_max, samples)
        # Parametric function
        env = {'__builtins__': {}, 
               **self.SAFE_MATH, 
               'domain': domain, 
               **self.__dict__,
               **self.kwargs}
        xs = eval(self.expression[0], env)
        ys = eval(self.expression[1], env)
        curve = np.array([xs, ys])
        return curve
    
    def _eval_expression(self, samples: int = None) -> np.ndarray:
        if samples is None:
            samples = self.resolution
        
        domain = np.linspace(self.domain_min, self.domain_max, samples)
        if isinstance(self.expression, str):
            # Simple Function
            env = {'__builtins__': {}, 
                   **self.SAFE_MATH, 
                   'domain': domain}
            ys = eval(self.expression, env)
            curve = np.array([domain, ys])
        else:
            curve = self._eval_parametric(samples)
            
        return curve
    
    def _normalize_curve(self, curve: np.ndarray) -> np.ndarray:
        """
        Normalizes a curve of n-many samples to the domain [0,1]

        """
        # Shift to start at 0
        curve = curve.copy()
        curve = curve - curve[:, [0]]
        
        # Rotate to basis vector
        dx, dy = curve[0, -1], curve[1, -1]
        angle = -np.arctan2(dy, dx)
        R = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle),  np.cos(angle)]
        ])
        curve = R @ curve
        
        # Normalize to magnitude 1
        curve /= curve[0, -1]

        return curve
    
    def _transform_to_segment(self, 
                              curve: np.ndarray, 
                              P: np.ndarray, 
                              Q: np.ndarray) -> np.ndarray:
        """
        Transforms a normalized curve between two points P and Q

        Parameters
        ----------
        curve : np.ndarray
            Normalized curve - domain[0,1].
        P : np.ndarray
            1x2 array representing ordered pair in x-y coordinate plane.
        Q : np.ndarray
            1x2 array representing ordered pair in x-y coordinate plane.

        Returns
        -------
        curve : np.ndarray
            Curve scaled and rotated to connect P to Q.

        """
        dx = Q[0] - P[0]
        dy = Q[1] - P[1]
        length = np.hypot(dx, dy)
        angle = np.arctan2(dy, dx)

        # Scale
        curve = curve * length

        # Rotate
        R = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle),  np.cos(angle)]
        ])
        curve = R @ curve

        # Translate
        curve = curve + P[:, None]

        return curve

    def generate_curves(self, samples: int = None) -> np.ndarray:
        """
        Generates a Order x Node Count x Ordered Pair x Samples array for every
        possible combination of founts in the self.nodes object evaluated using
        the provided expression.

        Parameters
        ----------
        samples : int, optional
            Number of points to resolve in the curve. The default is self.resolution.

        Returns
        -------
        curves : np.ndarray
            Array of all potential curves given the parameters.

        """
        
        if samples is None:
            samples = self.resolution
        
        raw_curve = self._eval_expression(samples)
        normal = self._normalize_curve(raw_curve.copy())
        curves = np.zeros((*self.line_pairings.shape,samples), dtype=np.float64)
        
        for order in range(curves.shape[0]):
            for index in range(curves.shape[1]):
                a,b = self.line_pairings[order, index] # indices of founts
                
                P = self.founts[:,a] 
                Q = self.founts[:,b]
                

                
                curve = self._transform_to_segment(normal.copy(), P, Q)
                
                # print(f"{P} -> {Q}\n{curve}\n\n")
                curves[order, index] = curve.astype(np.float64)
    
        return curves
    
    def preview(self):
        plt.figure()
        cmap = plt.get_cmap('tab20')
        for order, order_array in enumerate(self.default_curves):
            for diff, coords in enumerate(order_array):
                plt.plot(*coords, color=cmap.colors[order])
        
        plt.plot(*self.nodes, 'bo')
        plt.plot(*self.nodes[:,0], 'ro')