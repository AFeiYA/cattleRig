"""
tail rig
"""
import maya.cmds as cmds
from rigLib.base.control import Control
from rigLib.utils.name import removePrefix
from rigLib.utils.joint import listJointHierarchy


def build(
        tailRootJoint="Jt_tail",
        tailCurve="tail_SpIK_CV",
        base=None
):

    tailRootCtrl = Control(prefix=removePrefix(tailRootJoint),
                           scale=8,
                           translateTo=tailRootJoint,
                           rotateTo=tailRootJoint,
                           parent=base.controlGrp,
                           lockChannels=["t", "s"])

    cmds.parentConstraint(cmds.listRelatives(tailRootJoint, p=True, type="joint")[0], tailRootCtrl.Off, mo=True)

    tailJoints = listJointHierarchy(tailRootJoint)
    # cluster tail curve.
    tailCurveCvs = cmds.ls(tailCurve+".cv[*]", fl=1)
    tailCurveClusters = []

    for i in range(len(tailCurveCvs)):
        cluster = cmds.cluster(tailCurveCvs[i], n=tailCurve+"_cluster%d" % i)[1]
        tailCurveClusters.append(cluster)

    cmds.parent(tailCurve, base.noTransformGrp)
    tailControls = []
    for i in range(len(tailCurveCvs)):
        ctrl = Control(prefix="tail"+"%s" % i, translateTo=tailCurveClusters[i],
                       scale=3, parent=base.controlGrp, shape="octahedron")
        ctrl.adjustControlPosition(x=0, y=8, z=0)
        cmds.parentConstraint(tailRootCtrl.C, ctrl.Off, mo=True)
        tailControls.append(ctrl)

    for i in range(len(tailCurveCvs)):
        cmds.parent(tailCurveClusters[i], tailControls[i].C)

    tailIk = cmds.ikHandle(n=tailCurve + '_ikhandle', sol='ikSplineSolver', sj=tailJoints[0], ee=tailJoints[-1],
                           c=tailCurve, ccv=0, parentCurve=0)[0]

    cmds.parent(tailIk, base.ikGrp)

    twistAt = 'twist'
    cmds.addAttr(tailControls[-1].C, ln=twistAt, k=1)
    cmds.connectAttr(tailControls[-1].C+".%s" % twistAt, "%s.twist" % tailIk)
    cmds.hide(tailControls[0].Off)
    cmds.hide(tailCurveClusters)
