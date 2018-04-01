## Original code: 
## https://pythonprogramming.net/cnn-tensorflow-convolutional-nerual-network-machine-learning-tutorial/?completed=/convolutional-neural-network-cnn-machine-learning-tutorial/

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot = True)

# number of classes of the data
n_classes = 10
# for loading only a part of the database
batch_size = 128

# creates variables to fill later according to the type & format specified
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

# neuron drop-out, 80% of nodes are kept
# avoid overfitting, works better with large amounts of data
keep_rate = 0.8
keep_prob = tf.placeholder(tf.float32)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def maxpool2d(x):
    #                        size of window         movement of window
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')


def convolutional_neural_network(x):
	# 5x5 convolution (+maxpool of window), 1-img -> 32 out
	# 5x5 convolution (+maxpool of window), 32 in -> 64 out
	# fully connected layer (imgs of 7x7), 7*7*64 inputs -> 1024 out
	# output, 1024 in -> 10 out (n_classes)

    weights = {'W_conv1':tf.Variable(tf.random_normal([5,5,1,32])),
               'W_conv2':tf.Variable(tf.random_normal([5,5,32,64])),
               'W_fc':tf.Variable(tf.random_normal([7*7*64,1024])),
               'out':tf.Variable(tf.random_normal([1024, n_classes]))}

    biases = {'b_conv1':tf.Variable(tf.random_normal([32])),
               'b_conv2':tf.Variable(tf.random_normal([64])),
               'b_fc':tf.Variable(tf.random_normal([1024])),
               'out':tf.Variable(tf.random_normal([n_classes]))}

    # reshapes img to "1 < 28, < 28, 1" 
    x = tf.reshape(x, shape=[-1, 28, 28, 1])

    # first convolution (+maxpool)
    conv1 = tf.nn.relu(conv2d(x, weights['W_conv1']) + biases['b_conv1'])
    conv1 = maxpool2d(conv1)
    
    # second convolution (+maxpool)
    conv2 = tf.nn.relu(conv2d(conv1, weights['W_conv2']) + biases['b_conv2'])
    conv2 = maxpool2d(conv2)

    # fully connected layer
    # reshape output of conv2 (1, 28, 28, 1) to match fc (whatever, 7*7*64)
    fc = tf.reshape(conv2,[-1, 7*7*64])
    fc = tf.nn.relu(tf.matmul(fc, weights['W_fc'])+biases['b_fc'])
    # only 80% of nodes are used 
    fc = tf.nn.dropout(fc, keep_rate)

    # output layer
    output = tf.matmul(fc, weights['out'])+biases['out']

    return output

def train_neural_network(x):
    prediction = convolutional_neural_network(x)
    # how wrong we are, differences between prediction & actual value
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(prediction,y) )
    # to optimise this cost
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    # cycles of feedforward+backprop
    hm_epochs = 10

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples/batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                # function returns 2 values, uses _ to catch first one (not useful, just to avoid error)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:',accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

train_neural_network(x)