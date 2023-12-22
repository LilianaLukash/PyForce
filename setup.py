from setuptools import setup, find_packages

setup(
    name='PyForce',
    version='1',
    description='Personal assistant for reminding about contacts\' birthdays',
    url='https://github.com/LilianaLukash/PyForce',
    author='PyForce',
    author_email=['lukashliliana@gmail.com', 'artur.myhajlyuk@gmail.com', 'bogdan.pavlyk7@gmail.com', 'kucherkovpromotion@gmail.com'],
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyforce = pyforce.main:main_function',
            'pyforce-models = pyforce.models:function_in_models',
            'pyforce-notes = pyforce.modelsfornotes:function_in_modelsfornotes'
        ]
    }
)
