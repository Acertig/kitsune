from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.1"
DESCRIPTION = "Nhentai.net API wrapper for doujins"
LONG_DESCRIPTION = "Python wrapper around Nhentai.net's RESTful API for doujins"

setup(
    name="kitsune-nh",
    version=VERSION,
    author="acertig (@Acertig)",
    author_email="<acertig04@gmail.com>",
    description=DESCRIPTION, 
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["aiohttp", "Pillow"],
    keywords=["python", "wrapper", "scraper", "nhentai", "anime", "manga"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix", 
        "Operating System :: Microsoft :: Windows"
    ]
)
