from setuptools import setup, find_packages
from pathlib import Path


VERSION = '0.1.7'
DESCRIPTION = 'Python Script for Parsing Payments File.'
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="payment_parser",
    version=VERSION,
    url="https://github.com/org-not-included/payment_parser/",
    author=["shivanjaywagh", "mtsadler"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=["T140", "payment", "parser", "fixed", "width", "format"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)