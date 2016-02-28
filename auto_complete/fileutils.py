import os
import string

def get_fs_drives():
    drives = []
    for letter in string.ascii_lowercase:
        drive = '{}:\\'.format(letter)
        try:
            os.listdir(drive)
            drives.append(drive)
        except WindowsError:
            pass
    return drives

def get_dirpaths(root, depth=5):
    """Get any dir path till required depth"""
    paths = []
    paths.append(root)
    if depth <= 0:
        return []
    try:
        files = os.listdir(unicode(root))
    except WindowsError as e:
        # print 'Error:', e.strerror, e.filename
        return []
    files = [os.path.join(root, f) for f in files]
    for f in files:
        if os.path.isdir(f):
            paths.extend(get_dirpaths(f, depth-1))
    return paths

def find2(root):
    """Some things are best recursive

    Procedural skeleton version of recursive find_file_type_paths
    This code is difficult to write, read, extend and maintain.

    Another non-recursive solution would be to run depth-first.

    In essence, each iteration would run only on single depth eg.
    depth 1, check for file types and gather all folders on the
    current depth. Next iteration for depth+1 would run on collected
    folders and so on.
    """
    for d1 in os.listdir(root):
        for d2 in os.listdir(d1):
            for d3 in os.listdir(d2):
                for d4 in os.listdir(d3):
                    for d5 in os.listdir(d4):
                        pass

def find_file_type_paths(root, depth=5, suff=('py', 'java')):
    """Get dir paths having file of given file type(s)

    Search in particular dir stops as soon as either target
    file is found or maximum depth is reached.

    Note - result dir paths include only leading portion of
    directories with target files. It does not include complete
    listing of dirs and subdirs.
    """
    paths = []
    if depth <= 0:
        return []

    try:
        _files = os.listdir(unicode(root))
    except WindowsError as e:
        # print 'Error:', e.strerror, e.filename
        return []

    files = []
    dirs = []
    for f in _files:
        f = os.path.join(root, f)
        if os.path.isfile(f):
            files.append(f)
        else:
            dirs.append(f)

    for f in files:
        if os.path.isfile(f):
            if os.path.splitext(f)[1].lstrip('.') in suff:
                # print '[hit]', f
                # stop search once root yields target file type
                return [root]

    for d in dirs:
        paths.extend(find_file_type_paths(d, depth-1))
    return paths

def dump_file(fname):
    try:
        with open(fname) as fp:
            content = fp.read()
    except IOError:
        print 'Could not dump file content for {}'.format(fname)
    else:
        print '[file dump] {}'.format(content)

def clear_file(fname):
    with open(fname, 'w') as fp:
        pass

