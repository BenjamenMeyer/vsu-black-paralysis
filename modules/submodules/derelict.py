##
# derelict.py
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

import Vector
import vsrandom
import VS

def launchNewDerelict(name, ship_type):
    player = VS.getPlayer()
    if(player == None):
        return 0
    
    # get the player's position
    vec = player.Position()
    # set derelict position approximately 10000m away from the player.
    # TODO: make configurable
    vec = Vector.Add(vec,(10000,0,0))
    vec = Vector.Add (vec,(vsrandom.uniform(-2000,2000),
                            vsrandom.uniform(-2000,2000),
                            vsrandom.uniform(-2000,2000)))
    
    # launch the derelict.
    derelict = VS.launch(name, ship_type,"neutral","unit","default",1,1,vec,'')
    derelict.Derelict()

    # get rid of all orders, so that strange maneouvers don't happen
    derelict.PrimeOrders()

    return 0
