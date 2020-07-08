import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import torch
from torch import nn
from torch.autograd import Variable
import os
#import matplotlib.pyplot as plt

# 定义模型
class lstm_reg(nn.Module):
    def __init__(self, input_size, hidden_size, output_size=1, num_layers=2):
        super(lstm_reg, self).__init__()

        self.rnn = nn.LSTM(input_size, hidden_size, num_layers)
        self.reg = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x, _ = self.rnn(x)
        s, b, h = x.shape  # (seq, batch, hidden)
        x = x.view(s * b, h)
        x = self.reg(x)
        x = x.view(s, b, -1)
        return x


 # 数据集划分
def create_dataset(dataset, look_back=2):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)

def get_flag(a,n):
    sum = 0
    for i in a:
        sum = sum + i
    return sum/n

def get_to_int(pre):
    return round(pre)


# 文件操作
path_data = './data/country-epidemic-summary/'
path_list = os.listdir(path_data)
path_list.sort()
path_model = './model/'
data_type = '.csv'
model_type = '.pth'
pred_data = './prediction_data/'


# 循环训练模型，保存模型
for filename in path_list:

    # Worldwide United States China (mainland) Zimbabwe

    # 读取数据
    f = open(path_data + filename)
    df = pd.read_csv(f)
    f.close()
    # df = pd.read_csv('./data/China (mainland).csv')
    value = df['Confirmed'].values[:]

    # 数据量少于模型步长
    if (len(value) < 6):
        continue

    max_value = np.max(value)
    min_value = np.min(value)
    scalar_value = max_value - min_value
    if (scalar_value == 0):
        print('\t\t*************\t\t'+filename)
        continue  # 如果为0，不除以0


    # 数据预处理，标准化
    dataset = value.astype('float32')
    max_dataset = np.max(dataset)
    min_dataset = np.min(dataset)
    scalar = max_dataset - min_dataset
    dataset = list(map(lambda x: x / scalar, dataset))


    # 创建好输入输出
    data_X, data_Y = create_dataset(dataset)



    # 读取模型
    model_name=(filename.split('.'))[0]
    model = torch.load(path_model + model_name + model_type)
    # model = torch.load(path_model + filename + model_type)

    # model = model.eval()
    data_X = data_X.reshape(-1, 1, 2)
    data_X = torch.from_numpy(data_X)
    test_x = Variable(data_X)

    test_y = model(test_x)

    #构造验证集
    temp_x = test_x[-1:]
    temp_y = test_y[-1]

    # prediction_y.backward()
    pred_day=23
    pred_y = []
    for i in range(pred_day):
        temp_x[0][0][0]=temp_x[0][0][1]
        temp_x[0][0][1]=temp_y[0][0]
        # print(pred_x)
        # print(pred_y)
        pred_y.append(temp_y.item())
        # print(temp_x.tolist())
        temp_y = model(temp_x)
        # print(temp_y.item())


    # # 改变输出的格式
    test_y = test_y.view(-1).data.numpy()


    # 把数据改回原来的范围
    # dataset = list(map(lambda x: x * scalar, dataset))
    test_y = list(map(lambda x: x * scalar, test_y))
    pred_y = list(map(lambda x: x * scalar, pred_y))

    flag_len = 14
    flag_test = get_flag(test_y[-flag_len:],flag_len)
    flag_pred = get_flag(pred_y[2:flag_len+2],flag_len)
    if(flag_test >= flag_pred):
        for i in range(len(pred_y)):
            pred_y[i] = test_y[-2]

    # 误差函数
    def residuals(p, x, y):
        fun = np.poly1d(p)
        return y - fun(x)

    def fitting(p):
        pars = np.random.rand(p+1)
        r = leastsq(residuals, pars, args=(X, Y))
        return r

    pre_x = np.arange(0,len(value)+pred_day)
    X = np.arange(0,len(value))
    Y = np.array(value)
    fit_pars = fitting(5)[0]
    pre_y = np.poly1d(fit_pars)(pre_x)
    pred_fix = pre_y[-pred_day:]
    flag_fix = get_flag(pred_fix[:flag_len],flag_len)
    if(flag_fix > flag_test):
        test_y.extend(pred_fix)
    else:
        test_y.extend(pred_y)

    # 最终结果
    pred_result = test_y

    # 保存预测数据
    # with open((pred_data + model_name + '.txt'), 'w') as f:
    #     f.write(str(pred_result))
    #     f.close()
    # print(model_name + '.txt')

    name = ['Confirmed']
    if(len(pred_result)==0):
        continue
    savepre = pd.DataFrame(columns=name, data=pred_result)
    savepre.apply(get_to_int)
    savepre["Confirmed"] = savepre["Confirmed"].apply(get_to_int)
    savepre.to_csv(pred_data + model_name + '.csv', index=None)
    print(model_name + '.csv\tfinish.')


print("all model finish.")

