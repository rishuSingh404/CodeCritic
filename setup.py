from setuptools import setup, find_packages

# We use pyproject.toml for configuration
# This file is here for compatibility with older tools
setup(
    name="codecritic",
    packages=find_packages(),
    include_package_data=True,
)
