"""
spine rig,  hips included.
"""

#from .. base import module
import maya.cmds as cmds
from rigLib.utils.name import removePrefix, renameSuffix
from rigLib.utils.joint import duplicateJointChain


def build(
        spineJoints=['Jt_spine', 'Jt_spine1', 'Jt_spine2', 'Jt_spine3', 'Jt_spine4'],
        prefix="spine",
        spineCurve="spine_SpIk_CV",
        chestControl = "Ctrl_Chest",
        middleControl = "Ctrl_Spine_Mid",
        pelvisControl = "Ctrl_hip",
        pelvisJoint="Jt_pelvis",
        bodyControl = "Ctrl_root",
        base=None
):
    """
    :param spineJoints: list(spine_name), list of spine joints.
    :param rootJnt: string, root joint
    :param endJnt: string, end joint
    :param spineCurve:
    :return:
    """



    dpFkJoints = duplicateJointChain(spineJoints)
    spineCurveCVs = cmds.ls(spineCurve+'.cv[*]', fl=1)
    spineCurveClusters = []

    for i in range(len(spineCurveCVs)):
        cluster = cmds.cluster(spineCurveCVs[i], n=prefix+"%d_cluster" % i)[1]
        spineCurveClusters.append(cluster)
    cmds.group(spineCurveClusters, name=spineCurve+"_cls_grp", parent=base.noTransformGrp)
    cmds.parent(spineCurve, base.noTransformGrp)
    cmds.parent(dpFkJoints[0], base.controlGrp)
    # cmds.hide(spineCurveClusters)
    # print spineCurveClusters

    spineIK = cmds.ikHandle(
        n=renameSuffix(spineCurve, "ikHandle"),
        sol="ikSplineSolver",
        sj=spineJoints[0], ee=spineJoints[-1],
        c=spineCurve, ccv=0, parentCurve=0)[0]
    cmds.parent(spineIK, base.ikGrp)

    # enable twist.
    cmds.setAttr(spineIK+".dTwistControlEnable", 1)
    cmds.setAttr(spineIK+".dWorldUpType", 4)
    cmds.connectAttr(chestControl+".worldMatrix[0]", spineIK+".dWorldUpMatrixEnd")
    cmds.connectAttr(pelvisControl+".worldMatrix[0]", spineIK+".dWorldUpMatrix")

    # constraint clusters.
    cmds.parentConstraint(spineCurveClusters[0], spineCurveClusters[1], mo=True)
    cmds.parentConstraint(pelvisControl, spineCurveClusters[0], mo=True)
    cmds.parentConstraint(dpFkJoints[0], spineCurveClusters[2], mo=True)
    cmds.parentConstraint(dpFkJoints[1], spineCurveClusters[3], mo=True)
    cmds.parentConstraint(dpFkJoints[2], spineCurveClusters[4], mo=True)
    cmds.parentConstraint(dpFkJoints[3], spineCurveClusters[5], mo=True)
    cmds.parentConstraint(dpFkJoints[4], spineCurveClusters[6], mo=True)
    cmds.parentConstraint(dpFkJoints[4], spineCurveClusters[7], mo=True)

    # control setup
    cmds.parentConstraint(pelvisControl, dpFkJoints[0], mo=True)
    cmds.parentConstraint(middleControl, dpFkJoints[1], mo=True)
    cmds.parentConstraint(middleControl, dpFkJoints[2], mo=True)
    cmds.parentConstraint(middleControl, dpFkJoints[3], mo=True)
    cmds.parentConstraint(chestControl, dpFkJoints[4], mo=True)
    # chestControl offset grp
    constraint = cmds.parentConstraint(middleControl, chestControl+"_grp", mo=True)[0]
    cmds.connectAttr(chestControl+".Lock", constraint+".%sW0" % middleControl)


    # root
    cmds.parentConstraint(bodyControl, "Jt_root", mo=True)
    cmds.parent(bodyControl, base.controlGrp)

    # pelvis .
    cmds.parentConstraint(pelvisControl, pelvisJoint, mo=True)
    # cmds.parentConstraint(pelvisControl, dpFkJoints[0], mo=True)
    # chest
    cmds.orientConstraint(chestControl, spineJoints[-1], mo=True)






