import setuptools

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setuptools.setup(
    name="pyvercompat",
    version="0.1.0",
    description="A pure-python (Python>=3.10) code conversion tool to convert code file or wheel package to lower versions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hzyrc6011/pyvercompat",
    author="hzyrc6011",
    author_email="1295752786@qq.com",
    license="MIT",
    # For classifiers, refer to:
    # https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Documentation": "https://hzyrc6011.github.io/pyvercompat/",
    },
    packages=setuptools.find_namespace_packages(
        include=["pyvercompat", "pyvercompat.*"]
    ),
    install_requires=[
    ],
    python_requires=">=3.10",
    include_package_data=True,
)
