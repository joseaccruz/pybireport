import os
import setuptools


local_path = os.path.abspath(os.path.dirname(__file__))


def read_reqs(fname):
    req_file = os.path.join(os.path.abspath(local_path), fname)

    with open(req_file) as f:
        reqs = [req.strip() for req in f.read().strip().splitlines()]

    return reqs


def read_description(fname):
    desc_file = os.path.join(os.path.abspath(local_path), fname)

    with open(desc_file, "r") as f:
        desc = f.read()


setuptools.setup(
    name="pybireport", # Replace with your own username
    version="0.0.1",
    author="joseaccruz",
    #author_email="author@example.com",
    description="A simple BI report generator.",
    long_description=read_description("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/joseaccruz/pybireport",
    license='MIT',
    keywords='BI data reports pandas',

    packages=setuptools.find_packages(),
    install_requires=read_reqs('requirements.txt'),

    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Data Scientists/Analysts",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.7',
)