from setuptools import find_packages
from setuptools import setup

setup(
    name='amiko-bot',
    description="Simple Offer bot",
    author='owilover',
    url='',
    packages=find_packages('src'),
    package_dir={
        '': 'src'},
    include_package_data=True,
    keywords=[
        'telegram_bot', 'test', 'flask'
    ],
    entry_points={
        'console_scripts': [
            'telegram_bot = app:Amiko']},
)