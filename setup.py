#nose bien que hacer,pero me permite hacer que todas las carpetas sean módulos para la importación
from setuptools import setup, find_packages

setup(
    name="data_manager",
    version="0.1",
    packages=find_packages(),
)