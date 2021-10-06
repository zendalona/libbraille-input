# vim:set et ts=4:
#
# ibus-sharada-braille - The braille ibus engine
#
# Copyright (c) 2014-2015 Nalin.x.GNU <nalin.x.linux@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# if not 1, append datestamp to the version number.
m4_define([package_name], [brailleinput])
m4_define([brailleinput_released], [1])
m4_define([brailleinput_major_version], [1])
m4_define([brailleinput_minor_version], [2])
m4_define([brailleinput_micro_version], [99])
m4_define(brailleinput_maybe_datestamp,
    m4_esyscmd([if test x]brailleinput_released[ != x1; then date +.%Y%m%d | tr -d '\n\r'; fi]))

m4_define([brailleinput_version],
    brailleinput_major_version.brailleinput_minor_version.brailleinput_micro_version[]brailleinput_maybe_datestamp)

AC_INIT([package_name], [brailleinput_version], [http://code.google.com/p/ibus/issues/entry], [package_name])
AM_INIT_AUTOMAKE([1.10])
AC_GNU_SOURCE

AC_CONFIG_HEADERS([config.h])
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])

# define PACKAGE_VERSION_* variables
#AS_VERSION
#AS_NANO
AM_SANITY_CHECK
AM_MAINTAINER_MODE
AM_DISABLE_STATIC
AC_PROG_CC
AM_PROG_CC_C_O
AC_PROG_CXX
AC_ISC_POSIX
AC_HEADER_STDC
AM_PROG_LIBTOOL

AM_PATH_PYTHON(3.3)



# OUTPUT files
AC_CONFIG_FILES(
Makefile
brailleinput/Makefile
built-in-braille-tables/Makefile
liblouis-back-translation-tables/Makefile
built-in-braille-tables/arabic/Makefile
built-in-braille-tables/bengali-bangladesh/Makefile
built-in-braille-tables/bengali-indian/Makefile
built-in-braille-tables/braille-patterns/Makefile
built-in-braille-tables/croatian/Makefile
built-in-braille-tables/czech/Makefile
built-in-braille-tables/danish/Makefile
built-in-braille-tables/dutch/Makefile
built-in-braille-tables/emoji/Makefile
built-in-braille-tables/english/Makefile
built-in-braille-tables/english-grade-2/Makefile
built-in-braille-tables/finnish/Makefile
built-in-braille-tables/french/Makefile
built-in-braille-tables/georgian/Makefile
built-in-braille-tables/german/Makefile
built-in-braille-tables/hindi/Makefile
built-in-braille-tables/hungarian/Makefile
built-in-braille-tables/italian/Makefile
built-in-braille-tables/kannada/Makefile
built-in-braille-tables/lithuanian/Makefile
built-in-braille-tables/malay/Makefile
built-in-braille-tables/malayalam/Makefile
built-in-braille-tables/nepali/Makefile
built-in-braille-tables/norwegian/Makefile
built-in-braille-tables/numerical/Makefile
built-in-braille-tables/polish/Makefile
built-in-braille-tables/portuguese/Makefile
built-in-braille-tables/portuguese-brazil/Makefile
built-in-braille-tables/romanian/Makefile
built-in-braille-tables/russian/Makefile
built-in-braille-tables/sanskrit/Makefile
built-in-braille-tables/serbian/Makefile
built-in-braille-tables/slovak/Makefile
built-in-braille-tables/spanish/Makefile
built-in-braille-tables/swedish/Makefile
built-in-braille-tables/tamil/Makefile
built-in-braille-tables/turkish/Makefile
built-in-braille-tables/ukrainian/Makefile
)

AC_OUTPUT
