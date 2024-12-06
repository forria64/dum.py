from setuptools import setup, find_packages

setup(
    name="dumpy",  # Package name
    version="1.1-beta",  # Version
    description="A Python tool for summarizing code files.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="forria",
    author_email="forria@forria64.space",
    url="https://github.com/forria64/dum.py",
    packages=find_packages(),  # Automatically find all packages
    py_modules=["dumpy"],  # The module that will be used for the entry point
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "dumpy=dumpy.dum:main",  # This tells Python to use the main function in dum.py
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
)

