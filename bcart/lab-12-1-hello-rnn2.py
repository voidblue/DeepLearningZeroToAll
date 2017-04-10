# Lab 12 RNN
import tensorflow as tf
import numpy as np

class XXX:
    X = None
    Y = None

    _states = None

    hypothesis = None
    cost_function = None

    optimizer = None
    prediction = None

    def set_placeholder(self, seq_len, hidden_size):
        self.X = tf.placeholder(tf.float32, [None, seq_len, hidden_size])  # None, 6, 5, X one-hot
        self.Y = tf.placeholder(tf.int32, [None, seq_len])  # Y label

    def rnn_lstm_cell(self, hidden_size, batch_size ):
        #cell = tf.nn.rnn_cell.BasicLSTMCell(num_units=hidden_size, state_is_tuple=True)
        cell = tf.contrib.rnn.core_rnn_cell.BasicLSTMCell(num_units=hidden_size, state_is_tuple=True)
        initial_state = cell.zero_state(batch_size, tf.float32)
        outputs, self._states = tf.nn.dynamic_rnn(cell, self.X, initial_state=initial_state, dtype=tf.float32)

        return outputs

    def  set_hypothesis(self, output):
        self.hypothesis = output

    def set_cost_function(self, batch_size, seq_len):
        weights = tf.ones([batch_size, seq_len])
        self.cost_function = tf.contrib.seq2seq.sequence_loss(logits=self.hypothesis, targets=self.Y, weights=weights)
        #sequence_loss = tf.nn.seq2seq.sequence_loss_by_example(logits=outputs, targets=Y, weights=weights)

    def set_optimizer(self, l_rate):
        self.optimizer = tf.train.AdamOptimizer(learning_rate=l_rate).minimize(tf.reduce_mean(self.cost_function))

    def learn(self, xonehot, ydata):
        tf.set_random_seed(777)  # reproducibility

        input_dim = 5  # one-hot size

        hidden_size = 5  # output from the LSTM. 5 to directly predict one-hot
        batch_size = 1   # one sentence
        sequence_length = 6  # |ihello| == 6

        self.set_placeholder(seq_len=6, hidden_size=5)
        logits = self.rnn_lstm_cell(5, 1) #hidden_size

        self.set_hypothesis(logits)
        self.set_cost_function(batch_size=1, seq_len=6)

        self.set_optimizer(0.1)

        self.prediction = tf.argmax(logits, axis=2)

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

        for i in range(100):
            err, _ = self.sess.run([self.cost_function, self.optimizer], feed_dict={self.X: xonehot, self.Y: ydata})

            result = self.sess.run(self.prediction, feed_dict={self.X: x_one_hot})
            print(i, "Error:", err, "prediction: ", result, "True Y: ", ydata)

            # print char using dic
            result_str = [idx2char[c] for c in np.squeeze(result)]
            print("\tPrediction str: ", ''.join(result_str))

    def what_is_next(self, char_data):
        result = self.sess.run(self.prediction, feed_dict={self.X: char_data})
        print("My suggestion is ", result)


idx2char = ['h', 'i', 'e', 'l', 'o']

# hihell -> ihello
# h->i, i->h, h->e, e->l, l->l, l->o
x_data = [[0, 1, 0, 2, 3, 3]]  # hihell
y_data = [[1, 0, 2, 3, 3, 4]]  # ihello

x_one_hot = [[[1, 0, 0, 0, 0],   # 0 h
              [0, 1, 0, 0, 0],   # 1 i
              [1, 0, 0, 0, 0],   # 0 h
              [0, 0, 1, 0, 0],   # 2 e
              [0, 0, 0, 1, 0],   # 3 l
              [0, 0, 0, 1, 0]]]  # 3 l

gildong = XXX()
gildong.learn(x_one_hot, y_data)
gildong.what_is_next(x_one_hot)


'''
0 loss: 1.55474 prediction:  [[3 3 3 3 3 3]] True Y:  [[1, 0, 2, 3, 3, 4]]
	Prediction str:  llllll

97 loss: 0.671109 prediction:  [[1 0 2 3 3 4]] True Y:  [[1, 0, 2, 3, 3, 4]]
	Prediction str:  ihello
98 loss: 0.670507 prediction:  [[1 0 2 3 3 4]] True Y:  [[1, 0, 2, 3, 3, 4]]
	Prediction str:  ihello
99 loss: 0.669884 prediction:  [[1 0 2 3 3 4]] True Y:  [[1, 0, 2, 3, 3, 4]]
	Prediction str:  ihello
'''