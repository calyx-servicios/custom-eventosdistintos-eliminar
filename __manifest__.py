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
    'name': 'Custom ED',
    'version': '11.0.1',
    'category': 'Tools',
    'author': "Calyx",
    'website': 'www.calyxservicios.com.ar',
    'license': 'AGPL-3',
    'summary': '''Eventos Distintos Customization''',
    'depends': [
        'base',
        #'web_calendar',
        'calendar',
        'crm'
    ],
    'external_dependencies': {
    },
    'data': [
        'view/calendar_view.xml',
        'view/lead_view.xml',
        'view/color_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
