##
# log_faction_ships.py
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

import math
import faction_ships
stattable={}
def lg (num):
    return math.log(1+num)/math.log(2)
for i in faction_ships.stattableexp:
    tuple = faction_ships.stattableexp[i]
    stattable[i]=(tuple[0],tuple[1],lg(tuple[2]),lg(tuple[3]),lg(tuple[4]))
    stattable[i+'.rgspec']=(tuple[0],tuple[1]*.8,lg(tuple[2])*.8,lg(tuple[3])*.8,lg(tuple[4])*.8)
    stattable[i+'.milspec']=(tuple[0],tuple[1]*.65,lg(tuple[2])*.65,lg(tuple[3])*.65,lg(tuple[4])*.65)
    stattable[i+'.stock']=(tuple[0],tuple[1]*.5,lg(tuple[2])*.5,lg(tuple[3])*.5,lg(tuple[4])*.5)
    stattable[i+'.blank']=(tuple[0],tuple[1]*.1,lg(tuple[2])*.1,lg(tuple[3])*.1,lg(tuple[4])*.1)
    stattable[i+'.civvie']=(tuple[0],tuple[1]*.2,lg(tuple[2])*.2,lg(tuple[3])*.2,lg(tuple[4])*.2)
print(stattable)
