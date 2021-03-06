from setuptools import setup

setup(name='colored_logger',
      version='1.0.8',
      description='Colored Logger for terminal',
      url='https://github.com/eskemojoe007/colored_logger',
      author='David Folkner',
      author_email='David.Folkner@gmail.com',
      license='MIT',
      packages=['colored_logger'],
      install_requires=[
        'six',
        'colorama',
        'crayons'
        ],
      zip_safe=False)
