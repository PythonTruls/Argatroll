def array():
    size = 4
    number_of_coordinates= size **2
    array_of_coordinates = []
    for _ in range(number_of_coordinates):
        array_of_coordinates.append(1)

    return array_of_coordinates

#Create an array using a dictionary of i columns and rows j
def dictionary_system():
    
    size = 4
    number_of_rows = []
    number_of_columns = []
    array = {}
    i = 1
    j = 0

    for _ in range (size):
        number_of_rows.append(i)
        number_of_columns.append(i)
        i += 1

    for _ in range(size):
        array[number_of_columns[j]] = number_of_rows
        j += 1

    return array

def dictionary_grid():
    coordinates = dictionary_system()

    root = tk.Tk()
    root.title('Argatroll')

    myLabel2 = tk.Label(root, text='coordinate system')
    myLabel2.grid(column=0,row=0)

    for column in coordinates.keys():
        for row in coordinates[column]:
            myLabel1 = tk.Label(root, text='1')
            myLabel1.grid(column=column,row=row)

    root.mainloop()  