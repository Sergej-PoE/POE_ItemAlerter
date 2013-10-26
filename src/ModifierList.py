#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

'''
sku wrote this program. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.
'''


def getModifier(id):
    return _modifiers[id]

def getModifierName(id):
    if exists_modifier(id):
        return getModifier(id)[1]
    else:
        return " unknown mod / na"

def exists_modifier(id):
    found = False
    for key in _modifiers:
        if _modifiers[key][0] == id:
            found = True
            break
    
    return found
    
_modifiers = {}

_modifiers[0x0000c31c] = (0x0000c31c, " to Strength")

_modifiers[0x000085fd] = (0x000085fd, "% to Lightning Resistance")
_modifiers[0x00000fa1] = (0x00000fa1, "% to Lightning Resistance")
_modifiers[0x00000423] = (0x00000423, "% to Lightning Resistance")

_modifiers[0x0000c883] = (0x0000c883, "% to Chaos Resistance")


_modifiers[0x00004cfc] = (0x00004cfc, "% to Cold Resistance")
_modifiers[0x00005ca5] = (0x00005ca5, "% to Cold Resistance")
_modifiers[0x0000e1b8] = (0x0000e1b8, "% to Cold Resistance")

_modifiers[0x00007f6e] = (0x00007f6e, "% to Fire Resistance")




_modifiers[0x0000e083] = (0x0000e083, " to Maximum Life")
_modifiers[0x0000e4a9] = (0x0000e4a9, " to Maximum Life")
_modifiers[0x0000646f] = (0x0000646f, " to Maximum Life")
_modifiers[0x0000d253] = (0x0000d253, " to Maximum Life")

_modifiers[0x00008470] = (0x00008470, " to Maximum Mana")
_modifiers[0x0000afda] = (0x0000afda, " to Maximum Mana")

_modifiers[0x0000354e] = (0x0000354e, " to Maximum Energy Shield")

_modifiers[0x000049f6] = (0x000049f6, " to Armour")


_modifiers[0x00005d33] = (0x00005d33, "% increased Accuracy rating")
_modifiers[0x00001db5] = (0x00001db5, "% increased Accuracy rating")
_modifiers[0x0000c1b7] = (0x0000c1b7, "% increased Accuracy rating")
_modifiers[0x00007af7] = (0x00007af7, "% increased Accuracy rating")


_modifiers[0x000064d3] = (0x000064d3, "% increased Quantity of items found")
_modifiers[0x0000e977] = (0x0000e977, "% increased Quantity of items found")

_modifiers[0x000091d4] = (0x000091d4, "% increased Rarity of items found")
_modifiers[0x0000f20b] = (0x0000f20b, "% increased Rarity of items found")
_modifiers[0x00000a07] = (0x00000a07, "% increased Rarity of items found")


_modifiers[0x00007d3d] = (0x00007d3d, "% increased Evasion&Energy Shield")

_modifiers[0x0000b9fe] = (0x0000b9fe, "% increased Armour /% increased Block&Stun recovery")

_modifiers[0x0000ca67] = (0x0000ca67, "% increased Armour&Evasion/% increased Block&Stun recovery")

_modifiers[0x0000f968] = (0x0000f968, "% increased Evasion&Energy Shield/% increased Block&Stun recovery")

_modifiers[0x00004602] = (0x00004602, "% increased Block&Stun Recovery")
_modifiers[0x0000701c] = (0x0000701c, "% increased Block&Stun Recovery")


_modifiers[0x0000a0c8] = (0x0000a0c8, "% increased Spell damage")


_modifiers[0x0000cd5d] = (0x0000cd5d, " Life regenerated per second")
_modifiers[0x000022aa] = (0x000022aa, " Life regenerated per second")
_modifiers[0x0000f297] = (0x0000f297, " Life regenerated per second")



_modifiers[0x0000b755] = (0x0000b755, " physical damage reflect to melee attackers")