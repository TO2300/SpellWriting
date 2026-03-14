#
from pathlib import Path
from typing import Literal

import yaml
import requests
from rapidfuzz import process

from SpellWriting.generation import SpellData


SpellData_5e = SpellData.from_yaml(
    (Path(__file__).parent / 'fifth_edition.yaml'))

Offline_Library = {file.stem: SpellData_5e.yaml_spell(file)
           for file in (Path(__file__).parent / 'library').glob('*.yaml')}


with open((Path(__file__).parent / '5eTools_Index.yaml'), 'r') as fid:
    _5eTools_Index = yaml.safe_load(fid)
del fid
_5eTools_Spell_to_Json = {}
for key, value in _5eTools_Index.items():
    for name in value:
        if name in _5eTools_Spell_to_Json:
            continue # Err on the side of PHB
        _5eTools_Spell_to_Json[name] = key
del key, value, name
_BookMap = {Path(json).stem.split('-')[-1]: json for json in _5eTools_Index}


_5eCache = {}

@classmethod
def get_spell(cls, spell_name: Literal[*_5eTools_Spell_to_Json],
                  source: Literal[*_BookMap] = None) -> SpellData_5e:
    """
    Retrieves a spell from 5eTools using 2024 PHB, Tasha's, and Xanathar's.
    Spells err on the side of the player's handbook, so if you want the spell
    from a different book, use the source argument with 'xge', 'tce', or the
    last part of the "spells-*.json" data file name from 5e.toosl.data/spells.

    Parameters
    ----------
    spell_name : str
        Name exactly as it appears on 5eTools.
    source: str
        Override command to grab a different book's spells, literal "offline"
        will use the preloaded spells in the library

    Returns
    -------
    SpellData_5e
        Spell Data for the retrieved spell.

    """
    
    if source == 'offline':
        choices = list(Offline_Library)
        spell_name = process.extractOne(spell_name, choices)[0]
        return Offline_Library[spell_name]
    elif source == 'online' or source is None:
        choices = list(_5eTools_Spell_to_Json)
        spell_name = process.extractOne(spell_name, choices)[0]
        source = _5eTools_Spell_to_Json[spell_name]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document"
    }
    if source not in _5eCache:
        r = requests.get(source, headers=headers).json()
        _5eCache[source] = r
    else:
        r = _5eCache[source]
    spell = max(r['spell'], key=lambda d: d['name'] == spell_name)
    
    name = spell['name']
    level = spell['level']
    school = max(SpellData_5e.school.options,
                 key=lambda s : s[0] == spell['school'])
    
    damage_type = list(map(str.capitalize, spell.get('damageInflict', [])))
    if len(damage_type) == 1:
        damage_type = damage_type[0]
    elif len(damage_type) > 1:
        damage_type = tuple(sorted(damage_type))
    if not damage_type:
        damage_type = 'None'
    
    aoe_shape = spell.get('areaTags', None)
    
    rg = spell['range']
    tp = rg['type']
    if 'distance' in rg:
        if 'amount' in rg['distance']:
            am = rg['distance']['amount']
            unit = rg['distance']['type']
            if am != tp:
                rg = f"{rg['type']} ({am} {unit})"
            else:
                rg = 'point (None)'
        else:
            second = rg['distance']['type'].capitalize()
            first = rg['type']
            rg = f'{first} ({second})'
            # types[tp].add(rg['type'])
    else:
        rg = 'special (Special)'    
            
    duration = spell['duration']
    if len(duration) > 1:
        if duration[0]['type'] == 'instant':
            duration = duration[1]
    else:
        duration = duration[0]
    if duration['type'] == 'timed':
        timing = f'({duration["duration"]["amount"]} {duration["duration"]["type"]})'
        if duration.get('concentration', False):
            duration = f'concentration {timing}'
        else:
            duration = f'timed {timing}'
    elif 'amount' in duration:
        duration = f'timed ({duration["amount"]} {duration["type"]})'
    else:
        duration = f'special ({duration["type"].capitalize()})'
    
    spell_data = {'name' : name,
                  'system': '5e',
                  'level' : level,
                  'school' : school,
                  'damage_type' : damage_type,
                  'area_of_effect' : aoe_shape,
                  'range' : rg,
                  'duration' : duration}
    for key, value in spell_data.items():
        if value is None:
            spell_data[key] = 'None'
    
    return cls(**spell_data)

setattr(SpellData_5e, 'get_spell', get_spell)

