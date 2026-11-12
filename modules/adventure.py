##
# adventure.py
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


##
# VS is only for news
#


import VS
import quest
import vsrandom
import quest_surplus
import quest_drone
import quest_tutorial
import quest_dispute
import quest_blockade
import quest_shipyardbomb
import quest_slaver
import quest_debug
#import quest_racene #need rewrite
#import quest_disappear #need rewrite
#import quest_rlaan_spy #need rewrite
#import quest_rogue_militia #need rewrite
#import quest_contraband_truck #need rewrite
#import quest_isowing #need rewrite

adventures = {}
persistent_adventures = list()

adventures = {
    #"Crucible/Cephid_17":quest_debug.quest_debug_factory(), # enable for debugging only
    "Crucible/Cephid_17":quest_tutorial.quest_tutorial_factory(),
    "Sol/Regallis":quest_dispute.quest_dispute_factory(),
    "Crucible/Elohim":quest_blockade.quest_blockade_factory(),
    "Sol/Alpha_Centauri":quest_shipyardbomb.quest_shipyardbomb_factory(),
    "Sol/Iris":quest_slaver.quest_slaver_factory(),
#       "Crucible/Cephid_17":quest_drone.quest_drone_factory(),
#       "Enigma/callimanchius":quest_surplus.quest_surplus_factory(('Supplies/Medical','Research/Environmental',),1.5,.5,0,1,('callimanchius_disaster',),),
#       "Sol/alpha_centauri":quest_surplus.quest_surplus_factory(('Supplies/Construction_Supplies','Manufactured_Goods',),1.5,.5,0,1,('holman_population',),),
#       "Enigma/racene":quest_racene.quest_racene_factory(),
#       "Enigma/defiance":quest_isowing.quest_isowing_factory(),
#       "Enigma/axis":quest_disappear.quest_disappear_factory(),
#       "Enigma/novaya_kiev":quest_rlaan_spy.quest_rlaan_spy_factory(),
#       "Enigma/heinlein":quest_rogue_militia.quest_rogue_militia_factory(),
#       "Enigma/klondike":quest_contraband_truck.quest_contraband_truck_factory(),
#       "Crucible/Cephid_17":quest_teleport.quest_teleport_factory(),
    }

persistent_adventures = [
    #quest_debug.quest_debug_factory(), # for debugging
    #quest_tutorial.quest_tutorial_factory(),
    #quest_drone.quest_drone_factory(),
    #quest_isowing.quest_isowing_factory()]
        ]

def removePersistentAdventure(newq):
    mylen = len(persistent_adventures)
    if (mylen):
        for x in range (mylen):
            if (persistent_adventures[x]==newq):
                del persistent_adventures[x]
                return

def newAdventure(playernum,oldsys,newsys):
    newfac=adventures.get (newsys)
    if (newfac):
        newq = newfac.factory(playernum)
        if (newq):#only remove it if that player hasn't done it before
            del adventures[newsys]
            removePersistentAdventure(newfac)
        return newq
    return
#that returns false

def persistentAdventure(playernum):
    for index in range (len(persistent_adventures)):
        ret = persistent_adventures[index].persistent_factory(playernum)
        if (ret):
            del persistent_adventures[index]
            return ret
    if (vsrandom.randrange(0,4)==0):
        (key,val,news)=quest_surplus.makeSurplusShortage()
        if (not adventures.get(key)):
            adventures.setdefault(key,val)
            VS.IOmessage (0,"game","news",news)
    return
