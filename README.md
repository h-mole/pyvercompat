PyVerCompat: Semantic Features Conversion Tool for Pure-Python Code or Projects
===============================================================================

PyVerCompat is a tool to convert (mainly downgrade) Python `3.10+` codes' semantic features to Python `<=3.9` code.

> Note that this tool must be run on `Python>=3.10` to parse `match...case...` semantics

Now The **Supported Semantic Features**:

- Pattern-Matching (`match...case...`): Supported now
- Walrus Operator: Developing...

## Convert Single File

Go to the path `demos/wheels-packup`, the file `match_case_demo.py` features `match-case` semantic:

```python
# match_case_demo.py
def f(a):
    match a:
        case 1:
            return
        case [1, x]:
            return x
        case {"a": 1}:
            return a
        case _:
            pass
```

Then run:

```sh
python -m pyvercompat convert-file -i match_case_demo.py -o converted_to_if_else.py --encoding utf8 
```

File `converted_to_if_else.py` will be generated, and its content is shown in the code block below ↓. The original match...case... semantics was converted automatically to a series of `if...elif...else` statements.

```python
# converted_to_if_else.py
def f(a):
    if a == 1:
        return
    elif len(a) == 2 and a[0] == 1 and True:
        x = a[1]
        return x
    elif 'a' in a and a['a'] == 1:
        return a
    else:
        pass
```

## Build wheels for Lower Python versions

PyVerCompat can build wheels for lower Python versions on Python>=3.10.
Currently 3.8 and 3.9 are supported.

For example, go to the path `demos/wheels-packup`, there is a small python project with
heavy usage on match-case semantics, especially in `UppaalLTLParser/ltl.py`

Run the command below to packup the project:

> **NOTICE**: `pyvercompat create-wheel` command must be launched under the project root that have a `setup.py` or `pyproject.toml`.

```sh
python -m pyvercompat create-wheel --tag-types 38-39,310+ --wheel-src .\UppaalLTLParser\,.\README.md,.\setup.py --ignored-files .pyc
```

- **--tag-types**: The types of python version tag on the wheel's filename to be generated. Currently supporting:
  - `38-39` : Python 3.8 and 3.9, indicating python version tag `py38.py39`
  - `310+`  :Python >=3.10, indicating python version tag `py310.py311.py312.py313`(Will be changed if a newer version of python is released)
- **--wheel-src**: The source files or directories to be packed up.
- **--ignored-files**: The files to be ignored when packing up.


Then just check the generated wheel file in `pyvercompat-dist` directory, you will find the two wheels below:

```shell
pyvercompat-dist
|
|--UppaalLTLParser-0.1.0-py310.py311.py312.py313-none-any.whl
|--UppaalLTLParser-0.1.0-py38.py39-none-any.whl
```
