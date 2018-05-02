import numpy as np
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import random

def predict(x1pts, ):






def hashCoords(x, y):
    return (y*1000 + x)/(608608)

def reverseHash(code):
    x = (code*608608)%1000
    y = (code*608608)//1000
    return (x, y)

#hash for 608 by 608 image coordinate: (y*1000 + x)/(608608)

def generateCoords(start, end, step):
    generated = []
    for x in range(start, end, step):
        generated.append((x + random.randint(-40, 40), (x * 0.005 * x) + random.randint(-40, 40)))
    return [hashCoords(x, y) for (x, y) in generated]


def generateCoords2(start, end, step):
    generated = []
    for x in range(start, end, step):
        generated.append((0.6 * x + random.randint(-40, 40), (x * 0.006 * x) + random.randint(-40, 40)))
    return [hashCoords(x, y) for (x, y) in generated]


def genSinCoords(start, end, step):
    generated = []
    period = (end - start) / 16
    for x in range(start, end, step):
        generated.append((2 * np.sin(period * x) + 2))
    return generated


def genData():
    generated = np.array(genSinCoords(100, 600, 1))
    generated2 = np.array(generateCoords2(100, 600, 1))

    generated3 = 1+np.array(genSinCoords(100, 600, 1))
    generated4 = 1+np.array(generateCoords2(100, 600, 1))

    plt.plot(generated, '-b')
    plt.plot(generated2, '-r')
    plt.plot(generated3, color='lightblue')
    plt.plot(generated4, color='orange')

    generated = generated.reshape(generated.shape[0], 1)
    generated2 = generated2.reshape(generated2.shape[0], 1)
    generated3 = generated3.reshape(generated3.shape[0], 1)
    generated4 = generated4.reshape(generated4.shape[0], 1)

    trainingSet = np.hstack((generated, generated3))
    testSet = np.hstack((generated2, generated4))

    return trainingSet, testSet

# def create_dataset(dataset, look_back=1):
#     dataX, dataY = [], []
#     for i in range(look_back, len(dataset)):
#         #a = dataset[i:(i+look_back)]
#         dataX.append(dataset[i])
#         dataY.append(dataset[i - look_back:i])
#     return np.array(dataX), np.array(dataY)
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), :]
#         a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, :])
#         dataY.append(dataset[i + look_back, 0])

    return np.array(dataX), np.array(dataY)

def train():
    look_back = 5
    trainingSet, testSet = genData()
    trainX, trainY = create_dataset(trainingSet, look_back)#[:len(trainingSet)-1], trainingSet[1:]
    print(np.shape(trainX))
    print(np.shape(trainY))
    trainX = np.reshape(trainX, (trainX.shape[0], 2, trainX.shape[1]))

    model = Sequential()
    model.add(LSTM(4, input_shape=(2, look_back)))
    model.add(Dense(2))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=25, batch_size=1, verbose=2)

    testX, testY = create_dataset(testSet, look_back)  # testSet[:len(testSet)-1], testSet[1:]
    # testX = testX.reshape(testX.shape[0], 1)
    # testY = testY.reshape(testY.shape[0], 1)
    testX = np.reshape(testX, (testX.shape[0], 2, testX.shape[1]))
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    trainScore = math.sqrt(mean_squared_error(trainY[:], trainPredict[:, :]))
    print('Train Score: %.4f RMSE' % (1 - trainScore))
    testScore = math.sqrt(mean_squared_error(testY[:], testPredict[:, :]))
    print('Test Score: %.4f RMSE' % (1 - testScore))