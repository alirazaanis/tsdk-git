from setuptools import setup

setup(
    name='tsdk-git',
    version='1',
    packages=['tsdk', 'tsdk.test', 'tsdk.common', 'tsdk.logics', 'tsdk.logics.audits',
              'tsdk.logics.audits.nr_basic_audit_v2'],
    url='https://github.com/alirazaanis/tsdk-git',
    license='ATEC',
    author='Ali Raza Anis',
    author_email='alirazaanis@gmail.com',
    description='Telecom System Development Kit',
    install_requires=[
        'pandas',
        'python-dateutil',
        'pyodbc',
        'SQLAlchemy',
        'StrEnum',
        'setuptools',
        'numpy',
        'paramiko',
        'paramiko-expect',
        'APScheduler',
        'openpyxl'
    ],
    include_package_data=True
)
