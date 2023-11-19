import pandas as pd
import numpy as np


# df = pd.read_csv('routes.csv')
# df[' source airport id'] = pd.to_numeric(df[' source airport id'], errors = 'coerce').astype('Int64')
# print(df)
# n = df[' source airport id'].nunique()
# print(df[' source airport id'].min(), df[' source airport id'].max())
# print(n)


# Intialize the graph First
class flight_graph:
    def __init__(self):
        self.graph = None
        self.vert_dict = {}
        self.vertcount = 0


# add Verticie to graph. 
    def addVert(self, vert):
        print(self.vert_dict)

        if vert not in self.vert_dict:
            if self.vertcount == 0:
                self.vert_dict = {vert:self.vertcount}
                self.graph = np.zeros((1,1), dtype = int)
                self.vertcount += 1
                print("error")
                print(self.vert_dict)

            else:
                self.vert_dict[vert] = self.vertcount
                zero_col = np.zeros((self.vertcount,1), dtype = int)
                self.graph = np.append(self.graph, zero_col, axis =1)
                self.vertcount += 1
                zero_row = np.zeros((1,self.vertcount), dtype = int )
                self.graph = np.append(self.graph, zero_row, axis = 0)
      


#Adding edge. the verts are the datasets verts. 
    def addEdge(self,u_vert,v_vert,weight):
        print(self.vert_dict)

        if u_vert not in self.vert_dict:
            print("no_u")
            self.addVert(u_vert)
        if v_vert not in self.vert_dict:
            self.addVert(v_vert)
            print("no_v")
        self.graph[self.vert_dict[u_vert], self.vert_dict[v_vert]] = self.graph[self.vert_dict[u_vert], self.vert_dict[v_vert]] + weight

# Adding data to the graph based upon a pandas dataframe uCol, vCol, weightCol should be the name of the column in the df
    def importGraphData(self, df, uCol, vCol, weightCol):
        for index,row in df.iterrows():
            self.addEdge(row[uCol], row[vCol], row[weightCol])


# Displays the graph as a matrix
    def displayGraph(self):
        print(self.graph)
# Return Adjacency Matrix
    def adjacencyMatrix(self):
        return self.graph

# Manual Imports for Arrange List to work
    def manual_inport_vert_dict(self, input_vert_dict):
        self.vert_dict = input_vert_dict
    
    def manual_import_graph(self, input_graph):
        self.graph = input_graph

    def manual_retrieve_dict(self):
        return self.vert_dict
    
# Return Linked List:
    def linkedList(self):
        linked_list = []
        for row in range(0,len(self.graph)):
            for col in range(0,len(self.graph[row])):
                if self.graph[row,col] >0:
                    linked_list += [[row, col, self.graph[row,col]]]
        return np.array(linked_list)

# Limit to a number of layovers produces a new graph
# Save as a ne variable to retain original graph
### Error Incountered. Queing would go through and add every edge and their would be double outputing the wrong graph.
### Realized error was in the arrangedlist as it was including 0 weight which would cause every vert to be queue even if their graph doesnt have a weight
### Fixing list - error in addEdge - making a new dictionary
### This was due to the edge was imputing the value not the key of the edge. 
### Need to put the key value in but that is going to increase runtime significantly.
    def limitLayovers(self, startAirport, maxLayover = 1):
        start_vert = self.vert_dict[startAirport]
        edge_list = self.linkedList()
        layoverGraph = flight_graph()
        layoverGraph.manual_inport_vert_dict(self.vert_dict) 
        layoverGraph.manual_import_graph(np.zeros((len(self.vert_dict.keys()),len(self.vert_dict.keys())), dtype = int))
        layoverGraph.displayGraph()
        print(layoverGraph.manual_retrieve_dict())
        check_queue = [start_vert]
        shell_count = 0
        # Import Key and val into a list to decrease the runtime and retrive the key that the edge is assocaited. to. 
        key_list = list(layoverGraph.manual_retrieve_dict().keys())
        val_list = list(layoverGraph.manual_retrieve_dict().values())
        print("key",key_list)
        print("val",val_list)

        while shell_count <= maxLayover:   
            queue_pulled = check_queue
            # Clear Queue
            check_queue =[] 
            for vert in queue_pulled:
                for edge in edge_list:
                    if edge[0] == vert:
                        print(edge)
                        layoverGraph.manual_retrieve_dict
                        layoverGraph.addEdge(key_list[val_list.index(edge[0])], key_list[val_list.index(edge[1])], edge[2])
                        check_queue += [edge[1]]
            print("*")
            print(layoverGraph.displayGraph())
            print("*")
            shell_count += 1
            # print(check_queue)
            # print('-'*20)
        return layoverGraph




df = pd.DataFrame(np.array([[3,2,1],[2,3,2],[1,3,5]]), columns=['A', 'B', 'C'])

print(df)


x = flight_graph()

x.importGraphData(df, 'A', 'B', 'C')

x.displayGraph()
print("-------")
x2 = x.limitLayovers(3,1)
print("-------")
print("2")
print(x.linkedList())
print("-------")
x2.displayGraph()
print("-------")
print(x2.manual_retrieve_dict())
# x.linkedList()
# print(x.linkedList())


num_vertices = 50
vertices = [f'V{i}' for i in range(1, num_vertices + 1)]
num_edges = 25  # Number of edges in the graph

# Creating random edges and their weights
np.random.seed(42)
edges = []
weights = np.random.randint(1, 20, size=num_edges)
for _ in range(num_edges):
    edge = np.random.choice(vertices, size=2, replace=False)
    edge_weight = np.random.choice(weights)
    edges.append([edge[0], edge[1], edge_weight])

# Creating the dataframe
df = pd.DataFrame(edges, columns=['First Vertice', 'Second Vertice', 'Weight'])
print(df)

y = flight_graph()
y.importGraphData(df, "First Vertice", "Second Vertice" , "Weight")
y.displayGraph()

z = y.limitLayovers("V50",0)
y.displayGraph()
z.displayGraph()
print(z.linkedList())



# New error, if you have 3 layovers, it just adds the throughpukt of the same location, I dont believe that is what we want. Wont Impact us on this project as we are only looking at max 1 layover but is something to consieder
