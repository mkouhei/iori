# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012, 2013 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import syslog
from __init__ import NAME


def logging(priority, message):
    """

    Arguments:

        priority: syslog priority
        message : log message

    """
    syslog.openlog(NAME, syslog.LOG_PID, syslog.LOG_LOCAL0)
    syslog.syslog(priority, str(message))
    syslog.closelog()
    print(message)
    if priority in range(4):
        # 0: EMERG, 1: ALERT, 2: CRIT, 3: ERR
        exit(1)
    else:
        # 4: WARNING, 5: NOTICE:, 6: INFO, 7: DEBUG
        return True
