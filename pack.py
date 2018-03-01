# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 19:13:10 2018

@author: jimpri
"""

import os

root_path = r'I:\sd\se\msg\cortex\bolt_trade'
root_dirs = ['prod']
output_path = r"\\w.pdtpartners.com\DFS\Folders\jimpri\Desktop\TG\bolt_trade_dev5"

targets = []#[r'I:\git\di\rtech\wscript']
target_dirs = [os.path.join(root_path, d) for d in root_dirs]

while len(target_dirs) != 0:
    target_dir = target_dirs.pop()
    paths = [os.path.join(target_dir, x) for x in os.listdir(target_dir) if not x.endswith('.pyc')]
    file_paths = [path for path in paths if os.path.isfile(path)]
    dir_paths = [path for path in paths if os.path.isdir(path) if not path.endswith(r'\tests')]
    
    target_dirs = target_dirs + dir_paths
    targets = targets + file_paths

file_sizes = [os.path.getsize(file_path) for file_path in targets]
total_size = sum(file_sizes)
print total_size

def get_file(file_path):
    relative_path = file_path[len(root_path)+1:]
    length = str(os.path.getsize(file_path))
    f = open(file_path, 'r')
    contents = f.read()
    f.close()
    data = relative_path + ' ' + length + ' ' + contents
    
    return data

data_blobs = [get_file(target) for target in targets]
data_out = ''.join(data_blobs)

f = open(output_path, 'w')
f.write(data_out)
f.close()