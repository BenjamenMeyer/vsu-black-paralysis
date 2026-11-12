##
# faceoff.py
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
class faceoff (Director.Mission):
    def __init__(self):
        VS.SetDifficulty(0.1)
        Director.Mission.__init__(self)
        self.lasttime=-100
        self.waittime=100.0
        self.launchShip("nova","confed")
        self.launchShip("nova","confed")
        self.launchShip("revoker","pirates")
        self.launchShip("revoker","pirates")
        self.launchShip("revoker","pirates")

    def launchShip (self,type,faction):
        return launch.launch_wave_around_unit("Shadow",faction,type,"default",1,100.0,2000.0,VS.getPlayer(),'')
    def launch_new_wave(self):
        side = vsrandom.randrange(0,2)
        faction="confed"
        ai = vsrandom.randrange(0,2)
        if (ai==0):
            ai = "printhello.py"
        else:
            ai = "default"
        if (side==0):
            faction=faction_ships.get_enemy_of("confed")
        else:
            faction=faction_ships.get_friend_of("confed")
        launched = launchShip(faction_ships.getRandomFighter(faction),faction);

    def Execute (self):
        time = VS.GetGameTime()
        if (time-self.lasttime>self.waittime):
            #self.launch_new_wave()
            VS.IOmessage (0,"game","all","[Confed] This is a test of the emergency broadcast system.")
            self.lasttime=time
