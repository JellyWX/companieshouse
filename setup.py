import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

version = None

with open("companieshouse/__init__.py", "r") as f:
    for line in f:
        if line.startswith('__version__'):
            version = ''.join([x for x in line.split(' ')[-1] if x in '0123456789.'])

setuptools.setup(
    name="companieshouse",
    version=version,
    author="JellyWX",
    author_email="judewrs@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jellywx/companieshouse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
