import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quota-tracker",
    version="0.0.1",
    author="Thi Dang",
    author_email="dkthi2901@gmail.com",
    description="A quota tracker package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thidang2901/quota-tracker",
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
)