# -*- coding: utf-8 -*-
"""
    overholt.manage.tags
    ~~~~~~~~~~~~~~~~~~~~~
    tag management commands
"""

from ..services import tags


def CreateTagCommand():
    """Create a tag"""
    print("creating tag")
    try:
        tags.create(serial='YWJjZGVm', secretkey='AAAACCCC')
    except:
        pass
