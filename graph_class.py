import pandas as pd
import numpy as np


df = pd.read_csv('routes.csv')
df[' source airport id'] = pd.to_numeric(df[' source airport id'], errors = 'coerce').astype('Int64')
print(df)
n = df[' source airport id'].nunique()
print(df[' source airport id'].min(), df[' source airport id'].max())
print(n)


# Intialize the graph First
class flight_graph:
    def __init__(self):
        self.graph = None
        self.vert_dict = {}
        self.vertcount = 0


# add Verticie to graph. 
    def addVert(self, vert):
        if vert not in self.vert_dict:
            if self.vertcount == 0:
                self.vert_dict = {vert:self.vertcount}
                self.graph = np.zeros((1,1), dtype = int)
                self.vertcount += 1

            else:
                self.vert_dict[vert] = self.vertcount
                zero_col = np.zeros((self.vertcount,1), dtype = int)
                self.graph = np.append(self.graph, zero_col, axis =1)
                self.vertcount += 1
                zero_row = np.zeros((1,self.vertcount), dtype = int )
                self.graph = np.append(self.graph, zero_row, axis = 0)
      


#Adding edge. the verts are the datasets verts. 
    def addEdge(self,u_vert,v_vert,weight):
        if u_vert not in self.vert_dict:
            self.addVert(u_vert)
        if v_vert not in self.vert_dict:
            self.addVert(v_vert)
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
# Return Linked List:
    def linkedList(self):
        linked_list = []

        for row in range(0,len(self.graph)):
            for col in range(0,len(self.graph[row])):
                linked_list += linked_list + [[row, col, self.graph[row,col]]]
        return linked_list
df = pd.DataFrame(np.array([[3,2,1],[2,3,2],[1,3,5]]), columns=['A', 'B', 'C'])

print(df)


x = flight_graph()

x.importGraphData(df, 'A', 'B', 'C')

x.displayGraph()
print("-------")
# x.linkedList()
# print(x.linkedList())


num_vertices = 5
vertices = [f'V{i}' for i in range(1, num_vertices + 1)]
num_edges = 50  # Number of edges in the graph

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