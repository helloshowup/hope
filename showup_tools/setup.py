from setuptools import setup, find_packages

setup(
    name="showup_tools",
    version="0.1.0",
    description="Auxiliary ShowupSquared tools",
    packages=find_packages(where="."),  # automatically finds all valid packages
    package_dir={"": "."},
    python_requires=">=3.7",
)
