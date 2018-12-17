import rimuru
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='rimuru',
    version=rimuru.__version__,
    packages=find_packages(),
    url='https://github.com/TNK-Studio/Rimuru',
    license='MIT',
    author='TNK Studio',
    author_email='741424975@qq.com',
    description='📖Use TestCase auto generate API document.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'jinja2',
        'werkzeug'
    ]
)
