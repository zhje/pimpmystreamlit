# PimpMyStreamlit

 The same Streamlit elements you know and love, supercharged.

 ## About

PimpMyStreamlit extends existing Streamlit elements with more advanced functionality. This is accomplished through additional function parameters and arguments.

For example, `pimpst.data_editor` extends `st.data_editor` to include optional database interfacing, etc.

PimpMyStreamlit currently has ensured compatibility with Streamlit v1.40.0.

## Usage

Import Streamlit and PimpMyStreamlit modules.

```
import streamlit as st
import pimpmystreamlit as pimpst
```

When calling a Streamlit element, simply replace the module alias `st` with `pimpst` to access the additional functionality.

Example:

```
pimpst.data_editor()
```

### Usage Notes

- Although only a few elements are currently "pimpable", `pimpmystreamlit` can still replace any instance of a `streamlit` element. If the element called is not yet included here, the classic Streamlit element will be used. No worries 🤙
- PimpMyStreamlit attempts to enhance aspects of and not replace classic Streamlit. Therefore, instead of forking Streamlit, PimpMyStreamlit works alongside it. This means you can immediately use it with each new Streamlit release, with the caveat that compatibility is not ensured until a subsequent PimpMyStreamlit update. For the latest ensured compatible Streamlit version, see the [About](#About) section.

### Pimpable elements

The following elements are currently supported.

#### <span style="color: #FF0099;">pimpst.data_editor</span>

Display a data editor widget.

The data editor widget allows you to edit dataframes and many other data structures in a table-like UI. **Pimp it out by displaying a database table and allowing direct edits to the database.**

| Function signature |
|-|
|  st.data_editor(data, *, width=None, height=None, use_container_width=False, hide_index=None, column_order=None, column_config=None, num_rows="fixed", disabled=False, key=None, on_change=None, args=None, kwargs=None) |

| Parameters | |
|-|-|
| **data** *(Anything supported by st.dataframe)* | The data to edit in the data editor. To display an editable database table, must be a dict containing key/value pair `"type": "db_table"` |
| ... | All other parameters are identical to those of [st.data_editor](https://docs.streamlit.io/develop/api-reference/data/st.data_editor) |

```
data = {
    "type": "db_table", # Indicates this is a database table
    "db_name": "my_database",
    "db_type": "postgresql",
    "db_config": {
        "host": "localhost",
        "port": 5432,
        "user": "my_user",
        "password": "my_password"
    },
    "table_name": "my_table",
    "schema_name": "public",
}
```

| Returns | |
|-|-|
| *(pandas.DataFrame, pandas.Series, pyarrow.Table, numpy.ndarray, list, set, tuple, or dict.)* | The edited data. The edited data is returned in its original data type if it corresponds to any of the supported return types. All other data types are returned as a pandas.DataFrame. |