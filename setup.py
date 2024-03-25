from setuptools import setup, find_packages

setup(
    name="spectralib",
    version="0.0.22",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 1 - Planning",
    ],
    author="Jack White",
    author_email="jack.white@eng.ox.ac.uk",
    description="Synthetic Pulsar Emission, Contamination and Transients Radio Astronomy Library (SPECTRALib)",
    long_description="A python library for creating synthetic filterbank files (pulsars, FRBs, RFI) for radio astronomy. Integrate functions in your code or use standalone to generate custom datasets.",
    long_description_content_type="text/markdown",
    url="https://github.com/jack-white1/spectralib",
)
