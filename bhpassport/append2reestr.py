import re

s = '\newcommand{\txtDepth}{12.0}  % Глубина скважины'
pattern = re.compile('{(\d*.\d*)}')

if re.findall(r'.*\newcommand{\txtDepth}', s):
    Depth = pattern.findall(s)[0].replace('.', ',')
    print('Depth: {}'.format(Depth))
else:
    print('Не найден')

