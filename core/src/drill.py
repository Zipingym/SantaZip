import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Input, Flatten, Dropout
from keras.utils import to_categorical, plot_model
from sklearn.model_selection import train_test_split 
from keras.optimizers import RMSprop, Adam
from keras.losses import CategoricalCrossentropy 
import numpy as np
import processer as util
from sklearn.model_selection import train_test_split

  
model = Sequential([
            Input(shape=(66)),
            Dense(33, activation=tf.nn.relu),
            Dropout(0.3),
            Dense(11, activation=tf.nn.relu),
            Dropout(0.2),
            Dense(2, activation=tf.nn.tanh)
        ])

x_data = []
y_data = []

loader = util.CSVLoader()
# processer = util.MultiProcesser(
#     [
#         util.AngleProcesser(),
#         util.DistanceProcesser()
#     ]
# )
processer = util.DistanceProcesser()

stand_data = loader('./data/stand/dataset.csv')
left_data = loader('./data/ldumble/dataset.csv')
right_data = loader('./data/rdumble/dataset.csv')
down_data = loader('./data/dumble/dataset.csv')

for load in stand_data:
    x_data.append(processer(load))
    y_data.append([0, 0])
for load in left_data:
    x_data.append(processer(load))
    y_data.append([1, 0])
for load in right_data:
    x_data.append(processer(load))
    y_data.append([0, 1])
for load in down_data:
    x_data.append(processer(load))
    y_data.append([1, 1])

x_data = np.array(x_data)
y_data = np.array(y_data)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=1)


model.compile(optimizer=Adam(),
          loss="binary_crossentropy",
          metrics=['accuracy'])

model.fit(
    x=x_data,
    y=y_data,
    validation_data=(x_test, y_test),
    epochs=256, 
    batch_size=32,
    verbose=1,
)

model.save('./dist/temp.h5')