# Interapp

Interapp is a program that suggests user actions during a video call built on Machine Learning based on the emotion recognition of the image and audio of a video call.

The purposes of this project is to help user to notify the current emotion of the video calling subject and suggests them the action that could be taken to improve the mutual experiences of the video call. This is also useful for student that is taking video call as a type of interview, knowing the current emotion of the interviewer that initially could have gone unnoticed, might help student to avoid some pitfall of interview and thus getting a better result. 


# Overview

As a prototype, the python script will capture a specific windows on the screen and take computer own audio output as audio feed. Therefore, it given the script the capability to intergrate with any of the major conference or video call software including Skype, Facebook Messenger Call, Google Duo, etc

The structure of this project can roughly be separated into three part. 

## Image (Face Sentiment Analysis)
Although one always say he is deep with hiding their feeling, but almost everyone can't help but shown some of the emotion on their faces. By using Opencv library, we can extract faces inside the image efficiently thanks to its well implemented face detection function. Later the image with faces present is cropped then feed to the face emotion classifier built by Emopy one face at a time. 

The result of the classifier which constist of different percentage of similarity of each emotion is transfer to the action suggestion model for further training. 

## Voice (Real-time Speech Emotion Recognizer)
Speech Emotion or voice sentiment is also a hot topics with a lot of past research working on it. People tend to speak with increasing frequency when they are happy or interested, while talking in normalized pitch when they got bored. Although talking in different language and word, the base frequency of the speech is highly corelate to the speaker mood and emotion. 

By doing short-time Fourier Transform (STFT), we are able to obtain the intensity of frequency versus short time chart. This is particularly useful becuase it enable researcher to treat it as a 2D data classifiation problem after signal processing. 

In our project, this is assisted by the library Emovoice.

## Action Suggestion (Reinforcement Learning using TensorFlow)
By using the output from image and voice analysis, a Neural Network model with 128 hidden layers is self-trained. During the prototyping stage, user will get suggestion for action during the conversation in video call, eg. "Change topics", "Pay Attention!", etc. Then, user can rate its usefulness relate with the actual situation. The data will be submitted back to the program to further train the model at the end of the conversation so that the program will be even smarter. 

Some of the action suggestion including
- `change topic`
- `engage in discussion`
- `slow down`
- `speed up`
- `stop and listen`
- `open conversation`
- `ask questions`
- `pay attention`

Lastly, having the ability to capture image and sound of any program on computer, the program is not restricted on solely video call, but there is a vast possibility of it is capable of.
# Warps things up
Interapp would like to express our gratitude toward these awesome packages that make this project possible

- [Emopy](https://github.com/thoughtworksarts/EmoPy) -- A deep neural net toolkit for emotion analysis via Facial Expression Recognition (FER) by thoughtworksarts
- [Emovoice](https://github.com/hcmlab/emovoice) --Real-time Speech Emotion Recognizer by hcmlab
- [TensorFlow](https://www.tensorflow.org/tutorials/) --An open source machine learning framework for everyone
