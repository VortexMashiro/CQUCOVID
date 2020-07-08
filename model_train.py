import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.autograd import Variable
import os


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

# 文件操作
path_data = './data/country-epidemic-summary/'
path_list = os.listdir(path_data)
path_list.sort()
path_model = './model/'
data_type = '.csv'
model_type = '.pth'

# 循环训练模型，保存模型
for filename in path_list:
    f = open(path_data + filename)
    df = pd.read_csv(f)
    f.close()

    # df = pd.read_csv('./data/China (mainland).csv')
    value = df['Confirmed'].values[:]

    # 数据标准化
    dataset = value.astype('float32')
    max_value = np.max(dataset)
    min_value = np.min(dataset)
    scalar = max_value - min_value
    dataset = list(map(lambda x: x / scalar, dataset))


    def create_dataset(dataset, look_back=2):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back):
            a = dataset[i:(i + look_back)]
            dataX.append(a)
            dataY.append(dataset[i + look_back])
        return np.array(dataX), np.array(dataY)

    # 创建好输入输出
    data_X, data_Y = create_dataset(dataset)

    # 划分数据集
    train_size = len(data_X)
    train_X = data_X[:train_size]
    train_Y = data_Y[:train_size]

    train_X = train_X.reshape(-1, 1, 2)
    train_Y = train_Y.reshape(-1, 1, 1)

    train_x = torch.from_numpy(train_X)
    train_y = torch.from_numpy(train_Y)

    # 定义网络结构
    model = lstm_reg(2, 4)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
    loss_func = nn.MSELoss()
    model.train()
    # 开始训练
    epoch = 200
    for e in range(epoch):
        var_x = Variable(train_x)
        var_y = Variable(train_y)
        # 前向传播
        out = model(var_x)
        loss = criterion(out, var_y)
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        # 更新参数
        optimizer.step()
        # 损失函数监控
        # if (e + 1) % 100 == 0:
        #     print('Epoch:{}, Loss:{:.5f}'.format(e + 1, loss.item()))

    # 保存模型
    model_name=(filename.split('.'))[0]
    torch.save(model, (path_model + model_name + model_type))
    print(filename + "\t\tFinish.")  # 提示完成

print("All finish.")   # 全部完成


