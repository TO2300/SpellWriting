"""Aim is to create a class that contains all the useful
functions a spell might need
    """
import matplotlib.pyplot as plt #There's almost certainly a better way than matplotlib but oh well
import numpy as np
from collections.abc import Callable
from necklaces import default_generation
import os
import bases

class custom_spell_input():
    """Class for custom inputting of spell data. Usually use the argparse object but this lets you do it in a code way
    """
    def __init__(self,
                 level,
                 school,
                damagetype,
                 aoe,
                 range,
                 duration,
                 concentration = False,
                 ritual = False):
        """Initialisation of class.

        Args:
            level (str): Spell level
            school (str): School of spell
            damagetype (str): Damage type of Spell
            aoe (str): Area of Effect of Spell
            range (str): Range of Spell
            duration (str): Duration of Spell
            concentration (bool, optional): bool for whether spell is concentration. Defaults to False.
            ritual (bool, optional): bool for whether spell is ritual. Defaults to False.
        """
        self.level = str(level).lower()
        self.school = school.lower()
        self.damagetype = damagetype.lower()
        self.aoe = aoe.lower()
        self.range = range.lower()
        self.duration = duration.lower()
        self.concentration = concentration
        self.ritual = ritual

class spell():
    def __init__(self,input_obj: custom_spell_input,base_fn:Callable,
                 txt_file_base:str = r"./attribute_ordering/",
                 n_att = None,
                 n_pol = None,
                 spell_name = "spell_class_default",
                 override_dict = {},
                 base_kwargs = []):
        self.__name__ = spell_name

        self.atts = ["level","school","damagetype",
                     "aoe","range","duration",
                     "concentration","ritual"]

        self.level = input_obj.level
        self.school = input_obj.school
        self.damagetype = input_obj.damagetype
        self.aoe = input_obj.aoe
        self.range = input_obj.range
        self.duration = input_obj.duration
        self.concentration = input_obj.concentration
        self.ritual = input_obj.ritual
        self.att_strs = [self.level,self.school,self.damagetype,self.aoe,self.range,self.duration,
                         self.concentration,self.ritual]
        
        self.base_fn = base_fn

        self.init_txt_files(txt_file_base)

        if n_att is None:
            self.n_att = len(self.txt_files)
        if n_pol is None:
            self.n_pol = 2*self.n_att + 1
        for i in range(len(self.txt_files)):
            assert os.path.isfile(self.txt_files[i]), f"Could not find file {self.txt_files[i]}"
        self.get_binary_values(override_dict)

    def init_txt_files(self,txt_file_base):
        self.txt_file_base = txt_file_base
        self.aoe_txt_file = os.path.join(self.txt_file_base, r"area_types.txt")
        self.dmg_txt_file = os.path.join(self.txt_file_base,r"damage_types.txt")
        self.dur_txt_file = os.path.join(self.txt_file_base,r"duration.txt")
        self.lvl_txt_file = os.path.join(self.txt_file_base,r"levels.txt")
        self.ran_txt_file = os.path.join(self.txt_file_base,r"range.txt")
        self.sch_txt_file = os.path.join(self.txt_file_base,r"school.txt")
        self.txt_files = [self.lvl_txt_file,
                          self.sch_txt_file,
                          self.dmg_txt_file,
                          self.aoe_txt_file,
                          self.ran_txt_file,
                          self.dur_txt_file]
        
    def read_txt_file(self,fpath):
        with open(fpath,"r") as f:
            data = f.readlines()
            f.close()
        data = [d.replace("\n","").lower() for d in data]
        return(data)

    def get_binary_values(self,override_dict = {}):
        binary_values = default_generation()
        self.binary_array = np.zeros((self.n_att,self.n_pol),dtype = int)
        override_keys = list(override_dict.keys())
        for i in range(self.n_att):
            if self.atts in override_keys:
                self.binary_array[i] = override_keys[self.atts]
            else:
                att_items = self.read_txt_file(self.txt_files[i])
                idx = att_items.index(self.att_strs[i])
                self.binary_array[i] = binary_values[idx]
        
        #------hard coding in the binary attributes
        self.level_b = binary_values[0]
        self.school_b = binary_values[1]
        self.damagetype_b = binary_values[2]
        self.aoe_b = binary_values[3]
        self.range_b = binary_values[4]
        self.duration_b = binary_values[5]

    def draw():
        pass

if __name__ == "__main__":
    test_inp = custom_spell_input(3,"evocation",
                                  "fire","sphere (20)",
                                  "150 feet","Instantaneous")
    test_obj = spell(test_inp,bases.circle)
    print(test_obj.binary_array)