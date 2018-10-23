# Copyright (C) 2015 Sebastian Herbord.  All rights reserved.
# Copyright (C) 2016 - 2018 Mod Organizer contributors.
#
# This file is part of Mod Organizer.
#
# Mod Organizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mod Organizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mod Organizer.  If not, see <http://www.gnu.org/licenses/>.
import logging
import os.path
import sys


program_files_folders = [os.environ['ProgramFiles(x86)'],
    os.environ['ProgramFiles'],
    os.environ['ProgramW6432'],
    "C:\\",
    "D:\\"]

def qt_inst_path():
    from config import config
    if config['binary_qt']:
        qt_inst_path = config["paths"]["qt_binary_install"]
    else:
        qt_inst_path = "{}/qt5".format(config['paths']['build']).replace("/", os.path.sep)
    return qt_inst_path

def cmake_parameters():
    from config import config

    boost_version = config['boost_version']
    vc_version = config['vc_version_for_boost']
    boost_tag_version = ".".join([_f for _f in [boost_version, config['boost_version_tag']] if _f])

    paths_build = config['paths']['build']

    cmake_parameters = ["-DCMAKE_BUILD_TYPE={}".format(config["build_type"]),
                        "-DDEPENDENCIES_DIR={}".format(paths_build),
                        "-DBOOST_ROOT={}\\boost_{}".format(paths_build, boost_tag_version.replace(".", "_")),
                        "-DBoost_LIBRARY_DIRS={}\\boost_{}\\lib{}-msvc-{}\\lib".format(paths_build, boost_tag_version.replace(".", "_"),"64" if config['architecture'] == 'x86_64' else "32",vc_version),
                        "-DLOOT_API_PATH={}\\lootapi-{}-{}".format(paths_build, config["loot_version"], config["loot_commit"]),
                        "-DLZ4_ROOT={}\\lz4-v{}".format(paths_build, ".".join([_f for _f in [config["lz4_version"], config['lz4_version_minor']] if _f])),
                        "-DQT_ROOT={}".format(qt_inst_path()),
                        "-DZLIB_ROOT={}\\\zlib-{}".format(paths_build, config["zlib_version"])]

    if config.get('optimize', False):
        cmake_parameters.append("-DOPTIMIZE_LINK_FLAGS=\"/LTCG /INCREMENTAL:NO /OPT:REF /OPT:ICF\"")
    return cmake_parameters

def bitness():
    from config import config
    return "x64" if config['architecture'] == "x86_64" else "Win32"
