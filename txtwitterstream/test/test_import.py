import os

root_dir = __package__.split(".")[0]

for (dirpath, dirnames, filenames) in os.walk(root_dir):
    for filename in (filename for filename in filenames if filename.endswith('.py')):
        dirs = dirpath.split("/")
        if filename != "__init__.py":
            dirs.append(filename[:-3])
        import_str = "%s" % ".".join(dirs)
        if import_str not in ("setup", __name__):
            print "import %s" % import_str
            __import__(import_str)
        
    if "test" in dirnames:
        dirnames.remove("test")