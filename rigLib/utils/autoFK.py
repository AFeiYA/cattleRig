
import maya.cmds as cmds
from rigLib.utils.joint import listJointChain, listJointHierarchy, duplicateJointChain, duplicateJointHierarchy


def build(topJoint='Jt_hip_RB', tipJoint='', originalString='Jt_', replaceWith="fkJnt_"):
    """
    create fk joints , do orient constraint.
    :param topJoint: the root joint of the joint hierarchy .
    :param tipJoint: the last joint of the joint chain.
    :param originalString: prefix in joint orignal name
    :param replaceWith: new prefix name of the joint.
    :return: fk joint name list.
    """
    # make fk joints.
    if not tipJoint:
        skinJoints = listJointHierarchy(topJoint, withEndJoints=True)
        fkJoints = duplicateJointHierarchy(topJoint, originalString=originalString, replaceWith=replaceWith)

    else:
        skinJoints = listJointChain(topJoint=topJoint, endJnt=tipJoint)
        # duplicate fk joint chain
        fkJoints = duplicateJointChain(skinJoints, originalString=originalString, replaceWith=replaceWith)

    # orient constraint joints.
    for skJnt, fkJnt in zip(skinJoints, fkJoints):
        cmds.orientConstraint(fkJnt, skJnt)

    return fkJoints

