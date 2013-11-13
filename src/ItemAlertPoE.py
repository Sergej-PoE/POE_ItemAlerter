#!/usr/bin/env python   
# -*- coding: ISO-8859-1 -*-

'''
sku wrote this program. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.
'''


from os import system as OMGDONT
from ModifierList import getModifier, getModifierName
from ItemList import getItem, getItemName
from NotifyItems import shouldNotify, isQuiverItem, isShieldItem, isBeltItem, isGemItem, isFlaskItem, isArmourItem, isCurrencyItem, isMapItem, isJewelleryItem, getSocketColor
from ByteBuffer import ByteBuffer
import ctypes
import sys
import threading
import winsound
import atexit
import datetime
import traceback

from colorama import init, Fore, Back, Style

init(autoreset=True)

try:
    from pydbg import *
    from pydbg.defines import *
except:
    print 'You seem to be missing pydbg or pydasm.'
    print 'Precompiled binaries can be downloaded from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pydbg'
    sys.exit(1)

ALERT_VERSION = '20131113'
POE_VERSION = '1.0.0g'
DEBUG = False

ALERT_RARES = True
ALERT_GEMS = True
ALERT_SPECIALGEMS = True
ALERT_MAPS = True
ALERT_CURR = True
ALERT_JEW_VALUES = True

#SHOW_OWN_ITEMS_ONLY = True

# Configuration for which drops sounds are played

#orbs
SOUND_eternal = True
SOUND_exalted = True
SOUND_divine = True
SOUND_gcp = True
SOUND_regal = True
SOUND_regret = True
SOUND_chaos = True
SOUND_blessed = True
SOUND_scour = True
SOUND_alc = True
SOUND_fuse = True
SOUND_chis = True
SOUND_chance = False
SOUND_jew = False
SOUND_glass = False
SOUND_mirror = True

#uniques
SOUND_uniques = True

#5-Link / 6-Link
SOUND_slots = True

#6 socket 
SOUND_6sockets = True

# special gems
SOUND_specialgems = True
specialGems = '0x4C32EEEE,0x26856055'
gemqual = 5

#maps
SOUND_maps = True


RUN_START = 0
RUN_END = 0

RUN = False

number_of_uniques = 0
number_of_rares = 0
number_of_orbs = 0
number_of_maps = 0



class PlaySoundMaps(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\legendarypoe.wav', winsound.SND_FILENAME)

class PlaySound6Sockets(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\payback_time.wav', winsound.SND_FILENAME)

class PlaySoundCraftingItem(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\craftingpoe.wav', winsound.SND_FILENAME)

class PlaySoundholy(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\holyshit.wav', winsound.SND_FILENAME)        

class PlaySoundWorker(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\drop.wav', winsound.SND_FILENAME)
        
class PlaySoundUnique(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\legendarypoe.wav', winsound.SND_FILENAME)
        
class PlaySoundSuperiorGem(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\superiorgem.wav', winsound.SND_FILENAME)
        
class PlaySoundSuperiorFlask(threading.Thread):
    def run(self):
        winsound.PlaySound(r'sounds\superiorflask.wav', winsound.SND_FILENAME)
        
class SoundPlayer(threading.Thread):
    def run(self, sound):
        winsound.PlaySound(r'sounds\\' + sound, winsound.SND_FILENAME)
        print >>self.logFile, str.format('Playing: {0!s}', sound)

class ItemAlert(object):

    BP0 = 0x00257239 + 0x00400000
    BP1 = 0x00257231 + 0x00400000
    BP2 = 0x0025727b + 0x00400000

    # 1.0.0f and 1.0.0g
    #BP0 = 0x00257239 + 0x00400000
    #BP1 = 0x00257231 + 0x00400000
    #BP2 = 0x0025727b + 0x00400000

    # 1.0.0e
    #BP0 = 0x00257109 + 0x00400000 #MOV EDI, EAX
    #BP1 = 0x00257101 + 0x00400000 #PUSH EAX 
    #BP2 = 0x0025714B + 0x00400000 #MOV EAX,DWORD PTR [ESI+54]

    #BP0 = 0x00235149 + 0x00400000
    #BP1 = 0x00235141 + 0x00400000
    #BP2 = 0x0023518B + 0x00400000
    
    number_of_uniques = 0
    number_of_rares = 0
    number_of_orbs = 0
    number_of_maps = 0
    
    RUN = False
    
    def __init__(self):
        atexit.register(self.atExit)
        self.logFile = open('log.txt', 'a', 0)
        self.statFile = open('stats.txt', 'a', 0)
        print >>self.logFile, 40 * '='
        print >>self.logFile, str.format('Started ItemAlertPoE version {0} at {1!s}.', ALERT_VERSION, datetime.datetime.now())
        print >>self.logFile, str.format('Python version: {0!s}', sys.version_info)
        self.dbg = pydbg()
        self.dbg.attach(self.getProcessId())
        self.baseAddress = self.getBaseAddress()
        adjustment = self.baseAddress - 0x00400000
        ItemAlert.BP0 += adjustment
        ItemAlert.BP1 += adjustment
        ItemAlert.BP2 += adjustment
        self.lastPacketBufferAddress = 0
        self.lastPacketSize = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logFile.close()
        self.statFile.close()

    def grabPacketSize(self, dbg):
        self.lastPacketSize = dbg.get_register('eax')
        return DBG_CONTINUE

    def beforeDemanglingPacket(self, dbg):
        self.lastPacketBufferAddress = dbg.get_register('eax')
        return DBG_CONTINUE
        

    def parseWorldItemPacket(self, packetData):
    
        global number_of_uniques
        global number_of_rares 
        global number_of_orbs 
        global number_of_maps
        global RUN
    
        try:
            buffer = ByteBuffer(packetData)
            buffer.setEndian(ByteBuffer.BIG_ENDIAN)

            if DEBUG:
                print >>self.logFile, '---------------------------------'
                print >>self.logFile, 'packet:'
                print >>self.logFile, self.dbg.hex_dump(map(lambda x: chr(x), packetData))
                            
            
            id = buffer.nextByte()
            #print >>self.logFile, str.format('id = {0}', id)
            
            objectType = buffer.nextDword()
            #print >>self.logFile, str.format('ObjectType = {0}', objectType)
            
            unk1 = buffer.nextDword()
            #print >>self.logFile, str.format('unk1 = {0}', unk1)
            
            unk2 = buffer.nextByte()
            #print >>self.logFile, str.format('unk2 = {0}', unk2)
            
            if unk2 != 0: 
                print >>self.logFile, 'The following packet has an odd unk2 field:'
                print >>self.logFile, self.dbg.hex_dump(map(lambda x: chr(x), packetData))
                return

            x = buffer.nextDword()
            #print >>self.logFile, str.format('x = {0}', x)
            
            y = buffer.nextDword()
            #print >>self.logFile, str.format('y = {0}', y)
            
            rot = buffer.nextDword()
            #print >>self.logFile, str.format('rot = {0}', rot)

            unk3 = buffer.nextDword(ByteBuffer.LITTLE_ENDIAN)
            #print >>self.logFile, str.format('unk3 = {0}', unk3)
            
            unk4 = buffer.nextDword()
            #print >>self.logFile, str.format('unk4 = {0}', unk4)
            
            if unk3 >> 2 != 0:
                print >>self.logFile, 'The following packet has an odd unk3 field:'
                print >>self.logFile, self.dbg.hex_dump(map(lambda x: chr(x), packetData))
                buffer.nextDword()
                buffer.nextDword()

            unk5 = buffer.nextDword()
            #print >>self.logFile, str.format('unk5 = {0}', unk5)

            unk6 = buffer.nextDword()
            #print >>self.logFile, str.format('unk6 = {0}', unk6)

            unk7 = buffer.nextByte()
            #print >>self.logFile, str.format('unk7 = {0}', unk7)
            
            unk8 = buffer.nextDword()
            #print >>self.logFile, str.format('unk8 = {0}', unk8)
			
            
            if unk8 >= 2:

                unk8 = buffer.nextDword()

            dropped_by_entity = buffer.nextByte()
            if DEBUG:
                print >>self.logFile, str.format('dropped by player or mob : {0}', dropped_by_entity)
            
            itemId = buffer.nextDword()
            print >>self.logFile, 'itemId = ' + "0x%x"%(itemId&0xffffffff)

            remaining = buffer.getRemainingBytes()
            
            itemName = getItemName(itemId)
            print >>self.logFile, str.format('itemName = {0}', itemName)

            if itemName == "unknown item":
                
                if DEBUG:
                    print Style.BRIGHT + Fore.RED + 'UNKNOWN ITEM:' + "0x%x"%(itemId&0xffffffff)

                print >>self.logFile, '---------------------------------'
                return

            if isCurrencyItem(itemName):
            
                if itemId !=0x50880BAF and itemId != 0x4F2B00ED: 
                    print Fore.WHITE + str.format('CUR: {0}',itemName)
                    number_of_orbs += 1

                    if itemId == 0x61B2F5ED and SOUND_eternal == True: # Eternal Orb
                        crafting_drop = PlaySoundholy()
                        crafting_drop.start()
                    if itemId == 0xC04F5629 and SOUND_exalted == True: # Exalted Orb
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x80047CFD and SOUND_divine == True: # Divine Orb
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x07A992EB and SOUND_gcp == True: # Gemcutter's Prism
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0xD8BD4F5D and SOUND_regal == True: # Regal Orb
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x9B4B42A5 and SOUND_regret == True: # Orb of Regret
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x7353DDF9 and SOUND_chaos == True: # Chaos Orb
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x2D8E7632 and SOUND_blessed == True: # Blessed Orb
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x7F0EF637 and SOUND_scour == True: # Orb of Scouring
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x9110493F and SOUND_alc == True: # Orb of Alchemy
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0xC71BF58D and SOUND_fuse == True: # Orb of Fusing
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0xDC217297 and SOUND_chis == True: # Cartographer's Chisel
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0xC5732C85 and SOUND_chance == True: # Orb of Chance
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0xDD917991 and SOUND_jew == True: # Jeweller's Orb
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0xDD74C4BF and SOUND_glass == True: # Glassblower's Bauble
                        crafting_drop = PlaySoundCraftingItem()
                        crafting_drop.start()
                    if itemId == 0x79C23B15 and SOUND_mirror == True: # Mirror of Kalandra
                        crafting_drop = PlaySoundholy()
                        crafting_drop.start()
                
                return
                
            actual = buffer.nextByte()
            actual = buffer.nextByte()
            actual = buffer.nextByte()
            actual = buffer.nextDword()
            itemlevel = buffer.nextDword()
            if DEBUG:
                print >>self.logFile, str.format('itemlevel = {0}', itemlevel)

            if isGemItem(itemName) and ALERT_GEMS == True:

                actual = buffer.nextByte()
                quality = int(buffer.nextDword())
                if DEBUG:
                    print >>self.logFile, str.format('Gem quality = {0}', quality)
                if quality >= gemqual:
                    print Fore.CYAN + str.format('GEM: {0}, quality: {1}',itemName,quality)

                if str(hex(itemId)) in specialGems and ALERT_SPECIALGEMS == True:
                    print Fore.CYAN + str.format('Special GEM: {0}, quality: {1}',itemName,quality)
                    
                    if SOUND_specialgems == True:
                        gem_drop = PlaySoundholy()
                        gem_drop.start()
                    
                print >>self.logFile, '---------------------------------'
                return

            req_lvl = buffer.nextDword()
            actual = buffer.nextDword()
            actual = buffer.nextByte()
            rarity = buffer.nextDword()
            if DEBUG:
                print >>self.logFile, str.format('rarity = {0}', rarity)

            identified = buffer.nextDword()
            if DEBUG:
                print >>self.logFile, str.format('identified = {0}', identified)
                
            
            if isMapItem(itemName) and ALERT_MAPS == True:
                
                actual = buffer.nextDword()
                actual = buffer.nextDword()
                actual = buffer.nextByte()
                
                actual = buffer.nextDword()
                actual = buffer.nextDword()
                quality = int(buffer.nextDword())
                actual = int(buffer.nextByte())
                if DEBUG:
                    print >>self.logFile, str.format('quality = {0}', quality)
                
                if quality == 0 and actual == 0:
                    quality = int(buffer.nextDword())
                    if DEBUG:
                        print >>self.logFile, str.format('quality new = {0}', quality)
                
                print Style.BRIGHT + Fore.BLUE + str.format('MAP: {0}, rarity: {1}, itemlevel: {2}, quality: {3}',itemName,rarity,itemlevel,quality)

                print >>self.logFile, '---------------------------------'
                if SOUND_maps == True:
                    map = PlaySoundMaps()
                    map.start()

                
                number_of_maps += 1
                return

            if isBeltItem(itemName):
                
                if rarity == 3:
                
                    print Fore.YELLOW + str.format('UNI BELT: {0}, rarity: {1}',itemName,rarity)
                    if SOUND_uniques == True:
                        unique = PlaySoundUnique()
                        unique.start()

                    number_of_uniques += 1
            
                elif rarity == 2 and ALERT_RARES == True:
                
                    print Style.BRIGHT + Fore.YELLOW + str.format('BELT: {0}, rarity: {1}, itemlevel: {2}',itemName,rarity,itemlevel)

                print >>self.logFile, '---------------------------------'
                
                return

            if isQuiverItem(itemName):
                
                if rarity == 3:
                
                    print Fore.YELLOW + str.format('UNI Quiver: {0}, rarity: {1}',itemName,rarity)
                    if SOUND_uniques == True:
                        unique = PlaySoundUnique()
                        unique.start()

                    number_of_uniques += 1
            
                elif rarity == 2 and ALERT_RARES == True:
                
                    print Style.BRIGHT + Fore.YELLOW + str.format('QUIV: {0}, rarity: {1}, itemlevel: {2}',itemName,rarity,itemlevel)

                print >>self.logFile, '---------------------------------'
                
                return

            if isJewelleryItem(itemName):
                
                if rarity == 2 and ALERT_RARES == True:
                    print Style.BRIGHT + Fore.YELLOW + str.format('JEW: {0}, rarity: {1}',itemName,rarity)
                    number_of_rares += 1
                    
                if (rarity == 0 or rarity == 1) and (itemId == 0x29F77698 or itemId == 0xDE069771) and ALERT_JEW_VALUES == True:

                    _implicitmods = int(buffer.nextDword())
                    _mod = buffer.nextDword()
                    _modvalues = buffer.nextByte()
                    _modvalue = int(buffer.nextDword())
                    
                    if _modvalue >= 13 and itemId == 0x29F77698:

                        print Fore.WHITE + str.format('JEW: {0}, Value: {1}',itemName,_modvalue)
                        
                    if _modvalue >= 18 and itemId == 0xDE069771:

                        print Fore.WHITE + str.format('JEW: {0}, Value: {1}',itemName,_modvalue)
                    
                elif rarity == 3:
                
                    if identified == 1 and itemId == 0x29F77698:
                        
                        if RUN == False:
                            RUN = True
                            number_of_uniques = 0
                            number_of_rares = 0
                            number_of_orbs = 0
                            number_of_maps = 0
                            
                            staTime= datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                            startTime = str.format('{0}',staTime)
                            
                            print Style.BRIGHT + Fore.GREEN + str.format('==== {0} ===== RUN started ===========',startTime)
                            
                            #print >>self.logFile, str.format('{0}', startTime)
                            # measure runtime later on here, get the start time
                            
                        else:
                        
                            RUN = False
                            stoTime = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                            stopTime = str.format('{0}',stoTime)
                            print Style.BRIGHT + Fore.GREEN + str.format('==== {0} ===== RUN stopped ===========',stopTime)                            
                            print >>self.statFile, str.format('{0},{1},{2},{3},{4}', stopTime,number_of_uniques,number_of_rares,number_of_orbs,number_of_maps)
                            
                    else:
                        print Fore.YELLOW + str.format('UNI JEW: {0}, rarity: {1}',itemName,rarity)
                        if SOUND_uniques == True:
                            unique = PlaySoundUnique()
                            unique.start()
                        
                        number_of_uniques += 1

                        
                print >>self.logFile, '---------------------------------'
                return

            if isArmourItem(itemName):
                    
                if rarity == 0:

                    if shouldNotify(itemName):
                        print Fore.WHITE + str.format('SPC: {0}', itemName)
                        # worker = PlaySoundWorker()
                        # worker.start()

                        print >>self.logFile, '---------------------------------'
                        return
                        
                elif rarity == 2:
                    number_of_rares += 1
                
                if identified == 1:

                    if isShieldItem(itemName):
                    
                        if DEBUG:
                            print >>self.logFile, str.format('identified as SHIELD', '1')

                        _implicitmod = int(buffer.nextDword())
                        
                        if _implicitmod == 2:
                            actual=buffer.nextDword()
                                
                            _skipnext = int(buffer.nextByte())

                            if _skipnext >= 1:
                                actual=buffer.nextDword()

                                _impl_mod = int(buffer.nextDword())
                                if DEBUG:
                                    print >>self.logFile, str.format('implicit mod = {0}', _impl_mod)

                                _impl_mod_values = int(buffer.nextByte())
                                
                                for i in range(0,_impl_mod_values):
                                    # needs to be worked out
                                    _mod_value = int(buffer.nextDword())
                                    
                                _skipnext = int(buffer.nextByte())
                                    
                                if _skipnext >= 1:
                                    for i in range(0,_skipnext):
                                        actual = int(buffer.nextDword())

                                    
                        else:
                        
                            actual=buffer.nextDword()
                        
                            _skipnext = int(buffer.nextByte())            

                            if _skipnext >= 1:                        
                                for i in range(0,_skipnext):
                                    actual=buffer.nextDword()
                    
                                _skipnext = int(buffer.nextByte())            

                                if _skipnext >= 1:                        
                                    for i in range(0,_skipnext):
                                        actual=buffer.nextDword()
                    
                    else:
                        _implicitmods = int(buffer.nextDword())
                        
                        if _implicitmods == 2:
                        
                            if DEBUG:
                                print >>self.logFile, str.format('_implicitmods = {0}', _implicitmods)
            
                        elif _implicitmods == 1:

                            _implicitmod = buffer.nextDword()
                            if DEBUG:
                                print >>self.logFile, str.format('_implicitmod = {0}', _implicitmod)
                            
                            _impl_mod_values = int(buffer.nextByte())
                            if DEBUG:
                                print >>self.logFile, str.format('_impl_mod_values = {0}', _impl_mod_values)
                            
                            
                            for i in range(0,_impl_mod_values):
                                # needs to be worked out
                                _mod_value = int(buffer.nextDword())
                                
                        unk_mod=int(buffer.nextByte())
                        
                        if unk_mod >=0:
                            for i in range(0,unk_mod):
                                # needs to be worked out
                                _mod_value = int(buffer.nextDword())
                            
                    
                    number_of_mods = int(buffer.nextDword())

                else:
                
                    if isShieldItem(itemName):
                    
                        if DEBUG:
                            print >>self.logFile, str.format('identified as SHIELD', '1')
                    
                
                        _implicitmod = int(buffer.nextDword())
                        
                        if _implicitmod == 2:
                        
                            actual=buffer.nextDword()
                                
                            _skipnext = int(buffer.nextByte())

                            if _skipnext >= 1:
                                actual=buffer.nextDword()

                                _impl_mod = int(buffer.nextDword())
                                
                                if DEBUG:
                                    print >>self.logFile, str.format('implicit mod = {0}', _impl_mod)

                                _impl_mod_values = int(buffer.nextByte())

                                if DEBUG:
                                    print >>self.logFile, str.format('_impl_mod_values = {0}', _impl_mod_values)
                                
                                
                                if _impl_mod_values > 0:
                                    for i in range(0,_impl_mod_values):
                                        # needs to be worked out
                                        _mod_value = int(buffer.nextDword())
                                        if DEBUG:
                                            print >>self.logFile, str.format('_mod_value = {0}', _mod_value)

                        elif _implicitmod == 1:
                        
                            actual=buffer.nextDword()
                        
                            _skipnext = int(buffer.nextByte())            

                            if _skipnext >= 1:                        
                                for i in range(0,_skipnext):
                                    actual=buffer.nextDword()

                    else:

                        _implicitmods = int(buffer.nextDword())
                        
                        if _implicitmods == 2:
                        
                            if DEBUG:
                                print >>self.logFile, str.format('_implicitmods = {0}', _implicitmods)
            
                        elif _implicitmods == 1:

                            _implicitmod = buffer.nextDword()
                            if DEBUG:
                                print >>self.logFile, str.format('_implicitmod = {0}', _implicitmod)
                            
                            _impl_mod_values = int(buffer.nextByte())
                            if DEBUG:
                                print >>self.logFile, str.format('_impl_mod_values = {0}', _impl_mod_values)
                            
                            
                            for i in range(0,_impl_mod_values):
                                # needs to be worked out
                                _mod_value = int(buffer.nextDword())

                    number_of_mods = 0
                                
                if DEBUG:
                    print >>self.logFile, str.format('number of explicit mods = {0}', number_of_mods)
                
                if number_of_mods > 6:
                    print >>self.logFile, 'The last packet had an odd number_of_mods field:'
                    print >>self.logFile, self.dbg.hex_dump(map(lambda x: chr(x), packetData))

                    print >>self.logFile, '---------------------------------'                        
                    return
                
                
                for i in range(0,number_of_mods):
                    mod_id = buffer.nextDword()
                    if DEBUG:
                        print >>self.logFile, str.format('mod id = {0}', mod_id)
                    sub_mod_count = buffer.nextByte()
                    if sub_mod_count > 3:
                        print >>self.logFile, 'The last packet had an odd sub_mod_count field:'
                        if DEBUG:
                            print >>self.logFile, self.dbg.hex_dump(map(lambda x: chr(x), packetData))

                        print >>self.logFile, '---------------------------------'                        
                        return
                    
                    for ii in range(0,sub_mod_count):
                        mod_value=buffer.nextDword()
                        if sub_mod_count == 1:
                            if DEBUG:
                                print >>self.logFile, str.format('Modifier: {0}{1}', mod_value, getModifierName(mod_id))
                        elif sub_mod_count == 2:
                            if mod_value != 0:
                                sub_mods = getModifierName(mod_id).split("/")
                                sub_mod = sub_mods[ii]
                                if DEBUG:
                                    print >>self.logFile, str.format('Modifier: {0}{1}', mod_value, sub_mod)
                    
                quality = buffer.nextDword()
                if DEBUG:
                    print >>self.logFile, str.format('quality = {0}', quality)
                actual = buffer.nextByte()
                sockets = int(buffer.nextDword())
                if DEBUG:
                    print >>self.logFile, str.format('sockets = {0}', sockets)

                if sockets == 0 or sockets > 6:
                    print >>self.logFile, 'The last packet had an odd sockets field:'
                    if DEBUG:
                        print >>self.logFile, self.dbg.hex_dump(map(lambda x: chr(x), packetData))
                    
                    print >>self.logFile, '---------------------------------'                        
                    return
                
                _all_color = []
                
                sock_color_tmp = ""
                sock_color_tmp = getSocketColor(int(buffer.nextByte()))
                
                actual = buffer.nextByte()
                _all_color.append(sock_color_tmp)
                
                for i in range(1,sockets):
                    sock_color_tmp = getSocketColor(int(buffer.nextByte()))
                    actual = buffer.nextByte()
                    _all_color.append(sock_color_tmp)

                if DEBUG:
                    print >>self.logFile, str.format('socket colors = {0}', _all_color)
                    
                sock_fragments = int(buffer.nextDword())
                
                if DEBUG:
                    print >>self.logFile, str.format('socket fragments = {0}', sock_fragments)

                if sock_fragments > 6 or sock_fragments == 0:
                    print >>self.logFile, 'The last packet had an odd sock_fragments field:'
                    if DEBUG:
                        print >>self.logFile, self.dbg.hex_dump(map(lambda x: chr(x), packetData))

                    print >>self.logFile, '---------------------------------'                        
                    return
                
                listlen = len(_all_color)
                
                if sock_fragments == 1:
                    if DEBUG:
                        print >>self.logFile, str.format('Fully linked = {0}', sock_fragments)
                    ii=0
                    for i in range(1,listlen):
                        _all_color.insert(i+ii,"-")
                        ii=ii+1
                        
                else:
                    iii=0
                    maxfrag = 1
                    for i in range(0,sock_fragments):
                        frag = int(buffer.nextByte())
                        if frag > 1:
                            if maxfrag < frag:
                                maxfrag = frag
                            for ii in range(1,frag):
                                _all_color.insert(ii+iii,"-")
                                iii=iii+1
                            iii=iii+ii+1
                        else:
                            iii=iii+1
                
                socketsetup = ''.join(_all_color)
                
                if DEBUG:
                    print >>self.logFile, str.format('Socket Setup = {0}', socketsetup)

                rare_alerted = False 
                    
                if any(i in socketsetup for i in ('R-G-B','R-B-G','G-B-R','G-R-B','B-R-G','B-G-R','R-B-B-G','G-R-R-B','G-B-B-R','B-G-G-R','B-R-R-G','R-G-G-B')):
                
                    if rarity == 0:
                        print Style.BRIGHT + Fore.RED + "R" + Style.BRIGHT + Fore.GREEN + "G" + Style.BRIGHT + Fore.BLUE + "B" + Style.BRIGHT + Fore.WHITE + str.format(': {0}, rarity: {1}, itemlevel: {2}',itemName,rarity,itemlevel)
                    if rarity == 1:
                        print Style.BRIGHT + Fore.RED + "R" + Style.BRIGHT + Fore.GREEN + "G" + Style.BRIGHT + Fore.BLUE + "B" + Style.BRIGHT + Fore.BLUE + str.format(': {0}, rarity: {1}, itemlevel: {2}',itemName,rarity,itemlevel)
                    if rarity == 2:
                        print Style.BRIGHT + Fore.RED + "R" + Style.BRIGHT + Fore.GREEN + "G" + Style.BRIGHT + Fore.BLUE + "B" + Style.BRIGHT + Fore.YELLOW + str.format(': {0}, rarity: {1}, itemlevel: {2}',itemName,rarity,itemlevel)
                        rare_alerted = True 
                        
                    
                msg = ""
                if sockets == 5:
                    if sock_fragments == 1:
                        msg = "5-SLOT 5-LINK"
                if sockets == 6:
                    if sock_fragments == 1:
                        msg = "6-SLOT 6-LINK"
                    elif sock_fragments == 2:
                        if maxfrag == 5:
                            msg = "6-SLOT 5-LINK"
                        else:
                            msg = "6-SLOT"
                    else:
                        msg = "6-SLOT"
                
                if msg != "":
                    print >>self.logFile, msg

                    if rarity == 0:
                        print Style.BRIGHT + Fore.MAGENTA + msg + Style.BRIGHT + Fore.WHITE + str.format(' : {0}, rarity: {1}, ilvl: {2}, qual: {3}, sockets: {4}',itemName,rarity,itemlevel,quality, socketsetup)
                    if rarity == 1:
                        print Style.BRIGHT + Fore.MAGENTA + msg + Style.BRIGHT + Fore.BLUE + str.format(' : {0}, rarity: {1}, ilvl: {2}, qual: {3}, sockets: {4}',itemName,rarity,itemlevel,quality, socketsetup)
                    if rarity == 2:
                        print Style.BRIGHT + Fore.MAGENTA + msg + Style.BRIGHT + Fore.YELLOW + str.format(' : {0}, rarity: {1}, ilvl: {2}, qual: {3}, sockets: {4}',itemName,rarity,itemlevel,quality, socketsetup)
                        rare_alerted = True 

                    if SOUND_slots == True and msg != "6-SLOT":
                        sound = PlaySoundholy()
                        sound.start()
                    else:
                        if SOUND_6sockets == True:
                            sound = PlaySound6Sockets()
                            sound.start()
                        
                if rarity == 3:
                    print >>self.logFile, 'UNIQUE !'                    number_of_uniques += 1
                    
                    print Fore.YELLOW + str.format('UNI: {0}, rarity: {1}, ilvl: {2}, qual: {3}, sockets: {4}',itemName,rarity,itemlevel,quality, socketsetup)
                    
                    if SOUND_uniques == True:
                        unique = PlaySoundUnique()
                        unique.start()

                if rarity == 2 and ALERT_RARES == True and rare_alerted == False:
                
                    print Style.BRIGHT + Fore.YELLOW + str.format('RARE: {0}, rarity: {1}, itemlevel: {2}',itemName,rarity,itemlevel)
                    
                    
                print >>self.logFile, '---------------------------------'
                return
                    
            
            print >>self.logFile, '---------------------------------'            
                
        except: pass

    def afterDemanglingPacket(self, dbg):
        if self.lastPacketBufferAddress != 0 and self.lastPacketSize > 1:
            packetData = dbg.read_process_memory(self.lastPacketBufferAddress, self.lastPacketSize)
            packetData = map(lambda x: ord(x), packetData)
            for i in range(self.lastPacketSize):
                if packetData[i:i+5] == [0xf0, 0x54, 0x92, 0x8a, 0x3a]:
                    self.parseWorldItemPacket(packetData[i:])
        return DBG_CONTINUE

    def getProcessId(self):
        clients = [x[0] for x in self.dbg.enumerate_processes() if x[1].lower() == 'pathofexile.exe']
        print >>self.logFile, str.format('"pathofexile.exe" processes found: {0!s}', clients)
        pid = None
        if not clients or len(clients) == 0: print 'No "pathofexile.exe" process found.'
        #elif len(clients) > 1: print 'Found more than one "pathofexile.exe" process.'
        else: pid = clients[0]
        return pid

    def getBaseAddress(self):
        base = [x[1] for x in self.dbg.enumerate_modules() if x[0].lower() == 'pathofexile.exe'][0]
        print >>self.logFile, str.format('Base address: 0x{0:08x}', base)
        return base

    def run(self):
        print >>self.logFile, str.format('bp0: 0x{0:08x}: {1}', ItemAlert.BP0, self.dbg.disasm(ItemAlert.BP0))
        print >>self.logFile, str.format('bp1: 0x{0:08x}: {1}', ItemAlert.BP1, self.dbg.disasm(ItemAlert.BP1))
        print >>self.logFile, str.format('bp2: 0x{0:08x}: {1}', ItemAlert.BP2, self.dbg.disasm(ItemAlert.BP2))
        try:
            self.dbg.bp_set(ItemAlert.BP0, handler=self.grabPacketSize)
            self.dbg.bp_set(ItemAlert.BP1, handler=self.beforeDemanglingPacket)
            self.dbg.bp_set(ItemAlert.BP2, handler=self.afterDemanglingPacket)
        except Exception as inst:
            print >>self.logFile, type(inst)
            print >>self.logFile, inst.args
            print >>self.logFile, inst
            traceback.print_exc(file=self.logFile)
        print >>self.logFile, 'Starting main loop.'
        try: self.dbg.debug_event_loop()
        except: pass

    def atExit(self):
        try: self.dbg.detach()
        except: pass

def checkVersion():
    if ctypes.sizeof(ctypes.c_voidp) != 4:
        print 'This program only works with a 32-bit Python installation!'
        print 'The preferred (tested) version is Python 2.7, 32-bit.'
        print 'You can download it from here: http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi'
        sys.exit(1)

def main():
    OMGDONT('title Path of Exile ItemAlert by Sarge, original by sku')
    checkVersion()
    print Fore.RED + str.format('Starting ItemAlert {0} for Path of Exile {1} by Sarge, original by sku', ALERT_VERSION, POE_VERSION)
    with ItemAlert() as alerter: alerter.run()

if __name__ == '__main__':
    main()
