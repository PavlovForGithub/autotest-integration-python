from setuptools import setup

setup(
    name='testit-pytest',
    version='0.2.3',
    description='Pytest plugin for Test IT',
    long_description=open('README.rst').read(),
    url='https://pypi.org/project/testit-pytest/',
    author='Pavel Butuzov',
    author_email='pavel.butuzov@testit.software',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    py_modules=['testit', 'testit_pytest'],
    packages=['testit_pytest'],
    package_dir={'testit_pytest': 'src'},
    install_requires=['pytest', 'requests'],
    entry_points={'pytest11': ['testit_pytest = testit_pytest.plugin']}
)
