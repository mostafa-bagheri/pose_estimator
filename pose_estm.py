'''
Created on Feb 17, 2019
@author: Mostafa Bagheri
'''

import numpy as np
import csv


def read_data(i):
	'''
	As 6 dataset were provided, then "i" could be from 0 to 5.
	'''
	with open('dataset' + str(i) + '.csv') as csv_file:
		Lines = [line.split(' ,') for line in csv_file.readlines()[1:]]
		itr = len(Lines)
		t = np.zeros(itr)
		enc = np.zeros(itr)
		ang_v = np.zeros(itr)
		steering_ang = np.zeros(itr)
		for j in xrange(itr):
			data = Lines[j][0].split(',')
			t[j] = float(data[0])
			enc[j] = int(data[1])
			ang_v[j] = float(data[2])
			steering_ang[j] = float(data[3])

	return (t, steering_ang, enc, ang_v)


def estimate (t, steering_ang, enc, ang_v):
	'''
	The outputs of this function are,
		estimated_pose: Estimated pose of mobile robot
		estimated_pose_S: Estimated pose of front wheel position and steering angle
	'''
	front_wheel_radius_meters = 0.1250
	distance_between_rear_wheels = 0.3673
	distance_from_front_wheel_back_axis = 0.964
	front_circumference = 2 * np.pi * front_wheel_radius_meters
	ticks_per_rev = 35136

	estimated_pose = np.zeros((3, itr + 1))
	estimated_pose_S = np.zeros((3, itr + 1))

	# Initial pose is assumed to be (0, 0, 0)
	estimated_pose[:, 0] = np.array([0.0 , 0.0, 0.0])
	estimated_pose_S[:, 0] = np.array([distance_from_front_wheel_back_axis, 0, steering_ang[0]])

	for i in xrange(1, itr):
		dt = t[i] - t[i - 1]
		denc = enc[i] - enc[i - 1]
		ds = (float(denc)/ticks_per_rev) * front_circumference
		estimated_pose[2, i] = ang_v[i]*dt + estimated_pose[2, i - 1]
		estimated_pose_S[2, i] = steering_ang[i] + estimated_pose[2, i]
		estimated_pose_S[0, i] = estimated_pose_S[0, i - 1] + ds*np.cos(estimated_pose_S[2, i])
		estimated_pose_S[1, i] = estimated_pose_S[1, i - 1] + ds*np.sin(estimated_pose_S[2, i])
		estimated_pose[0, i] = estimated_pose_S[0, i] - distance_from_front_wheel_back_axis * np.cos(estimated_pose[2, i])
		estimated_pose[1, i] = estimated_pose_S[1, i] - distance_from_front_wheel_back_axis * np.sin(estimated_pose[2, i])

	return estimated_pose, estimated_pose_S


def animate(t, estimated_pose, estimated_pose_S):
	'''
	The animation illustrates the motion of mobile robot and is showing the front wheel streeing direction.
	'''
	import matplotlib.pyplot as plt
	from matplotlib.patches import Rectangle
	

	distance_between_rear_wheels = 0.3673
	distance_from_front_wheel_back_axis = 0.964

	plt.figure()
	plt.rc('font', family='serif')
	plt.rc('xtick', labelsize=18)
	plt.rc('ytick', labelsize=18)
	plt.ylabel('Y', fontsize=22)
	plt.xlabel('X', fontsize=22)
	plt.tight_layout()

	# For the first dataset (dataset0.csv), it seems mobile roobt is not moving for the frist 1000 data
	# then "i" can start from 1000
	i = 0
	while (True and i < itr):
		try:
			x_rec = estimated_pose[0, i] + (distance_between_rear_wheels/2.0) * np.sin(estimated_pose[2, i])
			y_rec = estimated_pose[1, i] - (distance_between_rear_wheels/2.0) * np.cos(estimated_pose[2, i])
			rect = Rectangle(xy=(x_rec, y_rec), width=distance_from_front_wheel_back_axis, height=distance_between_rear_wheels, angle=estimated_pose[2,i] * 180.0/np.pi, edgecolor='#FF3300')
			plt.plot(estimated_pose[0, i], estimated_pose[1, i], 'bo', linewidth=2, markersize=2)
			ax = plt.gca()
			plt.xlim(estimated_pose[0, i] - 5, estimated_pose[0, i] + 5)
			plt.ylim(estimated_pose[1, i] - 5, estimated_pose[1, i] + 5)
			plt.ylabel('Y', fontsize=22)
			plt.xlabel('X', fontsize=22)
			plt.grid(True)
			ax.add_artist(rect)
			ax.text(estimated_pose[0, i] - 4.5, estimated_pose[1, i] - 4.5, 't = ' + str(t[i]), fontsize=12)
			ax.arrow(estimated_pose_S[0, i], estimated_pose_S[1, i], \
						0.3*np.cos(estimated_pose_S[2, i]), 0.3*np.sin(estimated_pose_S[2, i]), \
						head_width=0.1, head_length=0.2, fc='k', ec='k')
			plt.hold(False)
			plt.pause(0.00001)
			i += 1
		except KeyboardInterrupt:
			print "\n Proram ended by user. \n"
			break


if __name__ == "__main__":
	
	# Reading Data
	data_index = 1
	t, steering_ang, enc, ang_v = read_data(data_index)
	itr = len(t)

	# Estimate Pose of mobile platform (estimated_pose) and fron wheel (estimated_pose_S)
	estimated_pose, estimated_pose_S = estimate (t, steering_ang, enc, ang_v)

	# This dunction illustrates the motion of mobile robot
	animate(t, estimated_pose, estimated_pose_S)


	