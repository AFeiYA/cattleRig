import maya.cmds as cmds


def deleteConstraintInScene():
    """
    delete constraint node in scene.
    :return:None
    """
    transforms_objects = cmds.ls(tr=True)
    for obj in transforms_objects:
        if "Constraint" in cmds.nodeType(obj):
            cmds.delete(obj)


def deleteNodeInScene(nodeName):
    nodes = cmds.ls(type=nodeName)
    cmds.delete(nodes)
