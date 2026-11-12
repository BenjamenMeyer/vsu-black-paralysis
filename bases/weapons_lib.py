##
# weapons_lib.py
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

def MakeWeapon (room, time_of_day='_day'):
    weap = Base.Room ('Weapons Room')
    Base.Texture (weap, 'tex', 'bases/generic/weapon.spr', 0, 0)
    Base.Comp (weap, 'comp', 0.5, -0.4, 0.5, 0.765625, 'Upgrade your Ship', 'Upgrade Info ShipDealer')
    Base.Link (weap, 'Back', -0.998047, -0.997396, 2, 0.28125, 'Exit the Weapons Room', room)
    Base.Link (weap, 'Back', -1, -1, .5, 2, 'Exit the Weapons Room', room)

    return weap
