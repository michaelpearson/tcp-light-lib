from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tcp-light-lib',
    version='0.1.0',
    description='Simple library for controling a TCP based smart light',
    long_description='',
    author='Michael Pearson',
    url='https://github.com/michaelpearson/tcp-light-lib',
    license=license,
    packages=find_packages()
)

