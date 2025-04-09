# Version 4/3/25
# cd Box\ Sync/Projects/Python_Col_Info/tests
import sys, os
import pandas as pd
import numpy as np
import pytest

# Add libs folder to sys.path and import project-specific modules
libs_path = os.path.join(os.path.dirname(__file__), '..', 'libs')
sys.path.insert(0, os.path.abspath(libs_path))
from col_info import ColumnInfo
from projfiles import Files
from projtables import ProjectTables

# files fixture
@pytest.fixture
def files():
    return Files(IsTest=True, subdir_tests='test_data')

@pytest.fixture
def tbls(files):
    return ProjectTables(files)

# Fixture for ColumnInfo
@pytest.fixture
def col_info():
    return ColumnInfo()
"""
=============================================================================
Class ColumnInfo - DataIngestionProcedure
=============================================================================
"""
def test_DataIngestionProcedure(tbls, col_info):
    """
    Procedure to import Excel data, subset to keep_cols_import and
    replace import names
    JDL 4/3/25
    """
    col_info.DataIngestionProcedure(tbls)

    print('\n\n', tbls.ExampleTbl1.df)
    print('\n', tbls.ExampleTbl2.df, '\n')

def test_ReplaceImportNames1(col_info, tbls):
    """
    Replace import names for ExampleTbl1
    JDL 4/3/25
    """
    # Precursor methods
    tbls.ImportExcelInputs()
    col_info.SetFlagColsBoolean(tbls)
    col_info.SetTblKeepColsFromImport(tbls, 'ExampleTbl1')

    # Call ReplaceImportNames
    col_info.ReplaceImportNames(tbls, 'ExampleTbl1')

    # Check that the column names are correctly replaced
    expected = ['date1', 'col_1a', 'col_1b']
    assert list(tbls.ExampleTbl1.df.columns) == expected

def test_ReplaceImportNames2(col_info, tbls):
    """
    Replace import names for ExampleTbl2
    JDL 4/3/25
    """
    # Precursor methods
    tbls.ImportExcelInputs()
    col_info.SetFlagColsBoolean(tbls)
    col_info.SetTblKeepColsFromImport(tbls, 'ExampleTbl2')

    # Call ReplaceImportNames
    col_info.ReplaceImportNames(tbls, 'ExampleTbl2')

    # Check that the column names are correctly replaced
    expected = ['date2', 'col_2a', 'col_2c']
    assert list(tbls.ExampleTbl2.df.columns) == expected

def test_SetTblKeepColsFromImport(col_info, tbls):
    """
    Subset tbl.df columns based on ColInfo.df
    JDL 4/3/25
    """
    # Precursor methods
    tbls.ImportExcelInputs()
    col_info.SetFlagColsBoolean(tbls)

    # Subset columns for ExampleTbl1 (no deletions)
    col_info.SetTblKeepColsFromImport(tbls, 'ExampleTbl1')
    expected = ['date1_import_name', 'col_1a_import_name', 'col_1b_import_name']
    assert list(tbls.ExampleTbl1.df.columns) == expected

    # Subset columns for ExampleTbl2 (col_dummy gets deleted)
    col_info.SetTblKeepColsFromImport(tbls, 'ExampleTbl2')
    expected = ['date2_import_name', 'col_2a_import_name', 'col_2c_import_name']
    assert list(tbls.ExampleTbl2.df.columns) == expected

def test_tbls_ImportExcelInputs(tbls):
    """
    Import ExampleTbl1 and ExampleTbl2
    JDL 4/3/25
    """
    tbls.ImportExcelInputs()
    assert len(tbls.ExampleTbl1.df) == 3
    assert len(tbls.ExampleTbl2.df) == 6

def test_SetFlagColsBoolean(col_info, tbls):
    """
    Fill False for NaN values in tblCI flag columns 
    (allow True/<blank> entries)
    JDL 4/3/25
    """
    col_info.SetFlagColsBoolean(tbls)

    # Check that IsCalculated and keep_col_import values are correctly processed
    expected = 7 * [False] + [True]
    assert list(tbls.ColInfo.df['IsCalculated']) == expected

    expected = [True, True, True, True, False, True, True, False]
    assert list(tbls.ColInfo.df['keep_col_import']) == expected

def test_tbls_fixture(tbls):
    """
    Test - Check that tbls.ColInfo exists and its path attributes are correct
    JDL 4/3/25
    """
    # Check that ColInfo initialized
    assert hasattr(tbls, 'ColInfo')
    assert tbls.ColInfo.pf.split(os.sep)[-1] == 'col_info.xlsx'

def test_files_fixture(files):
    """
    Test - Check that last two items in files paths are 'libs' and 'col_info.xlsx'
    JDL 4/3/25
    """
    # trailing os.sep creates '' final list item
    lst = files.path_root.split(os.sep)
    assert lst[-1] == ''
    root_folder = lst[-2]

    # Check libs, tests paths relative to root 
    lst = files.path_libs.split(os.sep)
    assert lst[-1] == ''
    assert lst[-2] == 'libs'
    assert lst[-3] == root_folder

    lst = files.path_tests.split(os.sep)
    assert lst[-1] == ''
    assert lst[-2] == 'tests'
    assert lst[-3] == root_folder

    lst = files.pf_col_info.split(os.sep)
    assert lst[-1] == 'col_info.xlsx'
    assert lst[-2] == 'test_data'