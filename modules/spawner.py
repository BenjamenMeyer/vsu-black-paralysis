##
# spawner.py
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

from go_to_adjacent_systems import *
from go_somewhere_significant import *
import vsrandom
import launch
import faction_ships
import VS
import Briefing
import universe
import unit
import Vector
import Director
import quest
class spawner (Director.Mission):
    def __init__ (self):
        Director.Mission.__init__(self)

        self.fac=[]
        self.facnames=["ISO",
			"LIHW",
			"aera",
			"andolian",
			"confed",
			"forsaken",
			"highborn",
			"homeland-security",
			"hunter",
			"klkk",
			"luddites",
			"mechanist",
			"merchant",
			"pirates",
			"purist",
			"rlaan",
			"rlaan_briin",
			"shaper",
			"shmrn",
			"unadorned"
			]
        self.facnames=self.facnames+self.facnames
        for i in range(len(self.facnames)):
            nam=self.facnames[i]+"_SPAWN"
            if (i>=len(self.facnames)/2):
                nam+="_CAPSHIP"
            self.fac.append(VS.launchJumppoint(nam,"neutral","75 jump.png %s (ONE ONE)"%nam,"planet","sitting_duck",1,1,Vector.Add((0.,-1000.+i*200.,1000.),VS.getPlayer().Position()),"",""))
        self.delay=VS.GetGameTime()
    def Execute (self):
        if (VS.getPlayer()):
            iter=0
            for base in self.fac:

                if (base.getDistance(VS.getPlayer())<0):
                    if (VS.GetGameTime()-self.delay>10):
                        self.delay=VS.GetGameTime()
                        type=faction_ships.getRandomFighter(self.facnames[iter])
                        if (iter>=len(self.facnames)/2):
                            type=faction_ships.getRandomCapitol(self.facnames[iter])
                        launch.launch_wave_around_unit("Shadow_"+self.facnames[iter],self.facnames[iter],type,"default",1,200,250,VS.getPlayer(),'',0)
                        VS.getPlayer().upgrade("tungsten",0,0,1,0)
                        VS.getPlayer().upgrade("tungsten_hull",0,0,1,0)
                    else:
                        VS.IOmessage(0,"spawner","all","Going to spawn "+self.facnames[iter]+"starships in %d seconds at."%(10-(VS.GetGameTime()-self.delay)))
                iter+=1
