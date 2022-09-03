from setuptools import setup, find_packages
from pathlib import Path


VERSION = '0.1.14'
DESCRIPTION = 'Python Script for interacting with Github API'
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="py-github-helper",
    version=VERSION,
    url="https://github.com/org-not-included/payment_parser/",
    author="shivanjaywagh,mtsadler",
    author_email="<michaeltsadler1@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas', 'pendulum'],
    keywords=['python', 'github', 'api', 'comment', 'action', 'Pull Request'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)