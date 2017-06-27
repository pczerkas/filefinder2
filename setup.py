#!/usr/bin/env python
import subprocess
import sys
import setuptools
import runpy

# Ref : https://packaging.python.org/single_source_version/#single-sourcing-the-version
# runpy is safer and a better habit than exec
version = runpy.run_path('filefinder2/_version.py')
__version__ = version.get('__version__')


# Best Flow :
# Clean previous build & dist
# $ gitchangelog >CHANGELOG.rst
# change version in code and changelog
# $ python setup.py prepare_release
# WAIT FOR TRAVIS CHECKS
# $ python setup.py publish
# => TODO : try to do a simpler "release" command


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PrepareReleaseCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "prepare a release of filefinder2"
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""

        # TODO :
        # $ gitchangelog >CHANGELOG.rst
        # change version in code and changelog
        subprocess.check_call(
            "git commit CHANGELOG.rst filefinder2/_version.py -m 'v{0}'".format(__version__), shell=True)
        subprocess.check_call("git push", shell=True)

        print("You should verify travis checks, and you can publish this release with :")
        print("  python setup.py publish")
        sys.exit()

# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PublishCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "releases filefinder2 to Pypi"
    user_options = []

    def initialize_options(self):
        """init options"""
        # TODO : register option
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        # TODO : clean build/ and dist/ before building...
        subprocess.check_call("python setup.py sdist", shell=True)
        subprocess.check_call("python setup.py bdist_wheel", shell=True)
        # OLD way:
        # os.system("python setup.py sdist bdist_wheel upload")
        # NEW way:
        # Ref: https://packaging.python.org/distributing/
        subprocess.check_call("twine upload dist/*", shell=True)

        subprocess.check_call("git tag -a {0} -m 'version {0}'".format(__version__), shell=True)
        subprocess.check_call("git push --tags", shell=True)
        sys.exit()


setuptools.setup(name='filefinder2',
    version=__version__,
    description='PEP420 - implicit namespace packages for python 2.7',
    url='http://github.com/asmodehn/filefinder2',
    author='AlexV',
    author_email='asmodehn@gmail.com',
    license='MIT',
    packages=[
        'filefinder2',
        'filefinder2.tests', 'filefinder2.tests.nspkg', 'filefinder2.tests.nspkg.subpkg',
    ],
    # this is better than using package data ( since behavior is a bit different from distutils... )
    include_package_data=True,  # use MANIFEST.in during install.
    # Reference for optional dependencies : http://stackoverflow.com/questions/4796936/does-pip-handle-extras-requires-from-setuptools-distribute-based-sources
    install_requires=[
        # this is needed as install dependency since we embed tests in the package.
        'pytest>=2.8.0',  # as per hypothesis requirement (careful with 2.5.1 on trusty)
        'pytest-xdist',  # for --boxed (careful with the version it will be moved out of xdist)
    ],
    cmdclass={
        'prepare_release': PrepareReleaseCommand,
        'publish': PublishCommand,
    },
    zip_safe=False,  # TODO testing...
)
