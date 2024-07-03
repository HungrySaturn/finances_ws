from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="finaces_ws",  # Název vašeho balíčku
    version="0.0.1",  # Počáteční verze
    author="Wala, Novotný",
    author_email="vase.email@example.com",
    description="ws finances",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HungrySaturn/finances_ws",
    packages=find_packages(include=['app', 'app.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.12',
    install_requires=[
        # Zde uveďte požadavky z requirements-dev.txt, např.
        'selenium',
        'bs4',
        'requests'
    ],
)