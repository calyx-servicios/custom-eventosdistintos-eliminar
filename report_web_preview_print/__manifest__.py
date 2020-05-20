# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2019  Calyx  (http://www.calyxservicios.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Open & Print PDF Reports in Browser",
    "version": "11.0.1.1",
    "summary": """Open & Print PDF Reports in Browser""",
    "author": "Calyx",
    "category": "Productivity",
    "license": "LGPL-3",
    "website": "www.calyxservicios.com.ar",
    "description": """
    Preview and print pdf reports in browser instead of downloading them.
    Based in [prt_report_attachment_preview] By: Ivan Sokolov, Cetmix.
""",
    "depends": ["base", "web"],
    "data": [
        "views/prt_report_preview_template.xml",
        "views/ir_actions_report.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
