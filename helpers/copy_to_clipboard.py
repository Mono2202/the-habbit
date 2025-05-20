import os
import pyperclip

x = os.listdir("./public/assets/indexed-sprites")
x = sorted(x)
y = ""
for i in x:
    y += f'\"/assets/indexed-sprites/{i}\",\n'

pyperclip.copy(y)
