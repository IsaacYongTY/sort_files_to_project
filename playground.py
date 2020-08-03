import zhon
from zhon import hanzi
import re

input = "流沙 4KHD.00_22_23_00.Still005.jpg"
result = re.findall('[{}]'.format(zhon.hanzi.characters),input)

str1 = ''
result = str1.join(result)

print(result)