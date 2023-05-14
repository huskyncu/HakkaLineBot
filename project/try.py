from openfile import pickup2
from identify import identify
ans_text = identify("454587147460461819")
print(ans_text)
list1 = pickup2()
if ans_text in list1:
    print('1')