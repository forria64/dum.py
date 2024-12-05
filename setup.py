from setuptools import setup, find_packages

setup(
    name="dumpy",
    version="1.0-beta",
    description="A Python tool for analyzing and summarizing text files in AI workflows.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="forria",
    author_email="forria@forria64.space",
    url="https://github.com/forria64/dum.py",
    packages=find_packages(),
    py_modules=["dumpy"],  # Refers to `dum.py`
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "dum=dum:main",  # Links `dum.py`'s `main()` as a command-line script
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)

