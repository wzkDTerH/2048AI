# -*- coding: utf-8 -*-
"""
Created on Sun May 28 01:20:00 2017

@author: wzkdterh
"""
import model2048
import tensorflow as tf

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
		self.buildModel()
		try:
			self.loadModel()
		except:
			pass
	def buildModel(self):
		self.x_input = tf.placeholder(tf.float32, [None, 4*4])
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

		self.W_conv2 = weight_variable([2, 2, 1, 9])
		self.b_conv2 = bias_variable([9])
		#1*1*(24*9)
		self.h_conv2= tf.nn.relu(conv2d(self.h_pool1,self.W_conv2) +self.b_conv2)
		#1*1*(24*3)
		self.h_pool2 = pool_2x2(self.h_pool1,stride=1)

		#1*1*(24*12)
		self.h_comb=tf.concat(3,[self.h_conv2,self.h_pool2])

		self.h_flat = tf.reshape(self.h_comb, [-1, 1*1*(24*12)])


		self.W_fc1 = weight_variable([24*12,24])
		self.b_fc1 = bias_variable([24])
		self.h_fc1 = tf.nn.relu(tf.matmul(self.h_flat, self.W_fc1)+self.b_fc1)

		self.keep_prob = tf.placeholder("float")
		self.h_fc1_drop = tf.nn.dropout(self.h_fc1,self.keep_prob)
		self.W_fc2 = weight_variable([24,1])
		self.b_fc2 = bias_variable([1])
		self.y = tf.nn.relu(tf.matmul(self.h_fc1_drop, self.W_fc2)+self.b_fc2)
		self.y_std = tf.placeholder("float", shape=[None, 1])

#		self.cross_entropy = -tf.reduce_sum(self.y_std*tf.log(self.y))
#		self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)
		self.saver = tf.train.Saver()


	def saveModel(self):
		pass
	def loadModel(self):
		pass
	def run(self,table):
		pass
	def train(self,dateset):
		pass

class AI2048_ml:
	def __init__(self,model):
		self.model=model
		self.model.Init()
	def run(self,draw=True):
		pass

if(__name__=='__main__'):
	AI=AI2048_ml(model2048.model2048())
	AI.run()
