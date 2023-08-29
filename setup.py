from setuptools import setup

setup(
    name='elbackup',
    version='2.0.0',
    author='Vyacheslav Anzhiganov',
    author_email='vanzhiganov@ya.ru',
    package_data={},
    scripts=[
        'elbackup.py',
    ],
    packages=[
        "elbackup"
    ],
    install_requires=[
        "python-gnupg",
        "easywebdav2"
    ]
)
