# coding: utf-8

import sys

version = sys.version_info
py3k = version >= (3, 0, 0)
py2k = version >= (2, 0, 0) and version < (3, 0, 0)
py1k = version < (2, 0, 0)

