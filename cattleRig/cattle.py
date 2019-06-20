

from rigLib.base import module
import maya.cmds as cmds
from . import project
from . import cattle_deform
from rigLib.rig import spine, leg, neck, head, tail


sceneScale = project.sceneScale
projectPath = project.projectPath
category = project.category[0]

modelFilePath = '{0}/{1}/{2}/model/{2}_model.ma'  # {0}:project path,{1}: category,sub-folder. {2}:characterName
builderFilePath = '{0}/{1}/{2}/builder/{2}_builder.ma'
modelGroupName = "ANML_FC6_Cattle_Basic_Cuban_Geo"
rootJointName = "root"


def build(characterName):
    """
    build character rig.
    :param characterName: string.
    :return: None
    """
    # create a new scene.
    cmds.file(new=True, f=True)

    # make a base hierarchy.
    base = module.Base(characterName=characterName, scale=sceneScale)

    # import model file
    modelFile = modelFilePath.format(projectPath, category, characterName)
    cmds.file(modelFile, i=True)

    # import builder file
    builderFile = builderFilePath.format(projectPath, category, characterName)
    cmds.file(builderFile, i=True)

    # parent models to modelGrp in base node.
    if cmds.objExists(modelGroupName):
        cmds.parent(modelGroupName, base.modelGrp)
    else:
        cmds.error("No group called %s, please name the model group correctly!" % modelGroupName)

    # parent joints to skinJointGrp in base node.
    if cmds.objExists(rootJointName):
        cmds.parent(rootJointName, base.skinJointGrp)
    else:
        cmds.error("No joint called %s, please name the root joint correctly!" % rootJointName)

    # build deform
    cattle_deform.build(characterName)

    # build spine
    spine.build(base=base)

    # build neck
    neck.build(base=base)

    # build head
    head.build(base=base)

    # build legs
    #   left front leg.
    leg.build(
            legJoints=['Jt_upperLeg_LF', 'Jt_knee_LF', 'Jt_ankle_LF'],
            poleVector="Ctrl_poleVector_LF",
            scapulaJnt="Jt_scapula_L",
            footControl="Ctrl_Foot_LeftFront",
            name="Leg_LeftFront",
            fkRootParent="Ctrl_Chest",
            base=base
    )

    #   right front leg
    leg.build(
            legJoints=['Jt_upperLeg_RF', 'Jt_knee_RF', 'Jt_ankle_RF'],
            poleVector="Ctrl_poleVector_RF",
            scapulaJnt="Jt_scapula_R",
            footControl="Ctrl_Foot_RightFront",
            name="Leg_RightFront",
            fkRootParent="Ctrl_Chest",
            base=base
    )
    #   left back leg.
    leg.build(
            legJoints=['Jt_hip_LB', 'Jt_upperLeg_LB', 'Jt_knee_LB', 'Jt_ankle_LB'],
            poleVector="Ctrl_poleVector_LB",
            scapulaJnt="",
            footControl="Ctrl_Foot_LeftBack",
            name="Leg_LeftBack",
            fkRootParent="Ctrl_hip",
            base=base
    )
    #   right back leg
    leg.build(
            legJoints=['Jt_hip_RB', 'Jt_upperLeg_RB', 'Jt_knee_RB', 'Jt_ankle_RB'],
            poleVector="Ctrl_poleVector_RB",
            scapulaJnt="",
            footControl="Ctrl_Foot_RightBack",
            name="Leg_RightBack",
            fkRootParent="Ctrl_hip",
            base=base
    )

    #
    tail.build(base=base)

    # clean up scene disp
    # lock attrs
    cmds.connectAttr("Ctrl_global.t", base.globalControlGrp+".t")
    cmds.connectAttr("Ctrl_global.r", base.globalControlGrp+".r")
    cmds.connectAttr("Ctrl_global.s", base.globalScaleGrp+".s")
    cmds.parent("Ctrl_global_grp", base.controlGrp)
    lock_attrs = "tx ty tz rx ry rz sx sy sz v".split()
    for attr in lock_attrs:
        cmds.setAttr(base.globalScaleGrp+"."+attr, lock=True, k=0)
        cmds.setAttr(base.globalControlGrp + "." + attr, lock=True, k=0)
    # hide some groups
    cmds.hide(base.ikGrp)
    cmds.hide(base.noTransformGrp)
    cmds.delete("ANML_FC6_Cattle_Basic_Cuban_bulider")
    cmds.hide(base.skinJointGrp)









