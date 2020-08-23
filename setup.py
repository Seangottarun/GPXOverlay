from setuptools import setup, find_packages

def requirements():
    list_requirements = []
    with open('requirements.txt') as f:
        for line in f:
            list_requirements.append(line.rstrip())
    return list_requirements

setup(
    name='GPXOverlay',
    version='0.0.1',
    packages=find_packages(),
    description='overlay GPS data on videos using custom user-defined HTML',
    install_requires=requirements(),
)
