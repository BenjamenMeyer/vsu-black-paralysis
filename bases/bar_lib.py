##
# bar_lib.py
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
import vsrandom
import fixers
def MakeBar (room,time_of_day='_day',bartext='bases/bartender_default.py', BaseTexture="bases/generic/bar"):
    bar = Base.Room ('Bar')
    Base.Texture (bar, 'tex', BaseTexture+'.spr', 0, 0)
    Base.Python (bar, 'talk', -0.138672, -0.127604, 0.306641, 0.341146, 'Talk to the Bartender',bartext,0)
    Base.Link (bar, 'Back', -0.998047, -0.997396, 2, 0.28125, 'Exit the Bar', room)
    Base.Comp (bar, 'newscomp', 0.505859, 0.153646, 0.248047, 0.328125, 'GNN News', 'News')
    i=vsrandom.randrange(0,20)
    file='bases/generic/bartender%d.spr' % (i)
    Base.Texture(bar,'bartender',file,0,-0.0035)
    fixers.CreateFixers(bar,[(-.65,-.815,.25,.667),
                        (.525,-.815,.25,.667),
                        #(-1.05,-.974,.25,.667),
                        ])
    return bar
