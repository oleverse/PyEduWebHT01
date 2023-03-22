from setuptools import setup, find_namespace_packages

setup(name='My_little_assistant',
      version='1.0.2',
      description='Sophisticated organizer for thoughtful',
      url='https://github.com/Greezli439/my_little_assistant',
      author='Python Mode',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages = find_namespace_packages(),
      include_package_data = True,
      entry_points = {'console_scripts': ['assistant = assistant.Main_menu:main']}
      )