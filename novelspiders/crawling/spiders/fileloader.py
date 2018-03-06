# -*- coding: utf-8 -*-
import os
def loadurls():
    BASE_DIR=os.path.dirname(__file__)
    file_path = BASE_DIR+'/urls.txt'
    # print(file_path)
    with open(file_path,'r') as f:
        return [x.strip() for x in f.readlines()]