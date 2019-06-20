import maya.cmds as cmds
from rigLib.utils.joint import listJointHierarchy
from rigLib.base.control import Control
from rigLib.utils.name import removePrefix


def build(
        headControl="Ctrl_head",
        headJoint="Jt_head",
        jawJoint="Jt_jaw",
        leftEyeJoint="Jt_eye_L",
        rightEyeJoint="Jt_eye_R",
        leftEarJoint="Jt_ear_L",
        leftEar1Joint="Jt_ear1_L",
        rightEarJoint="Jt_ear_R",
        rightEar1Joint="Jt_ear1_R",
        base = None
):

    cmds.orientConstraint(headControl, headJoint, mo=True)
    # joints = listJointHierarchy(headJoint, withEndJoints=False)
    # joints.pop(0)
    # for jnt in joints:
    #     ctrl = Control(prefix=removePrefix(jnt), scale=15, translateTo=jnt, rotateTo=jnt, parent=headControl, lockChannels=["t", "s"])

    jawCtrl = Control(prefix=removePrefix(jawJoint), scale=10, translateTo=jawJoint, rotateTo=jawJoint, parent=base.controlGrp, lockChannels=["t", "s"])
    cmds.parentConstraint(headJoint, jawCtrl.Off, mo=True)
    cmds.orientConstraint(jawCtrl.C, jawJoint, mo=True)

    rightEyeCtrl = Control(prefix=removePrefix(rightEyeJoint), scale=4, translateTo=rightEyeJoint, rotateTo="", parent=base.controlGrp, lockChannels=["t", "s"])
    leftEyeCtrl = Control(prefix=removePrefix(leftEyeJoint), scale=4, translateTo=leftEyeJoint, rotateTo="", parent=base.controlGrp, lockChannels=["t", "s"])
    cmds.parentConstraint(headJoint, rightEyeCtrl.Off, mo=True)
    cmds.parentConstraint(headJoint, leftEyeCtrl.Off, mo=True)
    cmds.orientConstraint(rightEyeCtrl.C, rightEyeJoint, mo=True)
    cmds.orientConstraint(leftEyeCtrl.C, leftEyeJoint, mo=True)

    leftEarCtrl = Control(prefix=removePrefix(leftEarJoint), scale=5, translateTo=leftEarJoint, rotateTo=leftEarJoint, parent=base.controlGrp, lockChannels=["t", "s"])
    rightEarCtrl = Control(prefix=removePrefix(rightEarJoint), scale=5, translateTo=rightEarJoint, rotateTo=rightEarJoint, parent=base.controlGrp, lockChannels=["t", "s"])
    cmds.parentConstraint(headJoint, leftEarCtrl.Off, mo=True)
    cmds.parentConstraint(headJoint, rightEarCtrl.Off, mo=True)

    cmds.orientConstraint(leftEarCtrl.C, leftEarJoint, mo=True)
    cmds.orientConstraint(rightEarCtrl.C, rightEarJoint, mo=True)

    leftEar1Ctrl = Control(prefix=removePrefix(leftEar1Joint), scale=6, translateTo=leftEar1Joint, rotateTo=leftEar1Joint, parent=leftEarCtrl.C, lockChannels=["t", "s"])
    rightEar1Ctrl = Control(prefix=removePrefix(rightEar1Joint), scale=6, translateTo=rightEar1Joint, rotateTo=rightEar1Joint, parent=rightEarCtrl.C, lockChannels=["t", "s"])
    cmds.orientConstraint(leftEar1Ctrl.C, leftEar1Joint, mo=True)
    cmds.orientConstraint(rightEar1Ctrl.C, rightEar1Joint, mo=True)







