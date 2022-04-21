"""
Amitoz AZAD 2022-04-18 10:14
"""

from setuptools import setup, find_packages

install_requires = [
    'numpy',
    'tqdm',
    'scipy',
    'scikit-image',
    'matplotlib',
]

setup(
    name="pyinpaint",
    version="1.0.0",
    description="A lightweight image inpainting tool",
    url="https://github.com/aGIToz/PyInpaint",
    python_requires='>=3.6',
    install_requires=install_requires,
    packages=find_packages(),
    author="Amitoz AZAD",
    license="MIT",
    include_package_data=True,
    entry_points={
        "console_scripts": [
        "pyinpaint=pyinpaint.__main__:main",
        ]
        },
    )
