# coding:utf8
import sys
import gflags

from stock import flags
from stock.apis.eniu import Eniu

FLAGS = gflags.FLAGS

PY_VERSION = sys.version_info[:2]
if PY_VERSION < (3, 5):
    raise Exception('Python 版本需要 3.5 或以上, 当前版本为 %s.%s 请升级 Python' % PY_VERSION)


def use(source):
    if source in [FLAGS.eniu]:
        return Eniu()
