#!/usr/bin/env python
import sys
import os

def make_makefileam(language):
	file_list = os.listdir(os.getcwd()+"/"+language)
	file_list = sorted(file_list)
	text = """###########################################################################
#    SBW - Sharada-Braille-Writer
#
#    Copyright (C) 2012-2014 Nalin <nalin.x.linux@gmail.com>
#    Copyright (C) 2021-2022 Nalin <nalin.x.linux@gmail.com>
#    
#    This project is funded by State Council of Educational Research and Training (S.C.E.R.T) Kerala 
#    Supervised by Zendalona(2021-2022) and Keltron(2012-2014)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

braille_{0}_DATA = \\
	{1}
	$(NULL)
	
braille_{0}dir = $(datadir)/braille-input/built-in-braille-tables/{2}
		
CLEANFILES = \\
	*~ \\
	$(NULL)
""".format(language.replace("-","_"), " \\\n	".join(file_list)+" \\", language)

	open("%s" %(os.getcwd()+"/"+language+"/Makefile.am"),'w').write(text)

for language in sorted(os.listdir(os.getcwd())):
	if(os.path.isdir(language)):
		if(os.path.exists(language+"/Makefile.am")):
			os.remove(language+"/Makefile.am")

		#print(language+"/Makefile") # for configure.ac
		print("built-in-braille-tables/"+language+"/Makefile") # for ../configure.ac 
		#print("	"+language+" \\") # for Makefile.am

		make_makefileam(language)


