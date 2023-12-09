from tkinter import *
from PIL import ImageTk, Image
import pandas as pd 

#load data
airport_data = pd.read_csv('c:/Users/rocky/iCloudDrive/Desktop/NCF Fall 2023/Algorithms/Group projects/Group project 2/Data/routes_w_capacities_starter_set.csv')


root = Tk()
root.title('Flights') #title of window
root.iconbitmap('C:/Users/rocky/iCloudDrive/Desktop/NCF Fall 2023/Algorithms/Group projects/Group project 2/Final Stuff/Plane.ico') #cute icon
root.geometry('900x600') #size of window

#create lists with unique departing airports and destination airports
departing_airports = airport_data['source_airport_name'].sort_values().unique()
destination_airports = airport_data['destination_airport_name'].sort_values().unique()


#this function will be used with the button. 
def show_airport_ids():
    #get departing airport info
    departing = selected_departing_airport.get()
    dep_filter = airport_data['source_airport_name']  == departing
    dep = airport_data[dep_filter]
    dep_id = dep['source_airport_ID'].unique()
    dep_label = Label(root, text = 'departing airport id; ' + str(dep_id))

    #get destination airport info
    destination = selected_destination_airport.get()
    dest_filter = airport_data['destination_airport_name']==destination
    dest = airport_data[dest_filter]
    dest_id = dest['destination_airport_ID'].unique()
    dest_label = Label(root, text = 'destination airport id; ' + str(dest_id))

    #put labels on screen
    dep_label.grid(row = 3, column = 0)
    dest_label.grid(row = 4, column = 0)



#storing the selected values
selected_departing_airport = StringVar()
selected_destination_airport = StringVar()

#set labels
label1 = Label(root, text = 'Select Departing Airport').grid(row = 0, column = 0)
label2 = Label(root, text = 'Select Destination Airport').grid(row = 0, column = 1)

#define dropdown boxes
selected_departing_airport.set('Orlando') #set default option
dropdownboxDeparting = OptionMenu(root, selected_departing_airport,*departing_airports) #must have the star to show the outside variable
dropdownboxDeparting.grid(row = 1, column = 0, padx = 25)

selected_destination_airport.set('San Diego') #set default option
dropdownboxDestination = OptionMenu(root, selected_destination_airport,*destination_airports) #must have the star to show the outside variable
dropdownboxDestination.grid(row = 1, column = 1, padx = 25)

#define enter button
enter_button = Button(root, text = 'click to enter selection', command = show_airport_ids )
enter_button.grid(row = 2, column = 0, padx = 50)



root.mainloop()
