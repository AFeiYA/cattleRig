"""
This is a module for making control objects
"""

import maya.cmds as cmds
import maya.mel as mel


class Control():
    """
    create a control object
    """
    def __init__(self, 
                 prefix='name',
                 scale=1.0,
                 translateTo="",
                 rotateTo="",
                 parent="",
                 shape="",
                 lockChannels=["s", "v"]):
        """
        :param prefix: the name of the control
        :param scale: float,
        :param translateTo:
        :param rotateTo:
        :param parent:
        :param lockChannels:
        """
        if shape == "octahedron":
            melString = "curve -d 1 -p 0 0 1 -p 1 0 0 -p 0 0 -1 -p -1 0 0 -p 0 0 1" \
                        " -p 0 1 0 -p 1 0 0 -p 0 -1 0 -p 0 0 -1 " \
                        "-p 0 1 0 -p -1 0 0 -p 0 -1 0 -p 0 0 1 " \
                        "-k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;" \
                        "scale -r {0} {0} {0} ;" \
                        "makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;".format(scale)

            mel.eval(melString)
            ctrlObject = cmds.rename(cmds.ls(sl=1)[0], "Ctrl_"+prefix)
        else:
            ctrlObject = cmds.circle(n="Ctrl_"+prefix, ch=False, normal=[1, 0, 0], radius=scale)[0]

        ctrlOffset = cmds.group(n="Ctrl_"+prefix+"_grp", em=1)
        cmds.parent(ctrlObject, ctrlOffset)

        # color control
        ctrlShape = cmds.listRelatives(ctrlObject, s=1)[0]
        ctrlShapeCheck = ctrlShape.lower()
        cmds.setAttr(ctrlShape+".ove", 1)
        if "_l" in ctrlShapeCheck:
                cmds.setAttr(ctrlShape+".ovc", 14)
        elif "_r" in ctrlShapeCheck:
                cmds.setAttr(ctrlShape+".ovc", 13)
        else:
                cmds.setAttr(ctrlShape+".ovc", 22) 

        # translate control
        if cmds.objExists(translateTo):
                cmds.delete(cmds.pointConstraint(translateTo, ctrlOffset))

        # rotate control
        if cmds.objExists(rotateTo):
                cmds.delete(cmds.orientConstraint(translateTo, ctrlOffset))

        # parent control
        if cmds.objExists(parent):
                cmds.parent(ctrlOffset, parent)

        # lock control channels
        attributes_to_lock = []
        for lock_channel in lockChannels:
                if lock_channel in ['t', 'r', 's']:
                        for axis in ['x', 'y', 'z']:
                                attr = lock_channel+axis
                                attributes_to_lock.append(attr)

        for attr in attributes_to_lock:
                cmds.setAttr(ctrlObject+"."+attr, lock=1, k=0)

        self.C = ctrlObject
        self.Off = ctrlOffset

    def adjustControlPosition(self, x=0, y=0, z=0):
        """
        adjust the points position of the control object.
        :param x: the distance will be adjusted in x axis.
        :param y: the distance will be adjusted in y axis.
        :param z: the distance will be adjusted in z axis.
        :return: None
        """
        ctrlShape = cmds.listRelatives(self.C, s=1, type="nurbsCurve")[0]
        cmds.move(x, y, z, ctrlShape + ".cv[*]", r=True, os=True, wd=True)

