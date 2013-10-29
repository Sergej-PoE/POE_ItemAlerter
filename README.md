## ItemAlertPoE — Item Alerter for Path of Exile

**ItemAlertPoE** tracks all item drops in the game [Path of Exile](http://www.pathofexile.com/) and announces them by playing a sound telling you which kind of item it is.
Only valuable items are being annonunced. 
Initially all drops were assigned with a sound, i removed this functionality cause it were just too many.

Heavily adjusted by me (Sergej), original contributors mentioned below.

## Notes

Original author: <a href="http://www.ownedcore.com/forums/members/69674-sku.html">SKU</a> / <a href="https://github.com/zku">ZKU</a><br>
PoERecvOffsetFinder.exe author: <a href="http://www.ownedcore.com/forums/members/917705-spl3en.html">Spl3en</a> (<a href="http://spl3en.alwaysdata.net/src/C/PoeOffsetFinder/">Source</a>)

SKU Note: I would strongly advise against using this program on a hardcore character, as crashes may occur.

## Basic Item Alerter

## List of updates since 2013-04-24 (Y-m-d)

Sergej:
* 5 Link and 6 Link detection
* 6 socket detection
* Gem detection based on quality (adjust value in line 239: if quality >= 5:)
* Debug mode included, will log all properties of a drop. (DEBUG = True)
* configurable alerts (Rares, Gems,Maps, Currency, values of gold amulets and rings)
* logging functionality - drop an Andvarius to start logging, drop it again to stop logging. Logfile can be imported in excel.
* color coded output in the alert window
* can show mods and values of an identified item.
* added missing maps and gems  

old version:
* **Unique** items detection (plays unique.wav)
* **Superior Gem** detection (plays superiorgem.wav)
* Non filtered items play sound drop.wav
* Added Multistrike Support Gem
* Added Cyclone Skill Gem
* Removed scrolls from beeping
* Bugfix: Now works with no C:\Windows OS installations

## Installation instructions
* Download and install Python 2.7 32 bit version! (<a href="http://www.python.org/ftp/python/2.7.4/python-2.7.4.msi">link</a>)
* Download and install dependencies (<a href="http://www.lfd.uci.edu/~gohlke/pythonlibs/gj5m29a8/pydbg-1.2.win32-py2.7.exe">link</a>)
* Download and uncompress ItemAlertPoE anywhere (<a href="https://github.com/Sergej-PoE/POE_ItemAlerter/archive/master.zip">link</a>)
* Run Path of Exile game client
* Finally, double click ItemAlertPoE.py


