
"""
joint utility functions.
"""

import maya.cmds as cmds


def listJointHierarchy(topJoint, withEndJoints=True):
    listedJoints = cmds.listRelatives(topJoint, type="joint", ad=True)
    listedJoints.append(topJoint)
    listedJoints.reverse()
    if not withEndJoints:
        for jnt in listedJoints:
            if not cmds.listRelatives(jnt, type="joint"):
                print jnt+" has no child"
                listedJoints.remove(jnt)
    return listedJoints


def listJointChain(topJoint, endJnt):
    """

    :param topJoint: start joint in the chain.
    :param endJnt: end joint in the chain.
    :return: joint list  from start to end.
    """
    child = endJnt
    depth = 0
    joints = []
    while depth < 200 and child != topJoint:
        joints.append(child)
        child = cmds.listRelatives(child, p=True)[0]
        depth += 1
    joints.append(topJoint)
    joints.reverse()
    return joints


# duplicate joint and rename
def duplicateJointChain(joints, originalString='Jt_', replaceWith='fkJnt_', reverseHierarchy=False):
    """
    duplicate a joint chain with new name.
    :param joints: a joints list.
    :param originalString: Joint in the list should contain string "Jt_"
    :param replaceWith: Rename the duplicate joint with new string.
    :param reverseHierarchy:  reverse the joint hierarchy
    :return: duplicated joints list
    """
    finalJoints = []
    for jnt in joints:
        dpJnt = cmds.duplicate(jnt, po=True, rc=True)
        if originalString in jnt:
            fJnt = cmds.rename(dpJnt, jnt.replace(originalString, replaceWith))
        else:
            fJnt = cmds.rename(dpJnt, "AutoJtPrefix_" + jnt)
        finalJoints.append(fJnt)
    for i in range(1, len(finalJoints)):
        if reverseHierarchy:
            cmds.parent(finalJoints[i-1], finalJoints[i])
        else:
            cmds.parent(finalJoints[i], finalJoints[i-1])
    cmds.parent(finalJoints[0], w=True)
    return finalJoints


def duplicateJointHierarchy(topJoint='', originalString='Jt_', replaceWith='fkJnt_'):
    """
    duplicate joint hierarchy with new name.
    :param topJoint: a root joint.
    :param originalString: Joint in the hierarchy should contain string "Jt_"
    :param replaceWith: Rename the duplicate joint with new string.
    :return: list, duplicated joint hierarchy
    """
    if topJoint:
        dpRootJnt = cmds.duplicate(topJoint, rc=True)[0]
        dpJoints = listJointHierarchy(dpRootJnt, withEndJoints=True)
        originalJoints = listJointHierarchy(topJoint, withEndJoints=True)
        finalJoints = []
        for jnt, dpJnt in zip(originalJoints, dpJoints):
            if originalString in jnt:
                fJnt = cmds.rename(dpJnt, jnt.replace(originalString, replaceWith))
            else:
                fJnt = cmds.rename(dpJnt, "NoJtPrefix_"+jnt)
            finalJoints.append(fJnt)
        return finalJoints
    else:
        pass
