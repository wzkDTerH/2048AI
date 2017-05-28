# -*- coding: utf-8 -*-
"""
Created on Sun May 28 13:18:54 2017

@author: wzkdterh
"""
import tensorflow as tf
import numpy as np
import sys
def weight_variable(shape):
	return tf.Variable(tf.truncated_normal(shape, stddev=0.1))

def bias_variable(shape):
	return tf.Variable(tf.constant(0.1, shape=shape))
def conv2d(x, W,padding='VALID'):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding=padding)

def pool_2x2(x,stride,padding='VALID'):
	pmax=tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
	                       strides=[1, stride, stride, 1], padding=padding)
	pavg=tf.nn.avg_pool(x, ksize=[1, 2, 2, 1],
	                       strides=[1, stride, stride, 1], padding=padding)
	pmin=-tf.nn.max_pool(-x, ksize=[1, 2, 2, 1],
	                       strides=[1, stride, stride, 1], padding=padding)
	return tf.concat(3,[pmax,pavg,pmin])

class nn_model:
	def __init__(self):
		self.savedir=sys.path[0]+"/nn_model/nn.ckpt"
		self.buildModel()
		self.sess = tf.Session()
		self.loaded=False
		try:
			self.loadModel()
		except:
			pass
	def __del__(self):
		self.sess.close()
	def buildModel(self):
		self.x_input = tf.placeholder(tf.float32, [None, 4,4])
		self.x = tf.reshape(self.x_input, [-1,4,4,1])

		self.W_conv1_1 = weight_variable([1, 1, 1, 3])
		self.b_conv1_1 = bias_variable([3])
		#4*4*3
		self.h_conv1_1= tf.nn.relu(conv2d(self.x,self.W_conv1_1) +self.b_conv1_1)
		#2*2*9
		self.h_pool1_1 = pool_2x2(self.h_conv1_1,stride=2)

		self.W_conv1_2 = weight_variable([2, 2, 1, 3])
		self.b_conv1_2 = bias_variable([3])
		#3*3*3
		self.h_conv1_2= tf.nn.relu(conv2d(self.x,self.W_conv1_2) +self.b_conv1_2)
		#2*2*9
		self.h_pool1_2 = pool_2x2(self.h_conv1_2,stride=1)

		self.W_conv1_3 = weight_variable([3, 3, 1, 6])
		self.b_conv1_3 = bias_variable([6])
		#2*2*6
		self.h_conv1_3= tf.nn.relu(conv2d(self.x,self.W_conv1_3) +self.b_conv1_3)

		#2*2*24
		self.h_pool1=tf.concat(3,[self.h_pool1_1,self.h_pool1_2,self.h_conv1_3])
		self.W_conv2 = weight_variable([2, 2, 24, 24*9])
		self.b_conv2 = bias_variable([24*9])
		#1*1*(24*9)
		self.h_conv2= tf.nn.relu(conv2d(self.h_pool1,self.W_conv2) +self.b_conv2)
		#1*1*(24*3)
		self.h_pool2 = pool_2x2(self.h_pool1,stride=1)

		#1*1*(24*12)
		self.h_comb=tf.concat(3,[self.h_conv2,self.h_pool2])
		#(24*12)
		self.h_flat = tf.reshape(self.h_comb, [-1, 1*1*(24*12)])


		self.W_fc1 = weight_variable([24*12,24])
		self.b_fc1 = bias_variable([24])
		#24
		self.h_fc1 = tf.nn.relu(tf.matmul(self.h_flat, self.W_fc1)+self.b_fc1)
		self.keep_prob = tf.placeholder("float")
		self.h_fc1_drop = tf.nn.dropout(self.h_fc1,self.keep_prob)

		self.W_fc2 = weight_variable([24,1])
		self.b_fc2 = bias_variable([1])
		self.y = tf.nn.relu(tf.matmul(self.h_fc1_drop, self.W_fc2)+self.b_fc2)

		self.y_std = tf.placeholder("float", shape=[None, 1])

		self.cross_entropy = tf.nn.l2_loss(self.y_std-self.y)
		self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)
		self.saver = tf.train.Saver()


	def saveModel(self):
		self.saver.save(self.sess, self.savedir)

	def loadModel(self,enforce=False):
		if((self.loaded) and (not enforce)): return
		try:
			self.saver.restore(self.sess, self.savedir)
		except:
			self.sess.run(tf.initialize_all_variables())
			print "no save file"
			self.saveModel(self.sess)
		self.loaded=True

	def run(self,table):
		self.loadModel()
		batch_xs=np.array(table)
		y=self.sess.run(self.y, feed_dict={self.x_input: batch_xs,self.keep_prob: 1})
		return y

	def train(self,getData,Ttotal=100):
		self.loadModel()
		for T in range(Ttotal):
			print 'T:',T,
			_batch_xs, _batch_ys = getData()
			print "len(_batch_xs):",len(_batch_xs)
			batch_xs=np.array(_batch_xs)
			batch_ys=np.array(_batch_ys)
			if(T%10==0):
				L2=self.sess.run(self.cross_entropy, feed_dict={self.x_input: batch_xs,
				                                                self.y_std: batch_ys,
				                                                self.keep_prob: 1})
				print 'T:',T,'L2',L2
			self.sess.run(self.train_step, feed_dict={self.x_input: batch_xs,
			                                          self.y_std: batch_ys,
			                                          self.keep_prob: 0.5})
			if(T%50==0):
				self.saveModel()
			self.saveModel()

