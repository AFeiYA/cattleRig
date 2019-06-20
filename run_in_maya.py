import sys

custom_path = r'E:\Rigging\rigging\code'
if not custom_path in sys.path:
    sys.path.append(custom_path)

import cattleRig
import rigLib

reload(cattleRig.cattle)
reload(cattleRig.cattle_deform)
reload(rigLib.base.module)
reload(rigLib.base.control)
reload(cattleRig.cattle_deform)
reload(rigLib.utils.joint)
reload(rigLib.rig.spine)
reload(rigLib.rig.neck)
reload(rigLib.rig.head)
reload(rigLib.rig.tail)
reload(rigLib.utils.name)
reload(rigLib.rig.leg)
reload(rigLib.utils.autoFK)

category = cattleRig.project.category[0]
characterName = 'ANML_FC6_Cattle_Basic_Cuban'

# cattleRig.cattle_deform.saveSkinWeights(characterName=characterName)
modelFileFullPath = '{0}/{1}/{2}/model/{2}_model.ma'.format(cattleRig.project.projectPath, category, characterName)
builderFileFullPath = '{0}/{1}/{2}/builder/{2}_builder.ma'.format(cattleRig.project.projectPath, category, characterName)
# print (modelFileFullPath)
# print (builderFileFullPath)
cattleRig.cattle.build(characterName=characterName)





