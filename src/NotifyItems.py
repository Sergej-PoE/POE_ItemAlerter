#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

'''
sku wrote this program. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.
'''


import ItemList

def getSocketColor(socket_color):
    if socket_color == 1:
        return "R"
    elif socket_color == 2:
        return "G"
    elif socket_color == 3:
        return "B"


def shouldNotify(itemName):
    return True if not _filterItems else itemName in getNotifyItems()
    
def isGemItem(itemName):
    return True if not _filterItems else itemName in getGemItems()
    
def isFlaskItem(itemName):
    return True if not _filterItems else itemName in getFlaskItems()

def isArmourItem(itemName):
    return True if not _filterItems else itemName in getArmourItems()

def isCurrencyItem(itemName):
    return True if not _filterItems else itemName in getCurrencyItems()
    
def isMapItem(itemName):
    return True if not _filterItems else itemName in getMapItems()
    
def isJewelleryItem(itemName):
    return True if not _filterItems else itemName in getJewelleryItems()
    
def isShieldItem(itemName):
    return True if not _filterItems else itemName in getShieldItems()
    
def isBeltItem(itemName):
    return True if not _filterItems else itemName in getBeltItems()
    
    
    
def getNotifyItems():
    return _notifyItems
    
def getGemItems():
    return _gemItems
    
def getFlaskItems():
    return _flaskItems

def getArmourItems():
    return _armourItems
    
def getCurrencyItems():
    return _currencyItems
   
def getMapItems():
    return _mapItems

def getJewelleryItems():
    return _jewelleryItems

def getShieldItems():
    return _shieldItems

def getBeltItems():
    return _beltItems
    
_beltItems = []
keywords = ["Belts"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in keywords): _beltItems.append(ItemList._items[key][1])
    
_shieldItems = []
keywords = ["Shields"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in keywords): _shieldItems.append(ItemList._items[key][1])



    
# Recommended patch by Rhynocerous.
_notifyItems = []
keywords = ["Map", "Currency"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in keywords): _notifyItems.append(ItemList._items[key][1])

#python sucks
_gemItems = []
gemwords = ["Gems"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in gemwords): _gemItems.append(ItemList._items[key][1])
    
#python sucks
_flaskItems = []
flaskwords = ["Flasks"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in flaskwords): _flaskItems.append(ItemList._items[key][1])

#python sucks
_armourItems = []
armourwords = ["Armours", "Weapons"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in armourwords): _armourItems.append(ItemList._items[key][1])

#python sucks    
_currencyItems = []
currencywords = ["Currency"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in currencywords): _currencyItems.append(ItemList._items[key][1])

#python sucks
_mapItems = []
mapwords = ["Map"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in mapwords): _mapItems.append(ItemList._items[key][1])

#python sucks
_jewelleryItems = []
jewellerywords = ["Rings", "Amulets"]
for key in ItemList._items:
    if any(x in ItemList._items[key][2] for x in jewellerywords): _jewelleryItems.append(ItemList._items[key][1])
    
# === SETTINGS ===	

# Set this to True if you want to filter items and only announce
# items that have been added to the _notifyItems list.
# If _filterItems is False, ItemAlertPoE will announce every item drop.
_filterItems = True

# Add items that you wish to announce to this list.
# This list is only considered if _filterItems is set to True.
# If the item name countains a single quote, either escape it
# using \' or use double quotes like in the example below.
#_notifyItems.append("Driftwood Wand")
#_notifyItems.append("Driftwood Club")
_notifyItems.append("Occultist's Vestment")
_notifyItems.append("Imperial Bow")
_notifyItems.append("Murder Mitts")
_notifyItems.append("Spine Bow")
