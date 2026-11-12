#!/usr/bin/python
##
# webpageize.py
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

import os
import sys
index=0
fp=0
def makeWebPage(fp,index):
    if (fp):
        fp.write("\n</body>\n</html>\n");
        fp.close();
    fp = open (str(index/10)+".html","w")
    fp.write('<html>\n<head>\n<title>Pictures from Hong Kong</title>\n</head>\n<body vlink="#001e73" link="#001e73" bgcolor="#ffffff" text="#000000">\n');
    return fp

for args in sys.argv:
    print (args)
    if (index%20==0):
        fp = makeWebPage(fp,index);
    index+=1
    if (index==1):
        continue
    os.system("xview -zoom 50 "+args+" &")
    first = sys.stdin.readline()
    if (first=="x\n"):
        continue
    second= sys.stdin.readline()
    fp.write('<br><br><b>\n'+first+'</b>')
    fp.write('<br><img src="'+args+'" width="1024"/>')
    fp.write("<br>"+second+"<br>")
