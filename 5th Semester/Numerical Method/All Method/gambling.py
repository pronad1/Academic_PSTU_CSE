import random
import numpy as np

total_cost=0
total_income =0

for game in range(100):
    x=0
    h = 0
    t = 0
    while(1):
        x+=1
        total_cost +=1
        r = random.randint(0,1)
        if r==0:
            h+=1
        else:
            t+=1
        dif = abs(h-t)

        if(dif>=3):
            print("won 8 dollar cost ",x,"dollar")
            total_income += 8
            break
print('Total Cost ',total_cost," Total Income ",total_income)