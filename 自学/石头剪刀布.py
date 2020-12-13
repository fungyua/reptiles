import random
import sys

user = int(input('请输入石头(0),剪刀(1),布(2)'))
machine = random.randint(0, 2)
tips = ['平手', '你输了', '你赢了']
model = ['石头', '剪刀', '布']
if not 0 <= user <= 2:
    print('请输入(0,1,2)')
    sys.exit()
print('你出了%s,机器人出了%s' % (model[user], model[machine]))
if user == 0:
    if machine == 0:
        print(tips[0])
    elif machine == 1:
        print(tips[2])
    else:
        print(tips[1])
elif user == 1:
    if machine == 0:
        print(tips[1])
    elif machine == 1:
        print(tips[0])
    else:
        print(tips[2])
elif user == 2:
    if machine == 0:
        print(tips[2])
    elif machine == 1:
        print(tips[1])
    else:
        print(tips[0])
