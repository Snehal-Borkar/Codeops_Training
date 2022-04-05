# 2nd Week Task

## 1. Write Functional Programming for 1st week task and Modularize it.
## Quick start
- #### Api call
```python
import api_response
response = api_response.api_call(url)
```
- #### Flat json data
```python
flat_df = api_response.flatten_json(data)
```
- #### Dataframe to file generation
```python
import json_X_converter

json_X_converter.df_csv(flat_dfs, filename)

json_X_converter.df_html(flat_dfs, filename)

json_X_converter.df_xml(flat_dfs, filename)
```
## 2.Write Class based programming and Modularize it.

## 3.Publish package to PyPI (Python Package Index)