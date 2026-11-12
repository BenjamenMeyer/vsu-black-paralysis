#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# process_includes.py
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

import sys

if len(sys.argv) <= 1:
    print("Usage: process_includes.py <file1> .. <filen>")
    print("Will create <file1>.pp .. <filen>.pp")
    sys.exit(0)

def process(path, outfile, processed):
    if '/' in path:
        dirname = path[:path.rfind('/')]
    else:
        dirname = "."
    processed.add(path)
    infile = open(path, "r")
    for lineno,line in enumerate(infile):
        if line.startswith('#include "'):
            incpath = dirname + "/" + line[10:line.find('"',10)]
            if incpath not in processed:
                outfile.write("#line 1\n")
                print("  including", incpath)
                process(incpath, outfile, processed)
                outfile.write("\n#line %d\n" % (lineno+1))
            else:
                outfile.write("\n")
        else:
            outfile.write(line)

for path in sys.argv[1:]:
    print("Processing", path)
    outfile = open(path+".pp","w")
    process(path, outfile, set())
