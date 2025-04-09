This user guide covers the ProjectTables (projtables.py) utility class. Its attributes are projtables.Table objects whose attributes include the metadata about the table including a .df DataFrame attribute. We hard code initializing a tbls attribute for the major tables in the project

Table Class
Its required and optional arguments with their data types and default values are:
* pf [str] path + filename of a single file to import to populate Table.df
* name [str] name of the table (a good practice is for it to match the Table instance programmatic name set when ProjectTables is instanced e.g. tbls.InputData.name = 'InputData')
* sht='' [str]
* idx_col_name=''
* dImportParams=None
* dParseParams=None
* import_dtype=None

Notes: Move sht to dImportParams; consider modifying to shts to allow for a list of raw import files

Approach based on recent projects:
* Populate tbl.lst_files from function that calls ImportToTblDf
* move Table.sht to be dImportParams['sht'] (used for dImportParams['ftype'] = 'Excel')
* dImportParams['import_path'] = folder to import from
* dImportParams['import_files'] = list of files to import from import_path
* 

Table (ImportProcedure) has:
    dImportParams import_path (can be blank if lst_files items are path+filename)
    dImportParams lst_files (either hard-coded in calling fn or sweep folder approach) has:
        raw file has:           
            dImportParams 'ftype' (either csv, excel or feather)
            dImportParams fvalidations: file_exists, sht_exists etc.

        <import to .df_raw using tbl.dParseParams for:
            skip_rows, is_unstructured, sht

        raw file has
            data_validations (list of tuples?) has
                val_type
                optional params like idx_row, idx_col, val_expected
            parse_type
                none
                rowmajor
                interleaved_col_blocks
        
        <parse to .df>
    
    To instance a table, need to specify its name attribute; dImportParams, dParseParams can be hard-coded when table instanced or specified after instancing tbls (by calling funciton/ipynb) before calling tbl.ImportAndParse

    dImportParams
        import_path (can be blank if lst_files items are path+filename)
        lst_files (either hard-coded in calling fn or sweep folder approach) has
        ftype (either csv, excel or feather)
        file_validations: file_exists, sht_exists etc.

    dParseParams (parse_type-specific instructions) has
        sht [optional --n/a for csv; sheet 0 Excel default]
        ftype = csv or excel:
            n_skiprows [optional; default 0]
            is_unstructured [optional; default False] -openpyxl load_workbook if True
        parse_type = none --> signifies no parsing .df = .df_raw
        parse_type = rowmajor
            flag_start_bound
            icol_start_bound
            flag_end_bound
            icol_end_bound
            idata_rowoffset_from_flag
            iheader_rowoffset_from_flag
            block_id_vars
            is_stack_parsed_cols
        parse_type = interleaved_col_blocks
            idx_start
            n_cols_metadata
            n_cols_block

