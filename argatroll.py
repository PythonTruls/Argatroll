import tkinter as tk

"""This will be the main program to run the game 'argatroll'
"""

class Gameboard:
    """Class of the gameboard in which the trolls can be added
    
    """
    def __init__(self,size,coordinates, array,trolls,list_of_occupied_coordinates):
        """A gameboard has size in whch the square array can be made,
        trolls is a list of all the placed trolls,
        the occupied list is a list of coordinates on which no trolls can be placed
        """
        self.size = size
        self.coordinates = coordinates
        self.board = array
        self.trolls = trolls
        self.occupied_list = list_of_occupied_coordinates
    
    def adding_troll(self,troll_coordinate):
        """appending a new troll to the trolls list¨
        """
        self.trolls.append(troll_coordinate)
        return troll_coordinate

    def changing_coordinates(self,new_troll_coordinate):
        """appending new coordinates to the occupied list,
        this is done by using the troll coordinate,
        all coordinates with the same y-value are occupied,
        all coordinates with the same x-value are occupied
        """

        changing_coordinates =  []

        occupied_row = new_troll_coordinate[1]
        occupied_column = new_troll_coordinate[0]

        #Horizontal and vertical to trolls coordinates are added to occupied list
        for i in range(1, self.size+1):
            changing_coordinates.append((occupied_column,i))
            changing_coordinates.append((i,occupied_row))

        y = occupied_row
        x = occupied_column
        for _ in range(x):
            y -= 1

        #Diagonal coordinates are added to occupied list
        for current_x in range(0,self.size+1):

            current_y1 = current_x + y
            current_y2 = current_y1 + (x - current_x)*2

            if self.size >= current_y1 > 0:
                changing_coordinates.append((current_x,current_y1))

            if self.size >= current_y2 > 0:
                changing_coordinates.append((current_x,current_y2))

        return changing_coordinates
        
    def occupying_coordinates(self):
        """All values connected to occupied coordinates 
        in the array dictionary are turned to 0s
        """
        for coordinate in self.occupied_list:
            self.board[coordinate] = 0 
        
        return self.board
    
    def changing_occupied_list(self, changing_list, type_of_change):
        
        if type_of_change == "occupy":
            for coordinate in changing_list:
                self.occupied_list.append(coordinate)
        elif type_of_change == "undo":
            for coordinate in changing_list:
                self.occupied_list.remove(coordinate)


    def angry_troll_check(self,troll_position):
        """Check if the coordinate is already occupied
        """
        if troll_position in self.trolls:
            print("Already troll here!")
            return False
        
        if troll_position in self.occupied_list:
            print("Trolls got angry!")
            return False
        else:
            return True
        
    def reseting_coordinate_values(self):
        """Creates a dictionary where the coordinates are keys which are assigned with the values 1
        """

        for coordinate in self.coordinates:
            self.board[coordinate] = 1



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
    """Creates a square gameboard in the terminal with the help of the 'board_layout()
    """
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
    """prints the visual for each coordinate, if the coordinate is occupied it prints a x aswell
    """
    if coordinate_value:
        print("|_|",end=ending)
    elif not coordinate_value:
        print("|x|",end=ending)
    
    

def main():
    """Main function of the game
    """
    size = 10

    trolls = []
    list_of_occupied_coordinates = []
    array = {}
    coordinates = []

    coordinates = coordinate_system(size)
    printing_board_in_terminal(array, board_layout,size)

    game1 = Gameboard(size,coordinates,array,trolls,list_of_occupied_coordinates)

    game1.reseting_coordinate_values()
    printing_board_in_terminal(game1.occupying_coordinates(), board_layout,size)

    for _ in range(1,size+1):

        game1.reseting_coordinate_values()

        troll_x_coordinate = int(input("X-värde: "))
        troll_y_coordinate = int(input("Y-värde: "))
        move = input("occupy eller undo? ")

        troll_position = (troll_x_coordinate,troll_y_coordinate)
        if move == "occupy":

            if game1.angry_troll_check(troll_position):

                new_coordinates = game1.changing_coordinates(game1.adding_troll(troll_position))
                game1.changing_occupied_list(new_coordinates,move)
                printing_board_in_terminal(game1.occupying_coordinates(),board_layout,size)

            else:
                continue
        elif move == "undo":

            new_coordinates = game1.changing_coordinates(game1.adding_troll(troll_position))
            game1.changing_occupied_list(new_coordinates,move)
            printing_board_in_terminal(game1.occupying_coordinates(),board_layout,size)


if __name__ == "__main__":
    main()