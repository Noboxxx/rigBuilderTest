from rigBuilderComponents import RData, RComp, RObj
from maya import cmds
import os


def buildDecorator(func):
    def wrapper(*args, **kwargs):
        cmds.file(new=True, force=True)
        result = func(*args, **kwargs)
        return result
    return wrapper


@buildDecorator
def build():
    # data
    currentLocation = os.path.dirname(os.path.abspath(__file__))

    # guides
    guidesFile = RData.MatrixFile(os.path.join(currentLocation, 'guides.json'))
    guidesFile.import_()
    guides = guidesFile.load()

    # import geo
    geoPath = os.path.join(currentLocation, 'HumanBody.ma')
    meshes = [node for node in cmds.file(geoPath, i=True, returnNewNodes=True) if cmds.objectType(node, isAType='mesh')]

    # base
    baseComp = RComp.RBaseComponent(ctrlSize=50.0)

    # hips
    hipsComp = RComp.RCtrlComponent(name='hips', matrix=guides['hips'], ctrlSize=20.0)

    # components
    comps = (
        baseComp,
        hipsComp
    )

    # connections
    RObj.createMatrixConstraint(
        (baseComp.outputs[1],),
        hipsComp.inputs[0]
    )

    # finalize
    assetGrp = cmds.group(empty=True, name='ass')

    rigGrp = cmds.group(empty=True, name='rig')
    modGrp = cmds.group(empty=True, name='mod')
    cmds.parent(meshes, modGrp)

    cmds.parent(modGrp, rigGrp, assetGrp)

    for comp in comps:
        cmds.parent(comp.folder, rigGrp)



