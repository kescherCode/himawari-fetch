from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="himawari_fetch",
    version="1.0.0",
    url="https://github.com/kescherCode/himawari_fetch",
    author="Jeremy Kescher",
    author_email="jeremy@kescher.at",
    license="MIT",
    description="himawari_fetch is a Python 3 script based on himawaripy that fetches near-realtime (10 minutes "
                "delayed) picture of Earth as its taken by Himawari 8 (ひまわり8号) and saves them to a prespecified "
                "directory. It also cleans up images older than a day.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["requests", "pillow"],
    packages=find_packages(),
    entry_points={"console_scripts": ["himawari_fetch=himawari_fetch.__main__:main"]},
)
