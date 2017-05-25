
import os
import json
import math

excluded_ids = ['43259']
excluded_from_a = excluded_ids + ['56640']
excluded_from_b = excluded_ids
all_excluded = set(excluded_from_a + excluded_from_b)

def load_user_ids():
	with open('experiment_ids.txt', 'r') as f:
		s = f.read()
	return [ x.split('\t') for x in s.splitlines() ]

def filter_ids(ids, bot_type):
	return [ x[0] for x in ids if x[1] == bot_type ]	

def load_json(file_name):
	with open(file_name, 'r') as f:
		o = json.load(f)
	return o

def fix_json(x):
	x['score_over_time_ai'].append(x['final_score_ai'])
	x['score_over_time_human'].append(x['final_score_human'])
	assert(len(x['score_over_time_ai']) == x['ticks_elapsed'] + 2)
	assert(len(x['score_over_time_human'])== x['ticks_elapsed'] + 2)

def load_results(dirname):
	files = os.listdir(dirname)
	js = [ load_json(dirname + "\\" + a) for a in files ]
	for j in js:
		fix_json(j)
	return js

def match_ids(ids, json_objects):
	group_by_3s = [ json_objects[i:i+3] for i in range(0, len(json_objects), 3) ]
	return list(zip(ids, group_by_3s))

user_ids = load_user_ids()
user_ids_a = filter_ids(user_ids, 'A_E')
user_ids_b = filter_ids(user_ids, 'B_M')

json_a = load_results("results_gameA")
json_b = load_results("results_gameB")

assert(len(user_ids_a) == len(set(user_ids_a)))
assert(len(user_ids_b) == len(set(user_ids_b)))

assert(len([ x for x in json_a if not ('Dream' in x['ai_controller']) ]) == 0)
assert(len([ x for x in json_b if not ('MCTS' in x['ai_controller']) ]) == 0)

assert(len(user_ids_a)*3 == len(json_a))
assert(len(user_ids_b)*3 == len(json_b))

data_a = match_ids(user_ids_a, json_a)
data_b = match_ids(user_ids_b, json_b)

# Exclude unwanted data
data_a = [ (id, x) for id, x in data_a if not (id in excluded_from_a) ]
data_b = [ (id, x) for id, x in data_b if not (id in excluded_from_b) ]

def won(x):
	return 1 if x['winner'] == 'human' else 0

def ticks(x):
	return x['ticks_elapsed']

def score(x):
	return x['final_score_human']

def score_diff(x):
	return x['final_score_human'] - x['final_score_ai']

def munge(x, condition):
	a = x[0]
	b = x[1]
	c = x[2]
	return {
		'wins_sum': sum(map(won, x)),
		'time_elapsed_avg': math.floor(sum(map(ticks, x)) / 3),
		'final_score_sum': sum(map(score, x)),
		'final_score_diff_sum': sum(map(score_diff, x)),
		'final_score_diff_avg': math.floor(sum(map(score_diff, x))/3),
		'condition': condition
	}

def to_csv_str(data):
	ks = list(data[0][1].keys())
	top_row = "id, " + ", ".join(ks) + "\n"
	rows = "\n".join([id + ", " + ", ".join([str(d[k]) for k in ks]) for id, d in data])
	return top_row + rows

def write_csv_file(data, file_name):
	ordered_data = []
	data_dict = dict(data)
	for x in user_ids:
		id = x[0]
		if not (id in all_excluded):
			ordered_data.append((id, data_dict[id]))

	csv_str = to_csv_str(ordered_data)

	with open('munged_game_logs.csv', 'w') as f:
		f.write(csv_str)

all_data = (
	[ (id, munge(x, '0')) for id, x in data_a ] +
	[ (id, munge(x, '1')) for id, x in data_b ])

# write_csv_file(all_data, 'munged_game_logs.csv')

def unzip(tups):
	a = []
	b = []
	for x, y in tups:
		a.append(x)
		b.append(y)
	return (a, b)



import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from collections import defaultdict

def median(lst):
	return np.median(np.array(lst))

def plot_data(data, colour):
	xgroups = defaultdict(list)
	points = []
	for d in data:
		attempt = d[1][2]
		human = attempt['score_over_time_human']
		ai = attempt['score_over_time_ai']
		for i in range(0, len(human), 20):
			x = i
			y = human[i] - ai[i]
			xgroups[x].append(y)
			points.append((x, y))

	(points, counts) = unzip(list(Counter(points).items()))
	(x, y) = unzip(points)

	plt.scatter(x, y, s=counts, color=colour)

	plotpoints = [ (x, median(ys) ) for x, ys in xgroups.items() ]
	(px, py) = unzip(plotpoints)
	plt.plot(px, py, "r--", color=colour)
	

	#z = np.polyfit(x, y, 1)
	#p = np.poly1d(z)
	#plt.plot(x,p(x),"r--", color=colour)

plot_data(data_a, 'orange')
plot_data(data_b, 'blue')

plt.xlabel('Game tick')
plt.ylabel('Score difference')
#plt.title("Difference between player and AI scores over time")
plt.grid(True)
#plt.savefig(file_name)

plt.interactive(True)
plt.show()

