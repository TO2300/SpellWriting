#
from SpellWriting.spell import spelldata, SpellAttribute



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