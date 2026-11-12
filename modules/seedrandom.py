##
# seedrandom.py
#
# Vega Strike: Black Paralysis - Space Simulation, Combat and Trading
# Copyright (C) 2003-2005 Daniel Aleksandrow <dandandaman@users.sourceforge.net>
# Copyright (C) 2003-2026 The Vega Strike Contributors
#
# https://github.com/vegastrike/vsu-black-paralysis
#
# This file is part of Vega Strike: Black Paralysis.
#
# Vega Strike: Black Paralysis is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Vega Strike: Black Paralysis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Vega Strike: Black Paralysis.  If not, see <https://www.gnu.org/licenses/>.
#

_seed=0
RAND_MAX = 0x7fffffff
aye = ord('a')
AAYE= ord('A')
Uhun= ord('0')
totalnormchar=26+26+10
def getNumFromChar(c):
    global aye,AAYE, Uhun
    charnum=ord(c)
    if (charnum-aye<26):
        charnum = charnum-aye
    else:
        if (charnum-AAYE<26):
            charnum = charnum-AAYE+26
        else:
            if (charnum-Uhun<10):
                charnum = charnum-Uhun+26+26
    return charnum
def seedstring (stru):
    num=0
    l=len (stru)
    for i in range(l):
        global totalnormchar,RAND_MAX
        num+=getNumFromChar(stru[l-i-1])
        num*=totalnormchar
        num = num % RAND_MAX
    return num
def interleave (slist):
    touch=1
    index=0
    rez=''
    while (touch):
        touch=0
        for s in slist:
            if len(s)>index:
                touch=1
                rez+=s[index]
        index+=1
    return rez
_seed=0
def rands(intseed):
    global RAND_MAX
    intseed = int(intseed) * 1103515245 + 12345
    intseed = intseed % RAND_MAX
    return intseed
def rand():
    global _seed
    _seed = rands (_seed)
    return _seed
def seed (seednum):
    global _seed
    _seed = seednum
