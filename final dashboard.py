from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import csv


root = Tk()
root.title('Flights') #title of window
root.iconbitmap('C:/Users/rocky/iCloudDrive/Desktop/NCF Fall 2023/Algorithms/Group projects/Group project 2/Final Stuff/Plane.ico') #cute icon
root.geometry('900x600') #size of window
# -------------------------------------------------------------------------------------------------------------------------------------

# Graph Class

# -------------------------------------------------------------------------------------------------------------------------------------

# Note: the graph must me intialized such as x = flight_graph()
df_routes = pd.read_csv('c:/Users/rocky/iCloudDrive/Desktop/NCF Fall 2023/Algorithms/Group projects/Group project 2/Data/FINAL_ALL_DATA_DEC_11.csv')


class flight_graph:
    def __init__(self,main_root):
        #create lists with unique departing airports and destination airports and unique airlines
        self.airline = df_routes['airline_name'].sort_values().unique()
        self.departing_airports = df_routes['source_airport_name'].sort_values().unique()
        self.destination_airports = df_routes['destination_airport_name'].sort_values().unique()

        #storing the selected values
        self.selected_departing_airport = StringVar()
        self.selected_destination_airport = StringVar()
        self.selected_airline = StringVar()

        #set labels
        self.label1 = Label(main_root, text = 'Select Departing Airport').grid(row = 0, column = 0)
        self.label2 = Label(main_root, text = 'Select Destination Airport').grid(row = 0, column = 1)
        self.label3 = Label(main_root, text = 'Select an Airline').grid(row = 0, column = 3)

        #define dropdown boxes
        self.selected_departing_airport.set('Cincinnati') #set default option
        self.dropdownboxDeparting = OptionMenu(main_root, self.selected_departing_airport,*self.departing_airports) #must have the star to show the outside variable
        self.dropdownboxDeparting.grid(row = 1, column = 0, padx = 25)

        self.selected_destination_airport.set('Tampa') #set default option
        self.dropdownboxDestination = OptionMenu(main_root, self.selected_destination_airport,*self.destination_airports) #must have the star to show the outside variable
        self.dropdownboxDestination.grid(row = 1, column = 1, padx = 25)

        self.selected_airline.set('American Airlines')
        self.dropdownboxAirline = OptionMenu(main_root, self.selected_airline, *self.airline)
        self.dropdownboxAirline.grid(row = 1, column = 3, padx = 25)

        #define enter button
        self.enter_button = Button(main_root, text = 'click to enter selection', command = self.find_airport_ids)
        self.enter_button.grid(row = 2, column = 0, padx = 50)

        #create frames to put output

        self.output_frame_max_capacity = Frame(main_root)
        self.output_frame_max_capacity.grid(row = 3, column = 0)


        self.graph = None
        self.vert_dict = {}
        self.vertcount = 0

    #function to be used with button
    def find_airport_ids(self):
        #call addEdge function to import data
        self.airline_info = self.selected_airline.get()
        airlinefilter = df_routes['airline_name'] == self.airline_info
        subset_airline = df_routes[airlinefilter]
        self.importGraphData(subset_airline, 'source_airport_ID', 'destination_airport_ID', 'capacity')

        #get departing airport info
        self.departing = self.selected_departing_airport.get()
        self.dep_filter = df_routes['source_airport_name']  == self.departing
        self.dep = df_routes[self.dep_filter]
        self.dep_id = int(self.dep['source_airport_ID'].iloc[0])
       

        #get destination airport info
        self.destination = self.selected_destination_airport.get()
        self.dest_filter =df_routes['destination_airport_name']==self.destination
        self.dest = df_routes[self.dest_filter]
        self.dest_id = int(self.dest['destination_airport_ID'].iloc[0])
        

        self.find_max(self.dep_id,self.dest_id)

        #put labels on screen
        


# add Verticie to graph. 
    def addVert(self, vert):
        # Check to see if it is the first Verticie
        if vert not in self.vert_dict:
            if self.vertcount == 0:
                self.vert_dict = {vert:self.vertcount}
                self.graph = np.zeros((1,1), dtype = int)
                self.vertcount += 1
            # Add Verticie to the dictionary and make acompyning row and column in adjacency matrix
            else:
                self.vert_dict[vert] = self.vertcount
                zero_col = np.zeros((self.vertcount,1), dtype = int)
                self.graph = np.append(self.graph, zero_col, axis =1)
                self.vertcount += 1
                zero_row = np.zeros((1,self.vertcount), dtype = int )
                self.graph = np.append(self.graph, zero_row, axis = 0)
      


#A dding edge. the verts are the datasets verts. 
    def addEdge(self,u_vert,v_vert,weight):
        if u_vert not in self.vert_dict:
            self.addVert(u_vert)
        if v_vert not in self.vert_dict:
            self.addVert(v_vert)
        # Sums the weights if their are multiple edges between the same tw verticies
        self.graph[self.vert_dict[u_vert], self.vert_dict[v_vert]] = self.graph[self.vert_dict[u_vert], self.vert_dict[v_vert]] + weight


# Adding data to the graph based upon a pandas dataframe uCol, vCol, weightCol should be the name of the column in the df
    def importGraphData(self, df, uCol, vCol, weightCol):
        for index,row in df.iterrows():
            self.addEdge(row[uCol], row[vCol], row[weightCol])

# //////////////////////////////////////////////////////
# Methods to display Graph
# ------------------------------------------------------
# Displays the graph as a matrix
    def displayGraph(self):
        print(self.graph)


# Adjaceny List
    def adjacency_list(self):
        adjac_list = []
        for row in self.graph:
            row_list = []
            col_count = 0
            for col in row:
                if col > 0:
                    row_list += [col_count]
                col_count += 1
            adjac_list += [row_list]
        return adjac_list
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# ------------------------------------------------------
#////////////////////////////////////////////////////////
# Finding the Max Algorithim
    def initialize_max(self, startVert):
        import math
        verts_current_capacity = list(np.zeros(len(self.graph), int))
        verts_current_capacity[self.vert_dict[startVert]] = math.inf
        return verts_current_capacity
        
    def find_max(self, input_startVert, input_endVert, layover = True):
        import math
        startVert = self.vert_dict[input_startVert]
        endVert = self.vert_dict[input_endVert]
        vert_capacity = self.initialize_max(input_startVert)
        adj_list = self.adjacency_list()
        first_shell = adj_list[startVert]
        for v_vert in first_shell:
            vert_capacity[v_vert] += self.graph[startVert,v_vert]
            if layover == False:
                max_people = vert_capacity[endVert]
                pass
            else:
                if endVert in adj_list[v_vert]:

                    if vert_capacity[v_vert] >=  self.graph[v_vert,endVert]:
                        vert_capacity[endVert] += self.graph[v_vert,endVert]
                    else:
                        vert_capacity[endVert] += vert_capacity[v_vert]
                     
        
        max_people = vert_capacity[endVert]



        self.max_label = Label(self.output_frame_max_capacity, text = 'max number of people ' + str(max_people))
        self.max_label.grid(row = 3, column = 0)
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

x = flight_graph(root)


root.mainloop()