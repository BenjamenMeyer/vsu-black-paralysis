##
# ====================================================================
# @file   : CMakeLists.txt
# @brief  : CMake configuration file for Vega Strike: Black Paralysis
# ====================================================================
#
# Vega Strike: Black Paralysis - Space Simulation, Combat and Trading
# Copyright (C) 2026 Benjamen R. Meyer, and other Vega Strike contributors.
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

CMAKE_MINIMUM_REQUIRED(VERSION 3.21 FATAL_ERROR)

SET(vsuBP_VERSION_MAJOR "0")
SET(vsuBP_VERSION_MINOR "1")
SET(vsuBP_VERSION_PATCH "0")

# Auto-populate with the git hash of the build
IF (DEFINED ENV{SHORT_SHA} AND NOT "$ENV{SHORT_SHA}" STREQUAL "")
    SET(vsuBP_GIT_HASH "$ENV{SHORT_SHA}")
ELSE ()
    EXECUTE_PROCESS(
        COMMAND git rev-parse --short HEAD
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        OUTPUT_VARIABLE vsuBP_GIT_HASH
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
ENDIF ()

SET(vsuBP_VERSION_LONG_STR "${vsuBP_VERSION_MAJOR}.${vsuBP_VERSION_MINOR}.${vsuBP_VERSION_PATCH}-${vsuBP_GIT_HASH}")
SET(vsuBP_VERSION_SHORT_STR "${vsuBP_VERSION_MAJOR}.${vsuBP_VERSION_MINOR}.${vsuBP_VERSION_PATCH}")
SET(vsuBP_PKG_VERSION_STR "${vsuBP_VERSION_MAJOR}.${vsuBP_VERSION_MINOR}.${vsuBP_VERSION_PATCH}")

PROJECT(vsuBP
    VERSION
        "${vsuBP_VERSION_MAJOR}.${vsuBP_VERSION_MINOR}.${vsuBP_VERSION_PATCH}"
)

MESSAGE("== Vega Strike Universe: Black Paralysis Version: ${vsuBP_VERSION_LONG_STR}")

# Let cmake find our in-tree modules
SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Detect available Linux Distros that can be built for
FIND_PACKAGE(LinuxDistro REQUIRED)

INCLUDE(GNUInstallDirs)

SET(CPACK_IGNORE_FILES
    build/
    packages/
    \\\\.git/
    \\\\.vs/
    \\\\.vscode/
    ".*\\\\.pyc"
    ".*~"
    ".*\\\\.swp"
    "migration_plan\\\\.md"
)
SET(CPACK_SOURCE_IGNORE_FILES
    "/[.]git/"
    "/build/"
    "/packages/"
    "/\\.vs/"
    "/\\.vscode/"
    "\\.pyc$"
    "~$"
    "\\.swp$"
    "migration_plan\\.md"
)

# Install asset directories
INSTALL(DIRECTORY .black-paralysis/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/.black-paralysis)

INSTALL(DIRECTORY ai/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/ai
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY animations/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/animations
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY bases/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/bases
        PATTERN "*.swp" EXCLUDE
        PATTERN "*~" EXCLUDE
        PATTERN "__pycache__" EXCLUDE)

INSTALL(DIRECTORY cockpits/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/cockpits
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY communications/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/communications)

INSTALL(DIRECTORY meshes/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/meshes
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY mission/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/mission)

INSTALL(DIRECTORY modules/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/modules
        PATTERN "*.swp" EXCLUDE
        PATTERN "*~" EXCLUDE
        PATTERN "__pycache__" EXCLUDE)

INSTALL(DIRECTORY programs/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/programs
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY python/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/python
        PATTERN "*.swp" EXCLUDE
        PATTERN "*~" EXCLUDE
        PATTERN "__pycache__" EXCLUDE)

INSTALL(DIRECTORY sectors/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/sectors)

INSTALL(DIRECTORY sounds/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/sounds
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY sprites/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/sprites
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY techniques/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/techniques
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY textures/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/textures
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY units/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/units
        PATTERN "*.am" EXCLUDE)

INSTALL(DIRECTORY universe/ DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis/universe)

# Install root asset files
INSTALL(FILES Version.txt DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES New_Game DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES factions.xml DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES LICENSE DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES engine.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES bindings.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES theme.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES controls.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES config.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES master_part_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES master_component_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES master_asteroid_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES master_ship_list.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES weapons.json DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
INSTALL(FILES weapon_list.xml DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)

# Platform-specific desktop integration and launcher installation
IF (CMAKE_SYSTEM_NAME STREQUAL Linux)
    INSTALL(FILES black-paralysis.desktop DESTINATION share/applications)
    INSTALL(FILES black-paralysis.png DESTINATION share/pixmaps)
    INSTALL(FILES black-paralysis.xpm DESTINATION share/pixmaps)
    INSTALL(PROGRAMS scripts/vsuBlackParalysis DESTINATION ${CMAKE_INSTALL_BINDIR})
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Windows)
    INSTALL(FILES favicon.ico DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
    INSTALL(FILES vega.ico DESTINATION ${CMAKE_INSTALL_DATADIR}/black-paralysis)
    INSTALL(PROGRAMS scripts/vsuBlackParalysis DESTINATION ${CMAKE_INSTALL_BINDIR})
ELSE ()
    INSTALL(PROGRAMS scripts/vsuBlackParalysis DESTINATION ${CMAKE_INSTALL_BINDIR})
ENDIF ()

# CPack Packaging Configuration
SET(CPACK_VERBATIM_VARIABLES YES)
SET(CPACK_PACKAGE_NAME "vsuBP")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Vega Strike Universe: Black Paralysis mini-game assets")
SET(CPACK_PACKAGE_VENDOR "Vega Strike")
SET(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
SET(CPACK_PACKAGE_VERSION_MAJOR "${vsuBP_VERSION_MAJOR}")
SET(CPACK_PACKAGE_VERSION_MINOR "${vsuBP_VERSION_MINOR}")
SET(CPACK_PACKAGE_VERSION_PATCH "${vsuBP_VERSION_PATCH}")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "vsuBP-${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}")
SET(CPACK_CONTACT "maintainers@vega-strike.org")

# Source package filename
IF (DEFINED ENV{TAG_NAME})
    SET(vsuBP_PACKAGE_VERSION_STR "$ENV{TAG_NAME}")
ELSE (DEFINED ENV{TAG_NAME})
    SET(vsuBP_PACKAGE_VERSION_STR "${vsuBP_VERSION_MAJOR}.${vsuBP_VERSION_MINOR}.${vsuBP_VERSION_PATCH}-0.${vsuBP_GIT_HASH}")
ENDIF (DEFINED ENV{TAG_NAME})

SET(CPACK_PACKAGE_VERSION "${vsuBP_PACKAGE_VERSION_STR}")
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${vsuBP_PACKAGE_VERSION_STR}-Source")
SET(CPACK_SOURCE_GENERATOR "TXZ")

IF (CMAKE_SYSTEM_NAME STREQUAL Windows)
    MESSAGE(STATUS "Configuring Packaging for Windows")
    SET(CPACK_PACKAGE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\favicon.ico")
    SET(CPACK_NSIS_DISPLAY_NAME "Vega Strike Universe: Black Paralysis")
    SET(CPACK_NSIS_MANIFEST_DPI_AWARE true)
    SET(CPACK_NSIS_ENABLE_UNINSTALL_BEFORE_INSTALL YES)
    SET(CPACK_NSIS_HELP_LINK "https://vega-strike.org")
    SET(CPACK_NSIS_URL_INFO_ABOUT "https://vega-strike.org/about")
    SET(CPACK_NSIS_CONTACT "maintainers@vega-strike.org")
    SET(CPACK_NSIS_MODIFY_PATH OFF)
    SET(CPACK_NSIS_CREATE_ICONS_EXTRA
        "CreateShortCut '$SMPROGRAMS\\\\$STARTMENU_FOLDER\\\\Vega Strike Universe - Black Paralysis.lnk' 'C:\\\\Program Files\\\\VegaStrike-0.10\\\\bin\\\\vegastrike-engine.exe' -D\"$INSTDIR\\\\share\\\\black-paralysis\""
    )
    SET(CPACK_NSIS_DELETE_ICONS_EXTRA
        "Delete '$SMPROGRAMS\\\\$START_MENU\\\\Vega Strike Universe - Black Paralysis.lnk'"
    )
    SET(CPACK_GENERATOR "NSIS64")
    SET(CPACK_PACKAGE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/packages")
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${vsuBP_PACKAGE_VERSION_STR}_Windows_${CMAKE_SYSTEM_VERSION}_${CMAKE_SYSTEM_PROCESSOR}")
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Darwin)
    MESSAGE(STATUS "Configuring Packaging for macOS")
    SET(CPACK_GENERATOR "DragNDrop")
    SET(CPACK_PACKAGE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/packages")
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${vsuBP_PACKAGE_VERSION_STR}_macOS_${CMAKE_SYSTEM_VERSION}_${CMAKE_SYSTEM_PROCESSOR}")
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Linux)
    MESSAGE(STATUS "Configuring Packaging for Linux")
    SET(CPACK_GENERATOR "TXZ")

    # Debian Package
    IF (VS_CAN_BUILD_DEB)
        MESSAGE(STATUS "Configuring Debian Packaging")
        SET(CPACK_DEBIAN_PACKAGE_NAME "vsubp")
        SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "maintainers@vega-strike.org")
        SET(CPACK_DEBIAN_COMPRESSION_TYPE "xz")
        SET(CPACK_DEBIAN_PACKAGE_DEPENDS "vega-strike")
        SET(CPACK_PACKAGE_FILE_NAME "${CPACK_DEBIAN_PACKAGE_NAME}_${vsuBP_PACKAGE_VERSION_STR}")
        SET(CPACK_DEBIAN_PACKAGE_SECTION "games")
        SET(CPACK_DEBIAN_PACKAGE_HOMEPAGE "https://www.vega-strike.org")
        SET(CPACK_GENERATOR "DEB")
    ENDIF ()

    # RPM Package
    IF (VS_CAN_BUILD_RPM)
        MESSAGE(STATUS "Configuring RPM Packaging")
        SET(CPACK_RPM_PACKAGE_LICENSE "GPLv2")
        SET(CPACK_RPM_PACKAGE_URL "https://www.vega-strike.org")
        SET(CPACK_RPM_PACKAGE_NAME "vsuBP")
        SET(CPACK_RPM_PACKAGE_REQUIRES "vega-strike")

        IF (LINUX_CODENAME)
            SET(vsuBP_LINUX_VERSION_STR "${LINUX_CODENAME}")
        ELSE (LINUX_CODENAME)
            SET(vsuBP_LINUX_VERSION_STR "${LINUX_VERSION_ID}")
        ENDIF (LINUX_CODENAME)

        SET(CPACK_PACKAGE_FILE_NAME "${CPACK_RPM_PACKAGE_NAME}_${vsuBP_PACKAGE_VERSION_STR}-${LINUX_ID}-${vsuBP_LINUX_VERSION_STR}")
        SET(CPACK_GENERATOR "RPM")
    ENDIF ()
ELSE ()
    MESSAGE(STATUS "Configuring Packaging for Unknown Platform - \"${CMAKE_SYSTEM_NAME}\"")
    SET(CPACK_GENERATOR "TXZ")
ENDIF ()

INCLUDE(CPack)
