##
# save_util.py
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

import Director

def loadStringList (playernum,mykey):
    lengt = Director.getSaveDataLength (playernum,mykey)
    if (lengt<1):
        return []
    rez = []
    curstr = []
    curstr_append = curstr.append
    lengt = Director.getSaveData(playernum,mykey,0)
    for i in range (1,lengt+1):
        myint=Director.getSaveData (playernum,mykey,i)
        if myint:
            curstr_append(myint)
        else:
            rez.append("".join(map(chr,curstr)))
            del curstr[:]
    return rez
def saveStringList (playernum,mykey,names):
    ord_ = ord
    length = Director.getSaveDataLength (playernum,mykey)
    k=1
    tot=0
    for i in range (len (names)):
        tot += len (names[i])+1
    if (length==0):
        Director.pushSaveData(playernum,mykey,tot)
    else:
        Director.putSaveData(playernum,mykey,0,tot)
    for i in range (len (names)):
        for j,c in enumerate (names[i]):
            if (k < length):
                Director.putSaveData(playernum,mykey,k,ord_(c))
            else:
                Director.pushSaveData(playernum,mykey,ord_(c))
            k+=1
        if (k < length):
            Director.putSaveData(playernum,mykey,k,0)
        else:
            Director.pushSaveData(playernum,mykey,0)
        k+=1
