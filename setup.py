from setuptools import setup, find_packages

setup(
    name="ioa_setup",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        'ioa_setup': [
            'ansible/*.yml',
            'ansible/templates/*.j2',
            'ansible/group_vars/*.yml'
        ],
    },
    install_requires=[
        'boto3==1.38.24',
        'botocore==1.38.24',
        'requests==2.31.0',
        'pyyaml==6.0.1',
        'ansible==8.7.0',
    ],
    entry_points={
        'console_scripts': [
            'ioa-setup=ioa_setup.ioa_setup:main',
        ],
    },
    author="Cosmaya",
    author_email="admin@nanda-registry.com",
    description="SDK for setting up Internet of Agents servers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Cosmaya/internet_of_agents",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
) 