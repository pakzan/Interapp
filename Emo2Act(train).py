import tensorflow as tf
import numpy as np
from gensim.models.doc2vec import Doc2Vec

model = Doc2Vec.load("data/d2v.model")
#get doc vectors as y_label
y_label = model.docvecs.doctag_syn0
#get the size of y_label
doc_size, vec_size = np.shape(y_label)
#num of probability emotion as input
inp_size = 10
#set temporary x_train
x_train = np.random.rand(doc_size, inp_size)

#start of tensor flow
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
hidden_layer_2 = tf.add(tf.matmul(hidden_layer_1, weights['1']), biases['1'])
hidden_layer_3 = tf.add(tf.matmul(hidden_layer_2, weights['2']), biases['2'])
pred = tf.add(tf.matmul(hidden_layer_3, weights['out']), biases['out'])

# define the loss function
pred = tf.nn.l2_normalize(pred)
y = tf.nn.l2_normalize(y)
cos_sim = tf.reduce_sum(tf.multiply(pred, y))
loss = 1 - cos_sim

# define the training step:
train_step = tf.train.AdamOptimizer(0.1).minimize(loss)

#start session
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

n_iters = 1000
# train for n_iter iterations
for epoch in range(n_iters):
    index = epoch % doc_size

    x_reshape = np.reshape(x_train[index], [-1, inp_size])
    y_reshape = np.reshape(y_label[index], [-1, vec_size])
    
    sess.run(train_step, feed_dict={x: x_reshape, y: y_reshape})
    
    if epoch % 101 == 0:
        _pred, _loss = sess.run([pred, loss], feed_dict={
             x: x_reshape, y: y_reshape})
        similar_doc = model.docvecs.most_similar(_pred)[0]
        print(index, similar_doc, _loss)

saver = tf.train.Saver()
save_path = saver.save(sess, "data/model.ckpt")
print("Model saved in path: %s" % save_path)
