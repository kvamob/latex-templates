import re

s = '\newcommand{\txtDepth}{12.0}  % Глубина скважины'
pattern = re.compile('{(\d*.\d*)}')

if re.findall(r'.*\newcommand{\txtDepth}', s):
    Depth = pattern.findall(s)[0].replace('.', ',')
    print('Depth: {}'.format(Depth))
else:
    print('Не найден')

'''
Clipboard

To use native Python directories, use:

import subprocess

def copy2clip(txt):
   cmd='echo '+txt.strip()+'|clip'
   return subprocess.check_call(cmd, shell=True)
'''