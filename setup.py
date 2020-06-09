from distutils.core import setup

setup(
    name='Routine Convert',
    version='0.1DEV',
    author='Ryan Metcalf',
    author_email='ryanitto@gmail.com',
    packages=['routine_convert'],
    scripts=[''],
    license='LICENSE.txt',
    description='A routine conversion script, using Handbrake, that collects media files in a directory structure'
                'and converts them!',
    long_description=open('README.txt').read(),
    install_requires=[
        "IMDbPY >= 6.8",
        "SQLAlchemy >= 1.3.17",
        "lxml >= 4.5.1",
    ],
)