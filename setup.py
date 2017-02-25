from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='oops-parser',
    version=version,
    keywords=('parser',),
    description='Oops parser',
    url='https://github.com/GNaive/oops-parser',
    license='MIT License',
    author='yetone',
    author_email='yetoneful@gmail.com',
    packages=find_packages(),
    platforms='any',
    tests_require=(
        'pytest',
    )
)
