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
departing_airports = airport_data['source_airport_name'].unique()
destination_airports = airport_data['destination_airport_name'].unique()




#storing the selected values
selected_departing_airport = StringVar()
selected_destination_airport = StringVar()

#set labels
label1 = Label(root, text = 'Select Departing Airport').grid(row = 0, column = 0)
label2 = Label(root, text = 'Select Destination Airport').grid(row = 0, column = 1)

#define dropdown boxes
dropdownboxDeparting = OptionMenu(root, selected_departing_airport,*departing_airports) #must have the star to show the outside variable
dropdownboxDeparting.grid(row = 1, column = 0)

dropdownboxDestination = OptionMenu(root, selected_destination_airport,*destination_airports) #must have the star to show the outside variable
dropdownboxDestination.grid(row = 1, column = 1)


root.mainloop()
