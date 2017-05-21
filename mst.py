import ast, os
import matplotlib.pyplot as plt

import networkx as nx
with open("input.txt", 'r') as f:
    Tnodes = ast.literal_eval(f.readline())
    graph = ast.literal_eval(f.readline())
    weight = ast.literal_eval(f.readline())
    #graph = map(list, graph)
    #print weight
    f.close()
cycle_count = 0    
cycles = []

file1 = open("cycle.txt",'w')
def main():
    global cycle_count
    global graph
    global graph1
    global cycles
    for edge in graph:
        for node in edge:
            findNewCycles([node])
    for cy in cycles:
        path = [str(node) for node in cy]
        s = ",".join(path)
        #print(s)
        path1 = map(int, path)
        c = zip(path1,path1[1:])
        c = map(list, c)
        c.append(path1[0::len(path1)-1])
        for i in range(len(c)):
            if c[i][0] > c[i][1]:
                c[i].reverse()
            file1.write(str(c[i]))
            if i != len(c)-1:
            	file1.write(",")
	cycle_count = cycle_count + 1
        file1.write("\n")

def findNewCycles(path):
    start_node = path[0]
    next_node= None
    sub = []

    #visit each edge and each node of each edge
    for edge in graph:
        node1, node2 = edge

        if start_node in edge:
                if node1 == start_node:
                    next_node = node2
                else:
                    next_node = node1
        if not visited(next_node, path):
                # neighbor node not on path yet
                sub = [next_node]
                sub.extend(path)
                # explore extended path
                findNewCycles(sub);
        elif len(path) > 2  and next_node == path[-1]:
                # cycle found
                p = rotate_to_smallest(path);
                inv = invert(p)
                if isNew(p) and isNew(inv):
                    cycles.append(p)

def invert(path):
    return rotate_to_smallest(path[::-1])

#  rotate cycle path such that it begins with the smallest node
def rotate_to_smallest(path):
    n = path.index(min(path))
    return path[n:]+path[:n]

def isNew(path):
    return not path in cycles

def visited(node, path):
    return node in path

main()
file1.close()
file3 = open("constraint.opb", 'w')
file3.write("min: ")
for k in range(len(graph)):
       file3.write(str(weight[k])+"*x"+str(k))
       if k!= len(graph)-1:
           file3.write(" +")
file3.write(";"+"\n")
for k in range(len(graph)):
       file3.write("1*x"+str(k))
       if k!= len(graph)-1:
           file3.write(" +")
file3.write(" = "+ str(Tnodes-1) + ";" + "\n")      
print "file closed"
with open("cycle.txt", 'r') as file2:
    for i in range(cycle_count):

    	constraint = ast.literal_eval(file2.readline())
    #constraint = map(list, constraint)
    	for j in range(len(constraint)):
    		edge_no = graph.index(constraint[j])
    		file3.write("1*x"+str(edge_no))
    		if j != len(constraint)-1:
		    file3.write(" +")
        file3.write(" < "+ str(len(constraint))+";"+"\n")
    file2.close()
    file3.close()
     
exe="./minisat+ constraint.opb | tee output.txt"
os.system(exe)
f1 = open("output1.txt",'w')
with open("output.txt", 'r') as f:
        for line in f:
            if 'v' in line:
                #print line;
                f1.write(line)
f1.close()
f1 = open("output1.txt",'r')               

lineList = f1.readlines()
f1.close()
#print "The last line is:"
#print lineList[-1]
f1 = open("output1.txt",'w')
f1.write(lineList[-1])
f1.close()
sum1 = 0
mstnodes = []
with open("output1.txt", 'r') as f:
    nodes = f.readline()
    f.close()
    nodes = map(str, nodes.split())
    nodes = nodes[1:]
    #print nodes #['x0', 'x1', '-x2', '-x3', 'x4', '-x5']
    f = open("output2.txt",'w')
    f.write("The edges in the minimum spanning tree and their weight: \n")
    for i in range(len(nodes)):
    	if nodes[i][0] != '-':
    		mstnodes.append(graph[nodes.index(nodes[i])])
    		#mstnodes = mstnodes + graph[nodes.index(nodes[i])]
    		#mstnodes.append(weight[nodes.index(nodes[i])])
    		print graph[nodes.index(nodes[i])],":", weight[nodes.index(nodes[i])]
    		f.write(str(graph[nodes.index(nodes[i])])+" : "+str(weight[nodes.index(nodes[i])])+"\n")
    		sum1 = sum1 + weight[nodes.index(nodes[i])]
    print "Optimal Solution: ", sum1
    f.write("Optimal Solution: "+str(sum1))
    f.close()
    #print "mstnodes: ", mstnodes
#mstnodes = [mstnodes[n:n+3] for n in range(0, len(mstnodes), 3)]
#print mstnodes
nod = []
for i in range(Tnodes):
	nod.append(i+1)
#print nod 

G = nx.Graph()

G.add_nodes_from(nod)
G.add_edges_from(mstnodes)

nx.draw(G,with_labels=True)
#plt.savefig("graph.png")
plt.show()

