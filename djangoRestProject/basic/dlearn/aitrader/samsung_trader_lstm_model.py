import os
import sys
from enum import Enum

import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Dense, LSTM
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from admin.path import dir_path
from abc import abstractmethod, ABCMeta

class ModelType(Enum):
    dnn_model = 1
    dnn_ensemble = 2
    lstm_model = 3
    lstm_ensemble = 4

class AiTradeBase(metaclass=ABCMeta): #
    @abstractmethod
    def split_sy5(self, **kwargs): pass
    
    @abstractmethod
    def create(self): pass

class SamsungTraderLstmModel(object):
    def __int__(self):
        global samsung
        samsung = np.load('./data/samsung.npy', allow_pickle=True)

    def split_xy5(self, dataset, time_steps, y_column):
        x, y = [], []
        for i in range(len(dataset)):
            x_end_number = i + time_steps
            y_end_number = x_end_number + y_column

            if y_end_number > len(dataset):
                break
            tmp_x = dataset[i:x_end_number]
            tmp_y = dataset[x_end_number:y_end_number, 0]
            x.append(tmp_x)
            y.append(tmp_y)
        return np.array(x), np.array(y)

    def create_lstm_model(self):
        samsung = np.load('./data/samsung.npy', allow_pickle=True)
        path = dir_path('aitrader')
        x, y = self.split_xy5(samsung, 5, 1)
        #print(x[0, :], '\n', y[0])
        #print(x.shape)
        #print(y.shape)


        x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.3)
        #print(x_train.shape)
        #print(x_test.shape)
        #print(y_train.shape)
        #print(y_test.shape)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1] * x_train.shape[2]))
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1] * x_test.shape[2]))  #x_train과 x_test의 차원 축소
        #print(f"reshape 된 xtrain {x_train.shape}")
        #print(f"reshape 된 xtest {x_test.shape}")



        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(x_test)
        x_train_scaled = np.reshape(x_train_scaled, (x_train_scaled.shape[0], 5, 5))
        x_test_scaled = np.reshape(x_test_scaled, (x_test_scaled.shape[0], 5, 5))

        model = Sequential()
        model.add(LSTM(64, input_shape=(5, 5))) # add
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam', metrics=['mse']) # compile

        early_stopping = EarlyStopping(patience=20)
        x_train_scaled = x_train_scaled.astype(np.float32)
        x_test_scaled = x_test_scaled.astype(np.float32)
        y_train = y_train.astype(np.float32)
        y_test = y_test.astype(np.float32)
        np.set_printoptions(threshold=sys.maxsize)
        model.fit(x_train_scaled, y_train, validation_split=0.2, verbose=1, batch_size=1, epochs=100, callbacks=[early_stopping]) # fit : batch_size, epochs

        loss, mse = model.evaluate(x_test_scaled, y_test, batch_size=1) #test(반복x)
        print('loss : ', loss)
        print('mse : ', mse)
        y_pred = model.predict(x_test_scaled)

        for i in range(5):
            print('종가 : ', y_test[i], '/예측가 : ', y_pred[i])
        file_name = os.path.join(path, "save", "samsung_stock_lstm_model.h5")
        print(f"저장경로: {file_name}")
        model.save(file_name)




if __name__ == '__main__':
    SamsungTraderLstmModel().create_lstm_model()