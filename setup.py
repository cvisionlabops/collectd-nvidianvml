from setuptools import setup
import os,sys

# Following Lapin example
# https://bitbucket.org/CVisionLab/cvl-python/src/51308c1155a6242fbb914870732187adfc8881f0/setup.py?at=default&fileviewer=file-view-default

root_pkg = 'collectd-nvidianvml'

# find all subpackages
root = os.path.join(os.path.dirname(__file__), root_pkg)

packages = []
for subdir, _, _ in os.walk(root):
        subpath = subdir[len(root):].replace(os.path.sep, '.')
        packages.append(root_pkg + subpath)

setup(
    name=root_pkg,
    description='CVISIONLAB OPS Collectd Python Plugin for NVIDIA GPU using nvml',
    long_description=open('README.txt').read(),
    version='0.1.1',
    author='Skubriev Vladimir',
    author_email='skubriev@cvisionlab.com',
    license='GPL',
    url='https://github.com/cvisionlabops/collectd-nvidianvml',
    install_requires=[
                  'nvidia-ml-py'
    ],
    packages=packages,
    package_data={'collectd-nvidianvml': ['nvidia-ml-py']},
)
