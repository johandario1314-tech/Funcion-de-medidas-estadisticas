from setuptools import setup, find_packages

setup(
    name="mi_funcion",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas"
    ],
    author="Johan",
    description="Paquete para análisis descriptivo de dataframes"
)