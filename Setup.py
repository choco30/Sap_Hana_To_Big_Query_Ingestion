import setuptools

REQUIRED_PACKAGES = ['pandas','fsspec','hdbcli','gcsfs','google-cloud-bigquery','google-cloud-storage']
PACKAGE_NAME = 'my_package'
PACKAGE_VERSION = '0.0.1'
setuptools.setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description='Example project',
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
)
