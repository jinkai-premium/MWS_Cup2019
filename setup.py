from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='mwscup2019_jinkai-premium',
    version="1.0.0",
    author='s.nakano',
    license='MIT',
    packages=find_packages(exclude=()),
    install_requires=[require for require in Path(Path(__file__).parent, 'requirements.txt').read_text().splitlines()],
    entry_points={
        "console_scripts": [
            "mwscup2019_jinkai-premium = src.console_run:main"
        ]
    }
)
