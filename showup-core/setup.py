from setuptools import setup

setup(
    name="showup_core",
    version="0.1.0",
    description="ShowupSquared Core Logic Modules",
    packages=['showup_core'],
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    python_requires=">=3.7",
    author="Your Name",
    author_email="your@email.com",
    url="https://yourprojecturl.example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
