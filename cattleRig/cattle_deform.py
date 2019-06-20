"""
deformation setup
"""

import maya.cmds as cmds
from . import project
from rigTools import bSkinSaver
import os

skinWeightsFolder = 'weights'
skinWeightExt = '.swt'


def build(characterName):
    modelGrp = "ANML_FC6_Cattle_Basic_Cuban_Geo"

    geoList = getModelGeoObjects(modelGrp)
    loadSkinWeights(characterName, geoList)


def getModelGeoObjects(modelGrp):
    geoList = [cmds.listRelatives(o, p=1)[0] for o in cmds.listRelatives(modelGrp, ad=1, type='mesh')]
    return geoList


def saveSkinWeights(characterName, geoList=[]):
    """
    save skin weight information.
    :param characterName: string
    :param geoList: Select skinned mesh in scene to save.
    :return:None.
    """
    geoList = cmds.ls(sl=True)
    # TODO automatically find skinned mesh in scene. Then export.
    if geoList:
        for geo in geoList:
            cmds.listHistory()
            # save weights file
            wtFile = os.path.join(project.projectPath,
                                  project.category[0],
                                  characterName,
                                  skinWeightsFolder,
                                  geo+skinWeightExt)
            print (wtFile)
            cmds.select(geo)
            bSkinSaver.bSaveSkinValues(wtFile)
    else:
        cmds.warning("No mesh has been selected.")


def loadSkinWeights(characterName, geoList=[]):
    """
    load skin weights automatically based on the name.
    :param characterName: string. To locate the character folder.
    :param geoList: target object.
    :return: None.
    """
    wtDir = os.path.join(project.projectPath, project.category[0], characterName, skinWeightsFolder)
    wtFiles = os.listdir(wtDir)

    for wtFile in wtFiles:
        fileName, fileExt = os.path.splitext(wtFile)
        if fileExt == skinWeightExt:
            if cmds.objExists(fileName):
                inputFile = os.path.join(wtDir, wtFile)
                bSkinSaver.bLoadSkinValues(loadOnSelection=False, inputFile=inputFile)
            else:
                cmds.error("%s is not exist, skin load skipped." % fileName)
        else:
            cmds.warning('%s is not a skin weight file, skipped.' % fileName)




