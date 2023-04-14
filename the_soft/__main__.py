from os.path import dirname, abspath, join
import sys

# add parent directory to sys.path
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..'))
sys.path.append(CODE_DIR)

from the_soft import main

if __name__ == '__main__':
    sys.exit(main())
