#!/usr/bin/env python
# Copyright (C) 2012 Enrico Rossi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Change working directory so relative paths (and template lookup) work again
import sys
import os
import bottle

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))

import blueshop

# ... build or import your bottle application here ...
# Do NOT use bottle.run() with mod_wsgi

application = blueshop.app

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
