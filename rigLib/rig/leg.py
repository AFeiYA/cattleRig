"""
cattle leg rig.
"""
import maya.cmds as cmds
from rigLib.utils.joint import listJointHierarchy, duplicateJointChain
from rigLib.base.control import Control
from cattleRig import project
from rigLib.utils.name import renamePrefix,removePrefix
from rigLib.utils import autoFK
from rigLib.base import module


def build(
        legJoints=['Jt_upperLeg_LF', 'Jt_knee_LF', 'Jt_ankle_LF'],
        poleVector="Ctrl_poleVector_LF",
        scapulaJnt="Jt_scapula_L",
        footControl="Ctrl_Foot_LeftFront",
        name="Leg_LeftFront",
        fkRootParent="Ctrl_Chest",
        base=None
):

    # create scapula IK handles
    if scapulaJnt:
        endEffectorJoint=cmds.listRelatives(scapulaJnt, c=True)[0]
        scapulaIk = cmds.ikHandle(n=scapulaJnt + '_ikHandle', sol='ikSCsolver', sj=scapulaJnt, ee=endEffectorJoint)[0]
        cmds.parent(scapulaIk, base.ikGrp)

        # make control.
        scapulaControl = renamePrefix(endEffectorJoint)
        cmds.pointConstraint(scapulaControl, scapulaIk, mo=True)
        cmds.orientConstraint(scapulaControl, endEffectorJoint, mo=True)

    fkJoints = autoFK.build(legJoints[0],  replaceWith="fkJnt_")
    ikJoints = autoFK.build(legJoints[0],  replaceWith="ikJnt_")

    fkControls = []
    for legJnt in listJointHierarchy(legJoints[0]):
        set_constraint_weight_expression(legJnt, type='orientConstraint', blendControl="%s.IKFK" % footControl)


    if scapulaJnt:
        fkContrl0 = Control(prefix=removePrefix(fkJoints[0]), scale=20, translateTo=fkJoints[0],
                            rotateTo=fkJoints[0], parent=fkRootParent, lockChannels=["t", "s", "v"])
        fkContrl1 = Control(prefix=removePrefix(fkJoints[1]), scale=8, translateTo=fkJoints[1],
                            rotateTo=fkJoints[1], parent=fkContrl0.C, lockChannels=["t", "s", "v"])
        fkContrl2 = Control(prefix=removePrefix(fkJoints[2]), scale=8, translateTo=fkJoints[2],
                            rotateTo=fkJoints[2], parent=fkContrl1.C, lockChannels=["t", "s", "v"])
        fkContrl3 = Control(prefix=removePrefix(fkJoints[3]), scale=8, translateTo=fkJoints[3],
                            rotateTo=fkJoints[3], parent=fkContrl2.C, lockChannels=["t", "s", "v"])




        #cmds.parent(fkContrl0.Off, scapulaControl)
        cmds.parentConstraint(endEffectorJoint, fkContrl0.Off, mo=True)
        cmds.parentConstraint(fkContrl0.C, fkJoints[0], mo=True)
        cmds.parentConstraint(fkContrl1.C, fkJoints[1], mo=True)
        cmds.parentConstraint(fkContrl2.C, fkJoints[2], mo=True)
        cmds.parentConstraint(fkContrl3.C, fkJoints[3], mo=True)
    else:
        fkContrl0 = Control(prefix=removePrefix(fkJoints[0]), scale=20, translateTo=fkJoints[0],
                            rotateTo=fkJoints[0], parent=fkRootParent, lockChannels=["t", "s", "v"])
        fkContrl1 = Control(prefix=removePrefix(fkJoints[1]), scale=18, translateTo=fkJoints[1],
                            rotateTo=fkJoints[1], parent=fkContrl0.C, lockChannels=["t", "s", "v"])
        fkContrl2 = Control(prefix=removePrefix(fkJoints[2]), scale=8, translateTo=fkJoints[2],
                            rotateTo=fkJoints[2], parent=fkContrl1.C, lockChannels=["t", "s", "v"])
        fkContrl3 = Control(prefix=removePrefix(fkJoints[3]), scale=8, translateTo=fkJoints[3],
                            rotateTo=fkJoints[3], parent=fkContrl2.C, lockChannels=["t", "s", "v"])
        fkContrl4 = Control(prefix=removePrefix(fkJoints[4]), scale=8, translateTo=fkJoints[4],
                            rotateTo=fkJoints[4], parent=fkContrl3.C, lockChannels=["t", "s", "v"])
        cmds.parentConstraint(fkContrl0.C, fkJoints[0], mo=True)
        cmds.parentConstraint(fkContrl1.C, fkJoints[1], mo=True)
        cmds.parentConstraint(fkContrl2.C, fkJoints[2], mo=True)
        cmds.parentConstraint(fkContrl3.C, fkJoints[3], mo=True)
        cmds.parentConstraint(fkContrl4.C, fkJoints[4], mo=True)

    cmds.connectAttr("%s.IKFK" % footControl, "%s.v" % fkContrl0.Off, force=True)
    # create leg IK handles.
    legIK = cmds.ikHandle(n=legJoints[0] + '_ikHandle', sol='ikRPsolver', sj=ikJoints[0], ee=ikJoints[-3])[0]
    cmds.parent(legIK, base.ikGrp)
    cmds.poleVectorConstraint(poleVector, legIK)
    cmds.parent(poleVector+"_grp", base.controlGrp)


    # make foot reverse joints
    #   1. duplicate foot joints, reverse the hierarchy
    joints = listJointHierarchy(ikJoints[-3])
    joints.reverse()
    reverseJnts = duplicateJointChain(joints, originalString="ikJnt_", replaceWith="reversedJnt_")
    #   2. offset toe tap pivot
    cmds.move(7, "%s.scalePivot" % reverseJnts[0], "%s.rotatePivot" % reverseJnts[0], r=True)
    #   3. make constraint
    cmds.pointConstraint(reverseJnts[2], legIK, mo=True)
    cmds.orientConstraint(reverseJnts[0], joints[1], mo=True)
    cmds.orientConstraint(reverseJnts[1], joints[2], mo=True)
    # make toe tap
    cmds.connectAttr(footControl+".ToeTap", reverseJnts[0]+".rz")

    #  parent controls
    cmds.parent(reverseJnts[0], footControl)
    cmds.parent(footControl, base.controlGrp)

    # make pole vector connection line
    pvLinePos1 = cmds.xform(ikJoints[1], q=1, t=1, ws=1)
    pvLinePos2 = cmds.xform(poleVector, q=1, t=1, ws=1)
    poleVectorCrv = cmds.curve(n=poleVector+'_curve', d=1, p=[pvLinePos1, pvLinePos2])
    cmds.cluster(poleVectorCrv + '.cv[0]', n=name + 'Pv1_cls', wn=[ikJoints[1], ikJoints[1]], bs=True)
    cmds.cluster(poleVectorCrv + '.cv[1]', n=name + 'Pv2_cls', wn=[poleVector, poleVector], bs=True)

    cmds.setAttr(poleVectorCrv + '.template', 1)
    cmds.setAttr(poleVectorCrv + '.it', 0)

    cmds.parent(poleVectorCrv, base.controlGrp)





def set_constraint_weight_expression(object, type='orientConstraint', blendControl=""):
    """
    create expression for two constraints. The second value is equal to 1 minus the first one.
    Then connect the blendControl to the first value.
    eg: weight1 = 1 - weight0. attr_a is weight0  attr_b is weight1,
    shape is the constraint type. eg: joint_skin_{num}_parentConstraint1.attr_a_W0
    :param object: constraint object.
    :type: constraint type.
    """
    constraint_node = cmds.listConnections(object, type=type, shapes=True)[0]
    attr_weight0 = cmds.listAttr(constraint_node, string='*W0')[0]
    attr_weight1 = cmds.listAttr(constraint_node, string='*W1')[0]
    expression_str = '{0}.{2} = 1 - {0}.{1};'.format(constraint_node, attr_weight0, attr_weight1)
    cmds.expression(s=expression_str)
    if blendControl:
        cmds.connectAttr(blendControl, constraint_node+".%s" % attr_weight0)
