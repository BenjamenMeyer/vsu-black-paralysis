##
# planet_lib.py
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
import dynamic_mission
import VS
def MakePlanet (time_of_day='_day'):
    plist=VS.musicAddList('agricultural.m3u')
    VS.musicPlayList(plist)
    dynamic_mission.CreateMissions()
    room1 = Base.Room ('Scenery')
    Base.Texture (room1, 'tex', 'bases/generic/generic'+time_of_day+'.spr', 0, 0)
    Base.Texture (room1, 'tex', 'bases/generic/holo.spr', -.5, -.4)
    Base.Comp (room1, 'Computer', -0.6, -0.8, .2578906, 0.80833, 'Computer', 'Cargo Upgrade Info ShipDealer News Missions')
    Base.Ship (room1, 'ship', (0,-.5,4), (0,.93,-.34), (-1,0,0))
    Base.LaunchPython (room1, 'launch','bases/launch_music.py', -1, -1, 2, .8, 'Launch Your Ship')

    return room1
