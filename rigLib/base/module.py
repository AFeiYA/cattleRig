"""
module for making top rig structure and rig module.
"""


import maya.cmds as cmds
from . import control

sceneObjectType = 'rig'


class Base:

    def __init__(self,
                characterName='name',
                scale=1.0):
        self.topGrp = cmds.group(n=characterName + "_Node", em=1)
        self.rigGrp = cmds.group(n="rig_grp", em=1, p=self.topGrp)
        self.modelGrp = cmds.group(n="model_grp", em=1, p=self.topGrp)
        self.globalControlGrp = cmds.group(n='globalControl_grp', em=1, p=self.rigGrp)
        self.globalScaleGrp = cmds.group(n='globalScale_grp', em=1, p=self.globalControlGrp)

        # add custom scene information, normally used for pipeline.
        characterNameAttr = 'characterName'
        sceneObjectTypeAttr = sceneObjectType

        for attr in [characterNameAttr, sceneObjectTypeAttr]:
            cmds.addAttr(self.topGrp, ln=attr, dt='string')
        cmds.setAttr(self.topGrp + "." + characterNameAttr, characterName, type='string', lock=1)
        cmds.setAttr(self.topGrp + "." + sceneObjectTypeAttr, sceneObjectType, type='string', lock=1)

        # groups
        self.skinJointGrp = cmds.group(n='skin_joints_group', em=1, p=self.globalScaleGrp)
        self.ikGrp = cmds.group(n='IKs_grp', em=1, p=self.globalScaleGrp)
        self.controlGrp = cmds.group(n='controls_grp', em=1, p=self.globalScaleGrp)
        self.noTransformGrp = cmds.group(n='noTransform_grp', em=1, p=self.rigGrp)
        cmds.setAttr(self.noTransformGrp+'.it', 0, lock=1)





