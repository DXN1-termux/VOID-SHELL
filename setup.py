from setuptools import setup, find_packages

setup(
    name="void-shell",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich>=12.0.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.20.0",
    ],
    entry_points={
        "console_scripts": [
            "v=void_shell.main:main",
        ],
    },
)
