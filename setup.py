import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybireport", # Replace with your own username
    version="0.0.1",
    author="joseaccruz",
    #author_email="author@example.com",
    description="A simple BI report generator.",
    long_description=long_description,
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