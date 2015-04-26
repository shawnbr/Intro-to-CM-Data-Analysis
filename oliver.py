from datetime import datetime
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

#Plot
def plot(X,Y, title, xlabel, ylabel):
   #plt.figure()
   plt.plot(X, Y, 'ro')
   plt.title(title)
   plt.xlabel(xlabel)
   plt.ylabel(ylabel)
   plt.show()

#Gets the number of days between 2 dates
def cal_days_diff(a,b):

    A = a.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    B = b.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    return (A - B).days

#Get number of friends a node has
def get_number_connections(filename, nodes):
	with open(filename, "rb") as input_data:
		data = [line.strip().split('\t') for line in input_data]
		for line in data:
			node = int(line[0])
			if node not in nodes:
				nodes[node] = {}
				nodes[node]['connections'] = 1
			else:
				nodes[node]['connections'] += 1
	return None

#Get number of days a user has been in the system
def get_number_days(filename, nodes):
	temp_nodes = {}
	with open(filename, "rb") as input_data:
		data = [line.strip().split('\t') for line in input_data]
		for line in data:
			node = int(line[0])
			if node not in temp_nodes:
				temp_nodes[node] = {}
				temp_nodes[node]['last'] = datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ')
				temp_nodes[node]['first'] = datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ')
				temp_nodes[node]['count'] = 1
				temp_nodes[node]['active_days'] = 1
			else:
				prev = temp_nodes[node]['first']
				temp_nodes[node]['first'] = datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ')
				if prev.date() != temp_nodes[node]['first'].date():
					temp_nodes[node]['active_days'] += 1
				temp_nodes[node]['count'] += 1

	for node_val in temp_nodes:
		num_days = cal_days_diff(temp_nodes[node_val]['last'],temp_nodes[node_val]['first'])
		nodes[node_val]['number_of_days'] = num_days + 1
		nodes[node_val]['number_of_checkins'] = temp_nodes[node_val]['count']
		nodes[node_val]['number_of_active_days'] = temp_nodes[node_val]['active_days']

	return None

if __name__ == "__main__":
	start_time = time.time()

	nodes = {}
	get_number_connections('data/edges.txt', nodes)
	get_number_days('data/checkins.txt', nodes)
	
	connections = {}
	nodes_without_checkin = 0

	for node in nodes:

		if 'number_of_checkins' in nodes[node]:
			nodes[node]['checkins_day'] = float(nodes[node]['number_of_checkins'])/nodes[node]['number_of_days']
			nodes[node]['checkins_active_day'] = float(nodes[node]['number_of_checkins'])/nodes[node]['number_of_active_days']

			if nodes[node]['connections'] not in connections:
				connections[nodes[node]['connections']] = {}
				connections[nodes[node]['connections']]['checkins_day'] = nodes[node]['checkins_day']
				connections[nodes[node]['connections']]['checkins_active_day'] = nodes[node]['checkins_active_day']
				connections[nodes[node]['connections']]['total'] = 1
			else:
				connections[nodes[node]['connections']]['total'] += 1
				connections[nodes[node]['connections']]['checkins_day'] += nodes[node]['checkins_day']			
				connections[nodes[node]['connections']]['checkins_active_day'] += nodes[node]['checkins_active_day']
		else:
			nodes_without_checkin += 1


	connections_list = []
	for connection in connections:
		connections[connection]['checkins_day'] = connections[connection]['checkins_day']/connections[connection]['total']
		connections[connection]['checkins_active_day'] = connections[connection]['checkins_active_day']/connections[connection]['total']
		connections_list.append(connection)

	#connections_list = connections_list.sort()
	x = []
	y = []
	y2 = []
	bucket_size = 10
	total_checkins_day = 0
	totals_val = 0
	for connection in connections_list:
		if connection < bucket_size:
			total_checkins_day += connections[connection]['checkins_day']
			totals_val += 1
		else:
			if totals_val != 0:
				x.append(bucket_size)
				y.append(float(total_checkins_day)/totals_val)

			bucket_size += bucket_size
			totals_val = 1
			total_checkins_day = connections[connection]['checkins_day']

	sns.set_palette("deep", desat=.6)
	sns.set_context(rc={"figure.figsize": (8, 4)})
	plt.plot(x,y)
	plt.show()


	print("--- %s seconds ---\n" % (time.time() - start_time))

# for node in nodes:
# 	if nodes[node]['connections'] > 10:
# 		print "Node {}: {}".format(node, nodes[node]['connections'])


