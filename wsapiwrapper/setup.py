import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wsapiwrapper",
    version="0.0.5",
    author="Malcolm Mackay",
    author_email="malcolm@plotsensor.com",
    description="A Python interface to wsbackend web APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/websensor/wsbackend",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=['requests']
)
