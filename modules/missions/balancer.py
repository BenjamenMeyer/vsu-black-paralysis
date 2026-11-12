# -*- coding: utf-8 -*-
##
# balancer.py
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

import VS
import Director
import launch
from Vector import Add

class balancer (Director.Mission):
    loops=()
    def __init__ (self, ships, num_ships=1, num_waves=1):
        Director.Mission.__init__(self)
        you = VS.getPlayer()
        for i in range(len(ships)):
            launch.launch(you.getFlightgroupName(), you.getFactionName(), ships[i], "ai_sitting_duck.py", num_ships, num_waves, Add(you.Position(),((i+1)*500,0,0)), '', False)
            print((" ++ Balancer mission launching %s unit..."%ships[i]))
        launch.launch(you.getFlightgroupName(), you.getFactionName(), "Archimedes", "ai_sitting_duck.py", num_ships, num_waves, Add(you.Position(),(0,0,8000)), '', False)
        print(" ++ Balancer mission launching the playground")

    def Execute(self):
        pass
