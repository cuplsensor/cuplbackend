# -*- coding: utf-8 -*-
"""
    overholt.manage.boxes
    ~~~~~~~~~~~~~~~~~~~~~
    box management commands
"""

from ..services import boxes


def CreateBoxCommand():
    """Create a box"""
    print("creating box")
    try:
        boxes.create(serial='YWJjZGVm', secretkey='AAAACCCC')
    except:
        pass
