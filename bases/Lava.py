##
# Lava.py
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

landing = Base.Room ('Landing Pad')
Base.Texture (landing, 'tex', 'bases/Lava/landing.sprite', 0, 0)
Base.Ship (landing, 'ship', (-0.3, -0.3, 10/shipsize), (0, 0.93, -0.34), (-1, 0, -1))

landscape = Base.Room ('Planet Exterior')
Base.Texture (landscape, 'tex', 'bases/Lava/landscape.sprite', 0, 0)

Base.Link (landing, 'ExtLink', 0.40, 0.02, 0.30, 0.22, 'Planet Exterior', landscape)
Base.Link (landscape, 'Landing', -0.5, -1, 1, 0.2, 'Landing Pad', landing)
Base.LaunchPython (landing, 'launch','bases/launch_music.py', -0.5, -0.5, 0.5, 0.3, 'Launch Your Ship')
