from setuptools import setup, find_namespace_packages

setup(name='the_soft',
      version='1.1.0',
      description='Sophisticated organizer for thoughtful',
      url='https://github.com/oleverse/PyEduWebHT01',
      author='Python Mode',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      entry_points={'console_scripts': ['the_soft = the_soft.main_menu:main']}
      )
