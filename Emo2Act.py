import tensorflow as tf
import numpy as np
from gensim.models.doc2vec import Doc2Vec
import time
import os
# UI module
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# own module
import EmoVoice

# get trained model
model = Doc2Vec.load("data/d2v.model")
#get the vec_size of actions, and inp_size of probability
vec_size = np.shape(model.docvecs.doctag_syn0)[1]
inp_size = 10

# initialize tensor flow variables
#---------------------------------------------------------start of tensor flow initialization
x = tf.placeholder(tf.float32, shape=(1, inp_size))
y = tf.placeholder(tf.float32, shape=(1, vec_size))

n_hidden = 128  # you can choose your own number
#output node weights and biases
weights = {
    'in': tf.Variable(tf.random_normal([inp_size, n_hidden])),
    '1': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    '2': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'out': tf.Variable(tf.random_normal([n_hidden, vec_size]))
}
biases = {
    'in': tf.Variable(tf.random_normal([n_hidden])),
    '1': tf.Variable(tf.random_normal([n_hidden])),
    '2': tf.Variable(tf.random_normal([n_hidden])),
    'out': tf.Variable(tf.random_normal([vec_size]))
}

#proceed to hidden layer
hidden_layer_1 = tf.add(tf.matmul(x, weights['in']), biases['in'])
hidden_layer_2 = tf.add(
    tf.matmul(hidden_layer_1, weights['1']), biases['1'])
hidden_layer_3 = tf.add(
    tf.matmul(hidden_layer_2, weights['2']), biases['2'])
pred = tf.add(tf.matmul(hidden_layer_3, weights['out']), biases['out'])
#---------------------------------------------------------end of tensor flow initialization

#start TF session
sess = tf.Session()
saver = tf.train.Saver()
saver.restore(sess, "data/model.ckpt")


def updateProgBar():
    total_prog_dif = 0
    # update all progress bars
    for i in range(len(emoList)):
        prog_dif = emoVoiceProb[i] - prog_var[i].get()
        prog_var[i].set(prog_var[i].get() + prog_dif / 30)
        total_prog_dif += prog_dif
    #if no update done(finished update), return false
    return round(total_prog_dif) != 0

# number of actions to show in UI
actionNo = 3
#global variables for main()
last_action = time.time()
emoVoiceProb = [0] * 5
x_inp = [0] * inp_size
# main loop
def main():
    global last_action, emoVoiceProb, x_inp

    # get emotion Probabilities after progress bar done animate
    # update progress bar value
    if not updateProgBar():
        # voiceProb = [neutrality, happiness, sadness, anger, fear]
        try:
            emoVoiceProb = qVoice.get(False)
        except queue.Empty:
            pass


    # update action every 1 second
    if time.time() - last_action > 1:
        #get input emotion
        x_inp = emoVoiceProb + emoVoiceProb

        #get suggessted action
        x_reshape = np.reshape(x_inp, [-1, inp_size])
        _pred = sess.run(pred, feed_dict={x: x_reshape})

        #find the most similiar doc vectors
        similar_doc = model.docvecs.most_similar(_pred)
        # print(similar_doc)
            
        for i in range(actionNo):
            action_ind = int(similar_doc[i][0])
            act_text[i].set(data[action_ind])
            #set dont size according to confidence
            font_sz = max(10, round(40 * (similar_doc[i][1] - .6)))
            act_label[i].config(font=("Helvetica", font_sz))

        # update action label text
        last_action = time.time()

    # proceed next loop
    root.after(20, main)

# Thread for getting voice and face emotions
import threading
import queue

def getVoiceFaceEmo(qVoice):
    while (True):
        qVoice.put(EmoVoice.GetVoiceEmo())
qVoice = queue.Queue()
thread = threading.Thread(target=getVoiceFaceEmo,
                          name=getVoiceFaceEmo, args=(qVoice,))
thread.start()
# End Thread

# Get Action file
with open('data/data.txt', 'r') as myfile:
    data = myfile.read().splitlines()

# Tkinter
root = tk.Tk()
# set frame to organise the UI 
frame = tk.Frame(root)
frame.grid()
# Frame elements
#-----------------------------------EMOTION PROGRESS BARS
emoList = ['Neutrality', 'Happiness', 'Sadness', 'Anger', 'Fear']

start_h = 0
prog_var = [None] * len(emoList)
for i, emoName in enumerate(emoList):
    # set progress variable for further modification
    prog_var[i] = tk.DoubleVar()
    # set label and progress bar UI
    ttk.Label(frame, text=emoName).grid(row=i+start_h, column=1)
    ttk.Progressbar(frame, length=300, maximum=1, variable=prog_var[i]).grid(row=i+start_h, column=2)
#-----------------------------------EMOTION PROGRESS BARS END

#-----------------------------------ACTIONS LABEL AND BUTTON
start_h = len(emoList)
act_text = [None] * actionNo
act_label = [None] * actionNo
for i in range(actionNo):
    # set progress variable for further modification
    act_text[i] = tk.StringVar()
    # set action label UI
    act_label[i] = ttk.Label(frame, textvariable=act_text[i])
    act_label[i].grid(row=i + start_h, column=2)

    # set action button UI
    ttk.Button(frame, text='Helpful', command=lambda i=i: train(i)).grid(row=i+start_h, column=1)
#-----------------------------------ACTIONS LABEL AND BUTTON END

frame.pack(padx=20, pady=20)


#------------------------------------UPDATE SESSION
#update response for further machine learning
user_train = open("data/user_train.txt", "a")
def train(actionNo):
    global user_train, hasUpdate
    rounded_x = [float("%.2f" % e) for e in x_inp]
    user_train.write(str(rounded_x) + ':' + data[actionNo] + '\n')
    hasUpdate = True

# Prompt for update
hasUpdate = False
if os.path.exists("data/hasUpdate.txt"):
    if tk.messagebox.askquestion('Update', "New update available! Update?") == 'yes':
        import Emo2Act_train
        tk.messagebox.showinfo('Done', 'Update Successfully')
        os.remove("data/hasUpdate.txt")
    else:
       hasUpdate = True
       
# Close Tkinter event
def on_closing():
    global user_train, hasUpdate
    user_train.close()
    if hasUpdate:
        if tk.messagebox.askquestion('Update', "New update available! Update?") == 'yes':
            import Emo2Act_train
            tk.messagebox.showinfo('Done', 'Update Successfully')
        else:
            open("data/hasUpdate.txt", 'a').close()

    root.destroy()
#------------------------------------UPDATE SESSION END

root.protocol("WM_DELETE_WINDOW", on_closing)

# call UI every 0.001s
root.title("Interapp")
root.after(1, main)
root.mainloop()
