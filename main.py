import time
import cv2
from threading import Thread
# UI module
import tkinter as tk
import numpy as np
# own module
import voice2emo
import face2emo
from constant import *
from classes import *
from doc2vec import load_model as load_d2v_model
from emo2act import load_data, train_model, get_model, save_model

def add_update(action):
    rounded_x = [round(e, 2) for e in face_prob + voice_prob]
    file_handler.add_update("%s:%s\n" % (','.join(str(v) for v in rounded_x), action))

def update_debug_mode():
    face2emo.debug = bool(debug_var.get())
    if not face2emo.debug:
        face2emo.destory_debug_window = True


def main(e2a_model, d2v_model, prev_pred_time):   
    # voiceProb = [neutrality, happiness, sadness, anger, fear]
    # faceProb = [anger, calm, happiness]
    # total_prob = [neutrality, happiness, sadness, anger, fear]
    # update all progress bars
    progress_win.update_label(0, (voice_prob[0] + face_prob[1]) / 2)
    progress_win.update_label(1, (voice_prob[1] + face_prob[2]) / 2)
    progress_win.update_label(2, voice_prob[2])
    progress_win.update_label(3, (voice_prob[3] + face_prob[0]) / 2)
    progress_win.update_label(4, voice_prob[4])

    # update action every 1 second
    if time.time() - prev_pred_time > 1:
        #get input emotion
        x_input = np.array([face_prob + voice_prob])

        #get suggessted action
        action_vec = e2a_model.predict(x_input)

        #find the most similiar doc vectors
        similar_doc = d2v_model.docvecs.most_similar(action_vec)
        for i in range(DISPLAY_ACTION_NUM):
            act_i, act_prob = similar_doc[i]
            font_sz = max(6, round(20 * (1 + act_prob)))
            action_win.update_label(i, ACTIONS[int(act_i)], font_sz)

        # update action label text
        prev_pred_time = time.time()

    # proceed next loop
    root.after(20, lambda: main(e2a_model, d2v_model, prev_pred_time))

# Prompt for update
def check_update():
    if file_handler.has_update() and\
        tk.messagebox.askquestion('Update', "New update available! Update?") == 'yes':
        file_handler.update_data()

        x_data, y_data = load_data(TRAIN_PATH)
        model = train_model(x_data, y_data)
        save_model(model, MODEL_PATH)

        tk.messagebox.showinfo('Done', 'Update Successfully')

# Close Tkinter event
def on_closing():
    global is_running
    is_running = False
    check_update()
    root.destroy()

def pred_voice():
    global voice_prob
    while is_running:
        voice_prob = tuple(voice2emo.pred_voice())

def pred_face():
    global face_prob
    while is_running:
        # get average face emotions
        face_prob = face2emo.pred_face_from_dimension(menu_win.win_dimen)
        cv2.waitKey(1)
    
voice_prob = EMPTY_VOICE_PROB
face_prob = EMPTY_FACE_PROB

if __name__ == "__main__":
    is_running = True
    file_handler = FileHandler(UPDATE_PATH, TRAIN_PATH)
    check_update()
    
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)    
    root.title("Interapp")

    menu_win = MenuWindow(root)
    progress_win = ProgressWindow(root, EMO_LIST)
    action_win = ActionWindow(root, DISPLAY_ACTION_NUM, add_update)
    debug_var = tk.IntVar()
    debug_cb = tk.Checkbutton(root, text="View Analysed Screen", variable=debug_var, command=update_debug_mode)
    debug_cb.pack()

    # not using daemon to close gracefully
    Thread(target=pred_voice, name=pred_voice).start()
    Thread(target=pred_face, name=pred_face).start()

    e2a_model = get_model(MODEL_PATH)
    d2v_model = load_d2v_model(D2V_MODEL_PATH)
    root.after(1, lambda: main(e2a_model, d2v_model, -1))
    root.mainloop()
