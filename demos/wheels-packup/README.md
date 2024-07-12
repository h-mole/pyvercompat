Demo Project to Packup A Wheel
==============================

Run command:

```sh
python -m pyvercompat create-wheel --tag-types 38-39,310+ --wheel-src .\UppaalLTLParser\,.\README.md,.\setup.py --ignored-files .pyc
```

Then just check the generated wheel file in `pyvercompat-dist` directory, you will find the two wheels below:

```shell
pyvercompat-dist
|
|--UppaalLTLParser-0.1.0-py310.py311.py312.py313-none-any.whl
|--UppaalLTLParser-0.1.0-py38.py39-none-any.whl
```
