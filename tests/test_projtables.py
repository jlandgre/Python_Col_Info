# Version 4/3/25
# cd Box\ Sync/Projects/Python_Col_Info/tests
import sys, os
import pandas as pd
import numpy as np
import pytest

# Add libs folder to sys.path and import project-specific modules
libs_path = os.path.join(os.path.dirname(__file__), '..', 'libs')
sys.path.insert(0, os.path.abspath(libs_path))
from projfiles import Files
from projtables import ProjectTables
from projtables import Table

#Stop 4/8/25 18:22
#Set up test of unstructured Excel import
#Set .df instead of .df_raw if .dParseParams['parse_type'] == 'none'
#Set tbl.col_info based on subsetting tbls.ColInfo.df by tbl.name

@pytest.fixture
def files():
    return Files(IsTest=True, subdir_tests='test_data')

@pytest.fixture
def tbls(files):
    return ProjectTables(files)

@pytest.fixture
def tbls_ExcelFile(files):
    tbls_ExcelFile = Table('ExcelFile')
    tbls_ExcelFile.dImportParams = {'import_path':files.path_data, 
        'lst_files':'', 'ftype': 'excel'}
    return tbls_ExcelFile

def test_ImportToTblDf1(tbls_ExcelFile):
    """
    Import Excel rows/cols table to tbls.ExcelFile.df_raw
    4/8/25
    """
    tbls_ExcelFile.dImportParams['lst_files'] = 'Example2.xlsx'

    # ImportToTblDf and check .df_raw
    tbls_ExcelFile.ImportToTblDf()
    check_ExcelFile(tbls_ExcelFile)

def test_ImportToTblDf2(tbls_ExcelFile):
    """
    Import Excel structured table with skip_rows
    4/8/25
    """
    tbls_ExcelFile.dImportParams['lst_files'] = 'Example2_skiprows.xlsx'
    tbls_ExcelFile.dParseParams['n_skiprows'] = 2

    # ImportToTblDf and check .df_raw
    tbls_ExcelFile.ImportToTblDf()
    check_ExcelFile(tbls_ExcelFile)

def test_ImportToTblDf3(tbls_ExcelFile):
    """
    Import Excel structured table from multiple raw files
    4/8/25
    """
    tbls_ExcelFile.dImportParams['lst_files'] = ['Example2a.xlsx', 'Example2b.xlsx']

    # ImportToTblDf and check .df_raw
    tbls_ExcelFile.ImportToTblDf()
    check_ExcelFile(tbls_ExcelFile)

def check_ExcelFile(tbls_ExcelFile):
    """
    Helper function to check ExcelFile import
    4/8/25
    """
    assert isinstance(tbls_ExcelFile.df_raw, pd.DataFrame)
    assert len(tbls_ExcelFile.df_raw) == 6

def test_Instance_ExcelFile_Table(tbls):
    """
    Test - Initialize tbls.ExcelFile as an instance of Table
    4/8/25
    """
    # Initialize tbls.ExcelFile as an instance of Table
    tbls.ExcelFile = Table('ExcelFile')

    # Assert that tbls.ExcelFile is correctly initialized
    assert isinstance(tbls.ExcelFile, Table)
    assert tbls.ExcelFile.name == 'ExcelFile'

def test_tbls_fixture(files, tbls):
    """
    Test - tbls fixture
    4/8/25
    """
    # Check that tbls is an instance of ProjectTables
    assert isinstance(files, Files)
    assert isinstance(tbls, ProjectTables)
    assert isinstance(tbls.ColInfo, Table)

