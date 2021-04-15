from setuptools import setup

setup(
    name='client',
    version='1.0',
    license='GPLv3',
    description='client arduino PUF',
    author='Corey Cline',
    packages='client',
    install_requires=['pyserial']
)