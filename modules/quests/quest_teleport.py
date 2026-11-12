##
# quest_teleport.py
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

import quest
import Vector
import VS
import unit
import universe
import vsrandom
import quest_explore
class quest_teleport (quest.quest):
    def __init__ (self):
        self.sysfile = VS.getSystemFile()
        self.timer = VS.GetGameTime()
        self.explorequest=quest_explore.quest_explore_factory().create()
        self.explorequest.setsystem('gemini_sector/delta')
    def teleportNPC (self,un):
        pos=un.Position()
        rsiz = un.rSize()
        size=4*rsiz
        sig = unit.getSignificant (vsrandom.randrange(0,50),0,0)
        if (not sig):
            return
        nam = sig.getName()
        if (nam.find ("lackhole")!=-1):
            return
        targetpos = sig.Position()
        arad = sig.rSize()*2+size
        targetpos = Vector.Add(targetpos,(vsrandom.uniform(arad,arad*1.5),
                                          vsrandom.uniform(arad,arad*1.5),
                                          vsrandom.uniform(arad,arad*1.5)))
        targetpos = VS.SafeEntrancePoint (targetpos,rsiz)
        if (size<1000):
            size=1000
        print("kill")
        print(un.getName())
        un.SetCurPosition(targetpos)
        VS.playAnimation("warp.ani",pos,size)
        VS.playSound("cloak.wav",pos,(1,0,0))
        VS.playAnimation("warp.ani",targetpos,size)
        VS.playSound("cloak.wav",targetpos,(1,0,0))
    def teleportPlayer(self,un):
        if (un.DockedOrDocking()):
            print("YOWWW")
        else:
            if (vsrandom.randrange(0,3)==0):
                (adj,test) = universe.getAdjacentSystems(self.sysfile,1)
                un.JumpTo(adj)
            else:
                self.teleportNPC (un)
    def teleportUnit (self,un):
        nam = un.getName()
        if ((nam.find ("lackhole")!=-1) or  un.isSun()):
            return
        if (un.isPlayerStarship()==-1):
            self.teleportNPC(un)
        else:
            self.teleportPlayer(un)
    def Execute (self):
        self.explorequest.Execute()
        if (VS.getSystemFile()==self.sysfile):
            mytime = VS.GetGameTime();
            if (mytime-self.timer>10):
                self.timer=mytime
                numunits=VS.getNumUnits()
                if (numunits>0):
                    self.teleportUnit(VS.getUnit(vsrandom.randrange(0,numunits)))
        return 1

class quest_teleport_factory (quest.quest_factory):
    def __init__ (self):
        quest.quest_factory.__init__ (self,"quest_teleport")
    def create (self):
        return quest_teleport()
