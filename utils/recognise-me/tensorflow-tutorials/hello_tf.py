import tensorflow as tf

x = tf.constant(5)
y = tf.constant(7)

result = tf.multiply(x,y)

with tf.Session() as session:
	output = session.run(result)
	print(output)
#print(result)