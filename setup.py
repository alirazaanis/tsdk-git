from setuptools import setup, find_packages

setup(
    name='tsdk-git',
    version='5.3.3',
    author='Ali Raza Anis',
    author_email='alirazaanis@gmail.com',
    description='Telecom System Development Kit',
    url='https://github.com/alirazaanis/tsdk-git',
    license='ATEC',
    packages=find_packages(include=['tsdk', 'tsdk.*']),
    install_requires=[
        'pandas>=1.5.1',
        'python-dateutil>=2.8.2',
        'pyodbc>=4.0.34',
        'SQLAlchemy>=1.4.42',
        'StrEnum>=0.1.0',
        'numpy>=1.23.4',
        'paramiko>=2.0.2',
        'paramiko-expect>=0.3.4',
        'APScheduler>=3.9.1',
        'openpyxl>=3.0.10',
        'XlsxWriter>=3.0.3'
    ]
)
