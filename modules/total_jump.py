##
# total_jump.py
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

import vsrandom
import launch
import faction_ships
import VS
import Briefing
import universe
import unit
import Director
class total_jump:
    def __init__(self):
        VS.SetDifficulty(.1)
        self.lasttime=-1000
        self.waittime=5.0
    def launch_new_wave(self):
        un = VS.getPlayer()
        if (vsrandom.randrange(0,4)==0):
            if (un):
                currentsystem = VS.getSystemFile()
                numadj=VS.GetNumAdjacentSystems(currentsystem)
                if (numadj):
                    cursys=VS.GetAdjacentSystem(currentsystem,vsrandom.randrange(0,numadj))
                else:
                    cursys = 'enigma_sector/heavens_gate'
                print("TJ: jumping to "+cursys)
                un.JumpTo(cursys)
            else:
                print("TJ: jumping to [ERROR: you are null]")
            return
        else:
            siglist=universe.significantUnits()
            if len(siglist)==0:
                print("TJ: siglist empty")
                return
            sig=siglist[vsrandom.randrange(0,len(siglist))]
            if (not sig):
                print("TJ: sig null")
                return
            print("TJ: autopiloting to "+sig.getName())
            un.AutoPilotTo(sig,True)
            un.SetTarget(sig)

##        side = vsrandom.randrange(0,2)
##        faction="confed"
##        ai = vsrandom.randrange(0,2)
##        if (ai==0):
##            ai = "printhello.py"
##        else:
##            ai = "default"
##        if (side==0):
##            faction=faction_ships.get_enemy_of("confed")
##        else:
##            faction=faction_ships.get_friend_of("confed")
##        launched = launch.launch_wave_around_unit ("Shadow",faction,faction_ships.getRandomFighter(faction),ai,vsrandom.randrange(1,10),100.0,2000.0,VS.getPlayer(),'')
##        if (vsrandom.randrange(0,10)==0):
##            launch.launch_wave_around_unit ("ShadowCap",faction,faction_ships.getRandomCapitol(faction),ai,1,2000.0,4000.0,VS.getPlayer(),'')
    def Execute (self):
#        un=VS.getUnit(0);
#        i=0
#        while (un):
#            print un.getName()
#            i+=1
#            un=  VS.getUnit(i)
        time = VS.GetGameTime()
        if (time-self.lasttime>self.waittime):
            self.launch_new_wave()
            self.waittime=vsrandom.randrange(10.0,30.0)
            self.lasttime=time
    def initbriefing(self):
        print("ending briefing")
    def loopbriefing(self):
        print("loop briefing")
        Briefing.terminate();
    def endbriefing(self):
        print("ending briefing")
