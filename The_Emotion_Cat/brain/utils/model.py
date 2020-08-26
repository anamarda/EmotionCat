from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D, AveragePooling2D

def create_model():
    model = Sequential()
    
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same', input_shape=(48,48,1)))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2)))
    
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2,2)))
    
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(3, 3), strides=(2,2)))
    
    model.add(Flatten())
    
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(7, activation='softmax'))
    
    return model
