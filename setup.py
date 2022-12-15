import os
import setuptools


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setuptools.setup(
    author="Zagaran, Inc.",
    author_email="info@zagaran.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Management command to attempt Django migrations and rollback on failure",
    keywords="django migrations",
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="django-migrate-or-rollback",
    packages=setuptools.find_packages(),
    install_requires=["django >= 2.0"],
    python_requires='>=3.6',
    url="https://github.com/zagaran/django-migrate-or-rollback",
    version="0.0.1",
)
