"""
neck rig
"""

#from .. base import module
import maya.cmds as cmds
from rigLib.utils.name import removePrefix, renameSuffix
from rigLib.utils.joint import duplicateJointChain


def build(
        neckJoints=['Jt_neck', 'Jt_neck1', 'Jt_neck2', 'Jt_neck3', 'Jt_neck4'],
        prefix="neck",
        neckCurve="neck_SpIK_CV",
        frontControl = "Ctrl_neck1",
        middleControl = "Ctrl_neck",
        headControl = "Ctrl_head",
        neckRootControl="Ctrl_neck_root",
        chestControl ="Ctrl_Chest",
        base=None
):
    """
    :param neckJoints: list(neck_name), list of neck joints.
    :param neckCurve:
    :return:
    """
    dpFkJoints = duplicateJointChain(neckJoints)
    # connect to body
    cmds.parent(dpFkJoints[0], "Jt_spine4")

    neckCurveCVs = cmds.ls(neckCurve+'.cv[*]', fl=1)
    neckCurveClusters = []

    for i in range(len(neckCurveCVs)):
        cluster = cmds.cluster(neckCurveCVs[i], n=prefix+"%d_cluster" % i)[1]
        neckCurveClusters.append(cluster)
    cmds.group(neckCurveClusters, name=neckCurve+"_cls_grp", parent=base.noTransformGrp)
    # cmds.hide(neckCurveClusters)
    # print neckCurveClusters

    neckIK = cmds.ikHandle(
        n=renameSuffix(neckCurve, "ikHandle"),
        sol="ikSplineSolver",
        sj=neckJoints[0], ee=neckJoints[-1],
        c=neckCurve, ccv=0, parentCurve=0)[0]
    cmds.parent(neckIK, base.ikGrp)
    cmds.parent(neckCurve, base.noTransformGrp)

    # constraint clusters.
    cmds.parentConstraint(dpFkJoints[0], neckCurveClusters[0], mo=True)
    cmds.parentConstraint(dpFkJoints[0], neckCurveClusters[1], mo=True)
    cmds.parentConstraint(dpFkJoints[1], neckCurveClusters[2], mo=True)
    cmds.parentConstraint(dpFkJoints[2], neckCurveClusters[3], mo=True)
    cmds.parentConstraint(dpFkJoints[2], neckCurveClusters[4], mo=True)
    cmds.parentConstraint(dpFkJoints[3], neckCurveClusters[5], mo=True)
    cmds.parentConstraint(dpFkJoints[4], neckCurveClusters[6], mo=True)
    cmds.parentConstraint(dpFkJoints[4], neckCurveClusters[7], mo=True)


    # control setup
    cmds.parentConstraint(middleControl, dpFkJoints[2], mo=True)
    cmds.parentConstraint(frontControl, dpFkJoints[3], mo=True)
    cmds.parentConstraint(headControl, dpFkJoints[4], mo=True)

    cmds.parentConstraint(dpFkJoints[0], middleControl+"_grp", mo=True)
    #cmds.parentConstraint(neckRootControl, middleControl+"_grp", mo=True)
    cmds.orientConstraint(neckRootControl, dpFkJoints[0], mo=True)
    cmds.parentConstraint(middleControl, frontControl + "_grp", mo=True)

    cmds.parent(frontControl+"_grp", base.controlGrp)
    cmds.parent(middleControl + "_grp", base.controlGrp)

    # frontControl offset grp
    constraint = cmds.parentConstraint(middleControl, frontControl+"_grp", mo=True)[0]
    cmds.connectAttr(frontControl+".Lock", constraint+".%sW0" % middleControl)

    return dpFkJoints[-1]








