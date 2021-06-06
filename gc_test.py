#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import gc

a = [1]
b = [2]
a.append(b)
b.append(a)
print(a)
print(b)
