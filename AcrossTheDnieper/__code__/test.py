import random

randomRGBValues = random.sample(range(0, 16777216), 30)
for data in randomRGBValues:
    r = data//65536
    g = data%65536
    b = g//256
    g %= 256
    print (r,g,b)