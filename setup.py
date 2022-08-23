import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="discord-webhook",
    version="0.17.0",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="execute discord webhooks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lovvskillz/python-discord-webhook",
    install_requires=[
        "requests>=2.19.1",
    ],
    author="Vadim Zifra",
    author_email="vadim@minehub.de",
    extras_require={
        'async': [
            'httpx>=0.20.0'
        ]
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    entry_points={
        "console_scripts": [
            "discord_webhook=discord_webhook.__main__:main",
        ],
    },
)
