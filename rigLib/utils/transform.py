"""
utility to manipulate and create transforms
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
import unicodedata
import re
import maya.cmds as cmds

from . import name

def makeOffsetGrp(object, prefix=''):
    if not prefix:
        prefix = name.removeSuffix(object)
    offsetGrp = cmds.group(n=prefix+'_grp', em=1)
    objectParents = cmds.listRelatives(object, p=1)

    if objectParents:
        cmds.parent(offsetGrp, objectParents[0])

    # transform offset group to object.    
    cmds.delete(cmds.parentConstraint(object, offsetGrp))
    cmds.delete(cmds.scaleConstraint(object, offsetGrp))
    cmds.parent(object, offsetGrp)


def match_transform_and_hierarchy(rename_target=False):
    """
    match the target object's position rotation and hierarchy to the source object.
    :param: renameTarget: if false use original name , else create a new one depend on source object.
    :param: select source object, than select target
    :return: none
    """
    objs = cmds.ls(sl=True)
    source = objs[0]
    if rename_target:
        target = cmds.rename(objs[1], name.renameSuffix(objs[0], suffix='ctrl'))
    else:
        target = objs[1]
    source_parent = cmds.listRelatives(source, p=True)
    cmds.delete(cmds.parentConstraint(source, target, mo=False))
    cmds.parent(target, source_parent)


