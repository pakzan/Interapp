ACTIONS = [
    'change topic',
    'engage in discussion',
    'deepen the topic',
    'slow down',
    'cool down',
    'speed up',
    'stop and listen',
    'open conversation',
    'ask questions',
    'pay attention'
]
DISPLAY_ACTION_NUM = 3
D2V_MODEL_PATH = "data/d2v.model"
UPDATE_PATH = "data/update.txt"
TRAIN_PATH = "data/user_train.txt"
MODEL_PATH = "data/model.h5"
EMO_LIST = ('Neutrality', 'Happiness', 'Sadness', 'Anger', 'Fear')

DEBUG = False
EMPTY_FACE_PROB = (0, 0, 0)
EMPTY_VOICE_PROB = (0, 0, 0, 0, 0)

INPUT_SIZE = len(EMPTY_FACE_PROB) + len(EMPTY_VOICE_PROB)
