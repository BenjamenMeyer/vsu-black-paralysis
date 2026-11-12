##
# MiningBase__rlaan.py
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

import Base
import VS

shipsize = VS.getPlayer().rSize()/35
#print "Ship Size: " + str(shipsize) #debug

# rooms
landing = Base.Room ('Landing Pad')
Base.Texture (landing, 'tex', 'bases/Rlaan_Star_Fortress/rlaan_landing.sprite', 0, 0)
# ship size is inverse proportional!
Base.Ship (landing, 'ship_l', (-0.3, -0.5, 5/shipsize), (0.00, 0.90, -0.20), (-0.7, 0, -0.7))

Base.LaunchPython (landing, 'launch','bases/launch_music.py', -0.5, -0.5, 0.5, 0.3, 'Launch Your Ship')

# computer terminals
Base.Comp (landing, 'my_comp_id', -0.75, -0.35, 0.30, 0.22, 'Computer', 'Info Missions News Upgrade Cargo ShipDealer')
