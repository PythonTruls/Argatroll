import tkinter as tk

"""This will be the main program to run the game 'argatroll'
"""

class Gameboard:

    def __init__(self,size,array,trolls,list_of_occupied_coordinates):
        self.size = size
        self.board = array
        self.trolls = trolls
        self.occupied_list = list_of_occupied_coordinates
    
    def adding_troll(self,troll_coordinate):
        self.trolls.append(troll_coordinate)
        return troll_coordinate

    def appending_occupied_coordinates(self,new_troll_coordinate):


        occupied_row = new_troll_coordinate[1]
        occupied_column = new_troll_coordinate[0]

        #Horizontal and vertical to trolls coordinates are added to occupied list
        for i in range(1, self.size+1):
            self.occupied_list.append((occupied_column,i))
            self.occupied_list.append((i,occupied_row))

        y = occupied_row
        x = occupied_column
        for _ in range(x):
            y -= 1

        #Diagonal coordinates are added to occupied list
        for current_x in range(0,self.size+1):

            current_y1 = current_x + y
            current_y2 = current_y1 + (x - current_x)*2

            if self.size >= current_y1 > 0:
                self.occupied_list.append((current_x,current_y1))

            if self.size >= current_y2 > 0:
                self.occupied_list.append((current_x,current_y2))
        

    def occupying_coordinates(self):

        for coordinate in self.occupied_list:
            self.board[coordinate] = 0
        
        return self.board
    
    def angry_troll_check(self,troll_position):
    
        if troll_position in self.trolls:
            print("Already troll here!")
            return False
        
        if troll_position in self.occupied_list:
            print("Trolls got angry!")
            return False
        else:
            return True


def coordinate_system(size):
    """Creates an square array of x and y coordinates
    """

    coordinates = []
    
    x = 0

    while x < size:
        x += 1
        for y in range(1,size+1):
            coordinates.append((x,y))

    return coordinates

def coordinate_values(coordinates):
    """Creates a dictionary where the coordinates are keys which are assigned with the values 1
    """
    array = {}

    for coordinate in coordinates:
        array[coordinate] = 1

    return array


def printing_board_in_terminal(current_coordinates,board_layout,size):

    size = int(len(current_coordinates) ** 0.5)

    y_coordinate = size

    print("_"*size*3)

    while y_coordinate > 0:

        for x_coordinate in range(1,size+1):

            if x_coordinate == size:
                board_layout(current_coordinates[(x_coordinate,y_coordinate)],"\n")
            else:
                board_layout(current_coordinates[(x_coordinate,y_coordinate)],"")
        
        y_coordinate -= 1

def board_layout(coordinate_value,ending):
    if coordinate_value:
        print("|_|",end=ending)
    elif not coordinate_value:
        print("|x|",end=ending)
    
    

def main():

    size = 10

    trolls = []
    list_of_occupied_coordinates = []
    array1 = {}
    

    array1 = coordinate_values(coordinate_system(size))
    printing_board_in_terminal(array1, board_layout,size)

    game1 = Gameboard(size,array1,trolls,list_of_occupied_coordinates)

    for _ in range(1,size+1):
        troll_x_coordinate = int(input("X-värde: "))
        troll_y_coordinate = int(input("Y-värde: "))

        troll_position = (troll_x_coordinate,troll_y_coordinate)

        if game1.angry_troll_check(troll_position):
            game1.appending_occupied_coordinates(game1.adding_troll(troll_position))
            game1.occupying_coordinates()
            printing_board_in_terminal(game1.occupying_coordinates(),board_layout,size)

        else:
            continue


if __name__ == "__main__":
    main()