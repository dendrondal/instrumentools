import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="instrumentools", # Replace with your own username
    version="0.0.1",
    author="dendrondal",
    author_email="dendrondal@protonmai.com",
    description="Data analysis tools for chemistry instrumentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="hhttps://github.com/dendrondal/instrumentools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
