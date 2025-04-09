#Version 11/19/2024; customize 3/4/25
import importlib
"""
This module makes it possible to instance all customized project classes by
a single-line call to instance_project_classes() from a driver script. It saves
doing this with multiple import + instantiation statements in the driver script.
The return from instance_project_classes() is a tuple of the instanced classes.

instance_project_classes() should be customized for each project as appropriate.
"""

def instance_project_classes(IsTest=False, IsParse=False, IsModel=False):
    """
    Instance customized [production-mode] classes for the project
    JDL 11/20/24; customize 3/4/25
    """
    #Tuples of libs aka *.py filename, module/class name) 
    mods_cls_names = [('libs.projfiles', 'Files'), 
                      ('libs.projtables', 'ProjectTables'),
                      ('libs.parse_fns', 'ParseImports')]
    
    #Create a dict of class objects (not yet instanced)
    class_objs = create_class_objs_dict(mods_cls_names)

    #Set a temp name for each class object and then use it to instance the class
    Files = class_objs['Files']
    files = Files(proj_abbrev='', subdir_home='most_recent', IsTest=IsTest, subdir_tests='tests')

    #IsParse and IsModel determine instancing of parsing and/or modeling related Tables
    ProjectTables = class_objs['ProjectTables']
    tbls = ProjectTables(files, IsParse=IsParse, IsModel=IsModel)

    #Custom parsers for ads and sales data
    ParseImports = class_objs['ParseImports']
    parse = ParseImports()

    return files, tbls, parse

def instance_classes_dboard(IsTest=False):
    """
    Instance customized [production-mode] classes for dashboard plots
    JDL 3/20/25
    """
    #Tuples of libs aka *.py filename, module/class name) 
    mods_cls_names = [('libs.projfiles', 'Files'), 
                      ('libs.projtables', 'ProjectTables'),
                      ('libs.parse_fns', 'ParseImports'),
                      ('libs.dashboard', 'DashboardPlots')]
    
    #Create a dict of class objects (not yet instanced)
    class_objs = create_class_objs_dict(mods_cls_names)

    #Set a temp name for each class object and then use it to instance the class
    Files = class_objs['Files']
    files = Files(proj_abbrev='', subdir_home='most_recent', IsTest=False, subdir_tests='')

    ProjectTables = class_objs['ProjectTables']
    tbls = ProjectTables(files, IsParse=True)

    ParseImports = class_objs['ParseImports']
    parse = ParseImports()

    DashboardPlots = class_objs['DashboardPlots']
    dshbrd = DashboardPlots()

    #Custom parsers for ads and sales data
    ParseImports = class_objs['ParseImports']
    parse = ParseImports()

    return files, tbls, parse, dshbrd, parse

def instance_classes_model(pl_abbr, IsTest=False, IsModel=True):
    """
    Instance customized [production-mode] classes for modeling
    JDL 3/31/25
    """
    #Tuples of libs aka *.py filename, module/class name) 
    mods_cls_names = [('libs.projfiles', 'Files'), 
                      ('libs.projtables', 'ProjectTables'),
                      ('libs.model', 'Model')]
    
    #Create a dict of class objects (not yet instanced)
    class_objs = create_class_objs_dict(mods_cls_names)

    #Set a temp name for each class object and then use it to instance the class
    Files = class_objs['Files']
    files = Files(proj_abbrev='', subdir_home='most_recent')

    ProjectTables = class_objs['ProjectTables']
    tbls = ProjectTables(files, IsModel=IsModel)

    Model = class_objs['Model']
    mdl = Model(pl_abbr=pl_abbr, IsPrint=True)
    return files, tbls, mdl

def create_class_objs_dict(mods_cls_names):
    """
    Return a dict of class objects to instance for the project
    JDL 11/19/24; add comments 3/6/25
    """
    # Iteratively import the specified classes (not yet instanced) as dict values
    class_objs = {}
    for mod_name, cls_name in mods_cls_names:
        
        # importlib imports the specified module (and sets var, module, equal to it)
        module = importlib.import_module(mod_name)

        # getattr returns the specified class object from the module
        class_objs[cls_name] = getattr(module, cls_name)
    return class_objs