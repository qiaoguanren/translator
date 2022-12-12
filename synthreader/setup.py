import atexit
from setuptools import setup
from setuptools import find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

# Post install hook doesn't work with wheels
# Therefore pip install -e . works, but pip install . doesn't
# Interestingly, pip install . does actually work
# and downloads punkt/averaged_perceptron_tagger if nltk is
# already installed. If nltk is not installed before running
# pip install . the downloads will fail as nltk can't be imported.
# This is included to enable develop install but general install should be:

# pip install .
# python postinstall.py
def _post_install():
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

class PostDevelopCommand(develop):
    def __init__(self, *args, **kwargs):
        super(PostDevelopCommand, self).__init__(*args, **kwargs)
        atexit.register(_post_install)

class PostInstallCommand(install):
    def __init__(self, *args, **kwargs):
        super(PostInstallCommand, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


setup(
    name='synthreader',
    version='0.1.16',
    description='Convert synthetic procedure descriptions to XDL files.',
    author='Matthew Craven',
    author_email='matthew.craven@glasgow.ac.uk',
    packages=find_packages(),
    package_data={'synthreader': ['tagging/reagent_names/probabilities/*.tsv']},
    include_package_data=True,
    install_requires=[
        'nltk>=3',
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
