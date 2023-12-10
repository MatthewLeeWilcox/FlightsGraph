from tkinter import *
from PIL import ImageTk, Image
import pandas as pd 

#load data
df_routes = pd.read_csv('c:/Users/rocky/iCloudDrive/Desktop/NCF Fall 2023/Algorithms/Group projects/Group project 2/Data/routes_w_capacities_starter_set.csv')

root = Tk()
root.title('Flights') #title of window
root.iconbitmap('C:/Users/rocky/iCloudDrive/Desktop/NCF Fall 2023/Algorithms/Group projects/Group project 2/Final Stuff/Plane.ico') #cute icon
root.geometry('900x600') #size of window

class flight_graph:
    
    def __init__(self,main_root):
        #create lists with unique departing airports and destination airports
        self.departing_airports = df_routes['source_airport_name'].sort_values().unique()
        self.destination_airports = df_routes['destination_airport_name'].sort_values().unique()

        #storing the selected values
        self.selected_departing_airport = StringVar()
        self.selected_destination_airport = StringVar()

        #set labels
        self.label1 = Label(main_root, text = 'Select Departing Airport').grid(row = 0, column = 0)
        self.label2 = Label(main_root, text = 'Select Destination Airport').grid(row = 0, column = 1)

        #define dropdown boxes
        self.selected_departing_airport.set('Orlando') #set default option
        self.dropdownboxDeparting = OptionMenu(main_root, self.selected_departing_airport,*self.departing_airports) #must have the star to show the outside variable
        self.dropdownboxDeparting.grid(row = 1, column = 0, padx = 25)

        self.selected_destination_airport.set('San Diego') #set default option
        self.dropdownboxDestination = OptionMenu(main_root, self.selected_destination_airport,*self.destination_airports) #must have the star to show the outside variable
        self.dropdownboxDestination.grid(row = 1, column = 1, padx = 25)

        #define enter button
        self.enter_button = Button(main_root, text = 'click to enter selection', command = self.find_airport_ids )
        self.enter_button.grid(row = 2, column = 0, padx = 50)

        #create frames to put output
        self.output_frame_departing = Frame(main_root)
        self.output_frame_departing.grid(row = 3, column = 0)

        self.output_frame_destination = Frame(main_root)
        self.output_frame_destination.grid(row = 4, column = 0)


    def find_airport_ids(self):
        #get departing airport info
        self.departing = self.selected_departing_airport.get()
        self.dep_filter = df_routes['source_airport_name']  == self.departing
        self.dep = df_routes[self.dep_filter]
        self.dep_id = self.dep['source_airport_ID'].unique()
        self.dep_label = Label(self.output_frame_departing, text = 'departing airport id; ' + str(self.dep_id))

        #get destination airport info
        self.destination = self.selected_destination_airport.get()
        self.dest_filter =df_routes['destination_airport_name']==self.destination
        self.dest = df_routes[self.dest_filter]
        self.dest_id = self.dest['destination_airport_ID'].unique()
        self.dest_label = Label(self.output_frame_destination, text = 'destination airport id; ' + str(self.dest_id))

        #put labels on screen
        self.dep_label.grid(row = 3, column = 0)
        self.dest_label.grid(row = 4, column = 0)


trial = flight_graph(root)

root.mainloop()
