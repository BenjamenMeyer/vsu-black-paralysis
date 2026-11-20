# package.ps1
#
# Copyright (C) 2026 Vega Strike Contributors
#
# This file is part of Vega Strike: Black Paralysis ("vsuBP").
#
# vsuBP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# vsuBP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vsuBP.  If not, see <https://www.gnu.org/licenses/>.

try {
    cmake --build .\build --target package
}
catch {
    Write-Error "Package target build failed: $_"
    $logFiles = Get-ChildItem -Path .\packages\_CPack_Packages -Filter "NSISOutput.log" -Recurse -ErrorAction SilentlyContinue
    foreach ($log in $logFiles) {
        Write-Host "=== Output from $($log.FullName) ==="
        Get-Content $log.FullName
    }
    throw
}

