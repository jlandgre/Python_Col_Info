# Version 4/3/25
import pandas as pd
import numpy as np
"""
=============================================================================
Class ColumnInfo
=============================================================================
"""
class ColumnInfo:
    def __init__(self, IsPrint=True):
        """
        JDL 4/3/25
        """
        self.IsPrint = IsPrint
    """
    =========================================================================
    DataIngestionProcedure
    =========================================================================
    """
    def DataIngestionProcedure(self, tbls):
        """
        Procedure to import Excel data, subset to keep_cols_import and
        replace import names. 
        * tbls.__init__ imports tbls.ColInfo.df
        * refactor to use tbl.dImportParams to decide call Excel, CSV etc.

        JDL 4/3/25
        """
        tbls.ImportExcelInputs()
        self.SetFlagColsBoolean(tbls)
        for tbl in tbls.lstExcelImports:
            self.SetTblKeepColsFromImport(tbls, tbl.name)
            self.ReplaceImportNames(tbls, tbl.name)

    def ReplaceImportNames(self, tbls, tbl_name):
        """
        Replace import names in tbl.df columns with project variable names
        JDL 4/3/25
        """
        # Get Table object from its name
        tbl = getattr(tbls, tbl_name)

        # Create table-specific, keep_col_import filter
        fil = self.fil_keep_vars(tbls, tbl_name)

        # Create dict mapping name_import to name; rename columns
        df_fil = tbls.ColInfo.df.loc[fil, ['name_import', 'name']]
        rename_dict = df_fil.set_index('name_import')['name'].to_dict()
        tbl.df.rename(columns=rename_dict, inplace=True)

    def SetTblKeepColsFromImport(self, tbls, tbl_name, IsImportNames=True):
        """
        Subset tbl.df columns based on ColInfo.df
        JDL 4/3/25
        """
        # Get Table object from its name
        tbl = getattr(tbls, tbl_name)

        # Base filtering either on 'name' or 'import_name' col_info column
        var_name_col = 'name'
        if IsImportNames: var_name_col = 'name_import'

        # Filter to tbl's rows where col_info keep_col_import is True
        fil = self.fil_keep_vars(tbls, tbl_name)
        keep_vars = list(tbls.ColInfo.df.loc[fil, var_name_col])
        tbl.df = tbl.df[keep_vars]

    def fil_keep_vars(self, tbls, tbl_name):
        """
        Helper function to filter .ColInfo.df for tbl and keep_col_import
        JDL 4/3/25
        """
        fil = tbls.ColInfo.df[tbl_name].notnull()
        fil = fil & (tbls.ColInfo.df['keep_col_import'])
        return fil

    def SetFlagColsBoolean(self, tbls):
        """
        Fill False for NaN's in .ColInfo flag columns  (allow True/<blank> original)
        JDL 4/3/25
        """        
        lst_flag_cols = ['keep_col_import', 'IsCalculated']
        for col in lst_flag_cols:
            tbls.ColInfo.df[col] = tbls.ColInfo.df[col].fillna(False)
            tbls.ColInfo.df[col] = tbls.ColInfo.df[col].astype(bool)
