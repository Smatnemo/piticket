import os.path as osp

def get_filename(name):
    """Return absolute path to a picture located in the current package.

    :param name: name of an image located in pitcures/assets
    :type name: str

    :return: absolute image path
    :rtype: str
    """
    return osp.join(osp.dirname(osp.abspath(__file__)), 'assets', name)