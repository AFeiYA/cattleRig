"""
Utilities to name objects

"""


def removePrefix(name):
    """
    Remove suffix form given name string.
    :param  name str
    :return str, name without prefix.
    """
    edits = name.split('_')
    if len(edits) < 2:
        return name
    prefix = edits[0] + '_'
    nameWithNoPrefix = name[len(prefix):]
    return nameWithNoPrefix

def removeSuffix(name):
    """
    Remove suffix form given name string.
    :param  name str
    :return str, name without suffix.
    """
    edits = name.split('_')
    if len(edits)<2:
        return name
    suffix = '_' + edits[-1]
    nameWithNoSuffix = name[:-len(suffix)]
    return nameWithNoSuffix


def renameSuffix(name, suffix='ctrl'):
    """
    Rename suffix form given name string.
    :param  name str
    :param suffix, new suffix name, default call ctrl
    :return str, name new suffix.
    """
    newName = removeSuffix(name=name)+"_"+suffix
    return newName


def renamePrefix(name, prefix='Ctrl'):
    newName = prefix+"_"+removePrefix(name=name)
    return newName
