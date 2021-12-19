import os
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from doc2vec import load_model as load_dv2_model
from constant import INPUT_SIZE, ACTIONS, D2V_MODEL_PATH


#get doc vectors as doc_vectors
d2v_model = load_dv2_model(D2V_MODEL_PATH)
vec_size = np.shape(d2v_model.docvecs.doctag_syn0)[1]
doc_vectors = d2v_model.docvecs.doctag_syn0

def get_model(model_path=''):
    if os.path.exists(model_path):
        return load_model(model_path)

    model = Sequential()
    model.add(Dense(8, activation='relu', input_shape=(INPUT_SIZE, )))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(vec_size, activation='softmax'))
    model.compile(optimizer = 'adam',
                loss = 'categorical_crossentropy',
                metrics = ['accuracy'])
    return model

def load_data(train_path):
    #get x_train from user_train
    with open(train_path, 'r') as f:
        user_train = f.read().splitlines()
        x, y = [], []
        for s in user_train:
            xs, action = s.split(':')
            # get emotion probabilities            
            x.append([float(v) for v in xs.split(',')])
            # get position of string in data.txt, then find the respective vectors
            y.append(doc_vectors[ACTIONS.index(action)])

    x, y = np.array(x), np.array(y)
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.15, shuffle=True)
    return (x_train, x_val), (y_train, y_val)

def train_model(x_data, y_data, model=get_model()):
    x_train, x_val = x_data
    y_train, y_val = y_data
    model.fit(x_train,
            y_train,
            epochs=10,
            batch_size=4,
            validation_data=(x_val, y_val))
    return model

def save_model(model, model_path):
    model.save(model_path)
    print("Model saved in path: %s" % model_path)