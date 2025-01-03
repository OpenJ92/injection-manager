from setuptools import setup, find_packages

setup(
    name="injection-manager",
    version="0.1.0",  # Update version if necessary
    description="An async-enabled injection framework for StarCraft data.",
    author="Jacob Vartuli-Schonberg",
    author_email="jacob.vartuli.schonberg@gmail.com",
    url="https://github.com/OpenJ92/injection-manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

