from setuptools import setup, find_namespace_packages

setup(name='The_soft',
      version='1.0.5',
      description='Sophisticated organizer for thoughtful',
      url='https://github.com/Greezli439/my_little_assistant',
      author='Python Mode',
      license='MIT',
      packages = find_namespace_packages(),
      include_package_data = True,
      entry_points = {'console_scripts': ['the_soft = assistant.Main_menu:main']}
      )
