## User Guide for `ImportToTblDf` Method

---

### Overview
The `ImportToTblDf` method is used to import data from various file types (e.g., Excel, CSV, Feather) into a `Table` instance. It supports structured and unstructured data imports, with options to customize the behavior using parameters in `dImportParams` and `dParseParams`.

The code is within projtables.py that contains two foundational classes that are part of a modeling toolbox:
* `ProjectTables` (typically instanced as `tbls`) is a collection of all data tables and their metadata associated with a project. Its attributes are `Table` objects typically instanced in `ProjectTables.InstanceTblObjs` as in this example for a hypothetical table to be imported from the sheet, `data` in a hypothetical Excel file, `Example1.xlsx`.  The `lst_files` dict item can be an individual filename or a list of files, and it can be set more dynamically as needed such as the situation where the files to be imported from a sweep folder.
```
        dImportParams = {'import_path':self.files.path_data,
                        'ftype':'excel',
                        'sht':'data'}
        dImportParams['lst_files'] = 'Example1.xlsx'
        self.ExampleTbl1 = Table('ExampleTbl1', dImportParams=dImportParams,
                                                dParseParams=None)
```
* The `Table` class objects that are `tbls` attributes contain all metadata for a project table including its `.df` data and its `.name`. The latter is input as an argument in the example above, and a best practice is to name the table the same as its programmatic instance. Other attributes are `.dImportParams` and `.dParseParams` that describe how to import and parse data into `.df` for use in modeling and analysis. Data ingestion directly imports to `.df` for "structured" rows/columns raw data. If the data are unstructured but in a repeatable format, `ImportToTblDf` populates `Table.lst_dfs` with individual raw (unparsed) imported df's --enabling subesquent parsing and concatenation into `Table.df`.

---
The following sections describe use of `Table.ImportToTblDf` options for ingesting and parsing data

### 1. `dImportParams`
This dictionary specifies import-related parameters.

| **Key**          | **Description**                                                                 | **Required/Optional** | **Default Value** |
|-------------------|---------------------------------------------------------------------------------|------------------------|-------------------|
| `ftype`           | File type to import. Supported values: `'excel'`, `'csv'`, `'feather'`.         | Required               | None              |
| `lst_files`       | List of file paths or a single file path to import.                             | Required               | None              |
| `import_path`     | Path to prepend to file names in `lst_files`.                                   | Optional               | None              |
| `sht`             | Sheet name or index for Excel files.                                           | Optional               | `0` (first sheet) |
| `sht_type`        | Specifies how to handle sheets in Excel files. Supported values: `'single'`, `'all'`, `'list'`, `'regex'`, `'startswith'`, `'endswith'`, `'contains'` (only `single` and `all` enabled as of 4/14/25). | Optional | `'single'`  |

---

### 2. `dParseParams`
This dictionary specifies parsing-related parameters.

| **Key**           | **Description**                                                                 | **Required/Optional** | **Default Value** |
|-------------------|---------------------------------------------------------------------------------|------------------------|-------------------|
| `is_unstructured` | Indicates whether the data is unstructured.                                     | Optional               | `False`           |
| `n_skip_rows`     | Number of rows to skip at the top of the file (for structured data).             | Optional               | `0`               |
| `parse_type`      | Parsing type for unstructured data. Supported values: `'none'`, `'row_major'`, `'col_major'`. | Optional | `'none'` |

---

### 3. Behavior Based on `ftype`

#### 3.1 `ftype = 'excel'`
- **Description**: Imports data from Excel files.
- **Additional Parameters**:
  - `sht`: Specifies the sheet to import. Can be a name or index.
  - `sht_type`: Determines how sheets are handled:
    - `'single'`: Imports a single sheet specified by `sht`.
    - `'all'`: Imports all sheets in the workbook.
    - `'list'`: Imports sheets specified in a list.
    - `'regex'`: Imports sheets matching a regular expression.
    - `'startswith'`: Imports sheets whose names start with a specific string.
    - `'endswith'`: Imports sheets whose names end with a specific string.
    - `'contains'`: Imports sheets whose names contain a specific substring.

#### 3.2 `ftype = 'csv'`
- **Description**: Imports data from CSV files.
- **Additional Parameters**:
  - `is_unstructured`: If `True`, the first row is not treated as headers (`header=None`).
  - `n_skip_rows`: Number of rows to skip at the top of the file.

#### 3.3 `ftype = 'feather'` (not implemented as of 4/13/25)
- **Description**: Imports data from Feather files.
- **Additional Parameters**:
  - None (Feather files are always structured).

---

### 4. Examples

#### 4.1 Importing a Single Excel Sheet
```python
dImportParams = {
    'ftype': 'excel',
    'lst_files': 'Example1.xlsx',
    'sht': 'data',
    'sht_type': 'single'}
tbl = Table('ExampleTable', dImportParams)
tbl.ImportToTblDf()
```

#### 4.2 Importing All Sheets from an Excel File
```python
dImportParams = {
    'ftype': 'excel',
    'lst_files': 'Example2.xlsx',
    'sht_type': 'all'}
tbl = Table('ExampleTable', dImportParams)
tbl.ImportToTblDf()
```

#### 4.3 Importing a CSV File with Skipped Rows
```python
dImportParams = {
    'ftype': 'csv',
    'lst_files': 'Example3.csv'
}
dParseParams = {
    'n_skip_rows': 2
}
tbl = Table('ExampleTable', dImportParams, dParseParams)
tbl.ImportToTblDf()
```

#### 4.4 Importing Unstructured CSV Data
```python
dImportParams = {
    'ftype': 'csv',
    'lst_files': 'Example4.csv'}
dParseParams = {
    'is_unstructured': True}
tbl = Table('ExampleTable', dImportParams, dParseParams)
tbl.ImportToTblDf()
```

---

#### 5. Default Behavior
- If `lst_files` is not specified, the method uses `dImportParams['lst_files']`.
- If `sht` is not specified for Excel files, the first sheet (`0`) is used.
- If `is_unstructured` is not specified, the data is treated as structured.

---

#### 6. Error Handling
To be implemented as of 4/13/25
- **Missing `ftype`**: Raises an error if `ftype` is not provided in `dImportParams`.
- **Invalid `ftype`**: Raises an error if `ftype` is not one of the supported values (`'excel'`, `'csv'`, `'feather'`).
- **File Not Found**: Raises an error if a file in `lst_files` does not exist.
- **Invalid Sheet Name**: Raises an error if the specified sheet does not exist in the Excel file.

---

This guide provides a comprehensive overview of the `ImportToTblDf` method, its parameters, and its behavior for different file types.

J.D. Landgrebe, Data Delve LLC
April 12, 2025