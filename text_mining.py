# -*- coding: utf-8 -*-

import sys
import os
import warnings
import numpy as np
from sklearn import metrics

warnings.filterwarnings("ignore")

def calculate_accurate(actual,predict):
        m_precision = metrics.accuracy_score(actual,predict)
        print '结果计算:'
        print '精度:{0:.3f}'.format(m_precision)


