from setuptools import setup, find_packages

setup(
    name = 'epsrc-scraper',
    version = '0.1',
    packages = find_packages(),
    install_requires = [
        'mechanize==0.2.5',
        'pyquery==0.7'
    ],
    entry_points = {
        'console_scripts': [
            'epsrc-scrape = epsrc.command.scrape:main',
        ],
    }
)
