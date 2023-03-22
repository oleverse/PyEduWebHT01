from setuptools import setup, find_namespace_packages

setup(name='My_little_assistant',
      version='1.0.0',
      description='Very useful code',
      url='https://github.com/Greezli439/my_little_assistant',
      author='Command_name',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages = find_namespace_packages(),
      include_package_data = True,
      entry_points = {'console_scripts': ['assistant = my_little_assistant:Main_menu']}
      )