import tkinter as tk

"""This will be the main program behind the game 'argatroll'
"""

class Gameboard:
    """Class which creates an object that has all methods needed for a game of arga troll to be played
    """

    def __init__(self,size,coordinates, array):
        """A gameboard has size in whch the square array can be made,
        trolls is a list of all the placed trolls,
        the occupied list is a list of coordinates on which no trolls can be placed
        """
        self.size = size
        self.coordinates = coordinates
        self.board = array
        self.trolls = []
        self.occupied_list = []
    
    def adding_troll(self,troll_coordinate):
        """appending a new troll to the trolls list¨
        """
        self.trolls.append(troll_coordinate)
        return troll_coordinate

    def removing_troll(self, troll_coordinate):
        """removing an existing troll from the trolls list
        """
        self.trolls.remove(troll_coordinate)
        return troll_coordinate

    def changing_coordinates(self,new_troll_coordinate):
        """Creating a tuple list of coordinates affected by a specific trolls position,
        by using the troll coordinate:
        all coordinates with the same y-value are occupied,
        all coordinates with the same x-value are occupied,
        all coordinates in the diagonals from specific position
        """

        changing_coordinates =  []

        changing_row = new_troll_coordinate[1]
        changing_column = new_troll_coordinate[0]

        #Horizontal and vertical to trolls coordinates are added to occupied list
        for i in range(1, self.size+1):
            changing_coordinates.append((changing_column,i)) #Horizontal
            changing_coordinates.append((i,changing_row)) #Vertical


        x = changing_column
        y = changing_row - x

        #Diagonal coordinates are added to occupied list
        for current_x in range(0,self.size+1):

            current_y1 = current_x + y
            current_y2 = current_y1 + (x - current_x)*2

            if self.size >= current_y1 > 0:
                changing_coordinates.append((current_x,current_y1))

            if self.size >= current_y2 > 0:
                changing_coordinates.append((current_x,current_y2))


        #ignores doubles when appending to the tuple list which is returned
        changing_tuple = []
        for coordinate in changing_coordinates:
            if coordinate in changing_tuple:
                continue
            else:
                changing_tuple.append(coordinate)

        return changing_tuple
    

        
    def occupying_coordinates(self):
        """All values connected to occupied key-coordinates 
        in the array dictionary are turned to 0s
        """
        for coordinate in self.occupied_list:
            self.board[coordinate] = 0 
        
        return self.board
    
    def changing_occupied_list(self, changing_list, type_of_change):
        """Chaning the coordinates, in the occupied_list,
        defined by the changing_list from function 'changing_coordinates'
        either by removing them (undo)
        or adding them (occupy)
        """
        
        if type_of_change == "occupy":
            for coordinate in changing_list:
                self.occupied_list.append(coordinate)
        elif type_of_change == "undo":
            for coordinate in changing_list:
                self.occupied_list.remove(coordinate)


    def angry_troll_check(self,troll_position):
        """Check if the coordinate is already in the occupied_list
        """
        if troll_position in self.occupied_list:
            return False
        else:
            return True
        
    def limiting_to_one_row(self, troll_position):
        """Checks if the requested placement is on the right row
        in which actions can be made
        """

        requested_row = troll_position[0]

        match len(self.trolls): 
            case 0: #Special conditions if the board is empty
                if requested_row == 1:
                    return True
                else:
                    return False
   
            case _:
                current_row = self.trolls[-1][0] #the row in which last troll was placed
                next_row = current_row +1 #the row in which next troll can be placed
                if requested_row == next_row or requested_row == current_row:
                    return True
                else:
                    return False

        
    

    def reseting_coordinate_values(self):
        """Cangng all values to the keys to 1
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
        for y in range(1,size+1): #iterates through all coordinates within the current x-row
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
    size = int(len(current_coordinates) ** 0.5) #the number of coordinates are the square of the side length

    y_coordinate = 1

    print("_"*size*3)

    while y_coordinate <= size:

        for x_coordinate in range(1,size+1):

            if x_coordinate == size:
                board_layout(current_coordinates[(x_coordinate,y_coordinate)],"\n")
            else:
                board_layout(current_coordinates[(x_coordinate,y_coordinate)],"")
        
        y_coordinate += 1

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
    array = {}
    coordinates = []

    coordinates = coordinate_system(size)
    printing_board_in_terminal(array, board_layout,size)

    game1 = Gameboard(size,coordinates,array)

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

            new_coordinates = game1.changing_coordinates(game1.removing_troll(troll_position))
            game1.changing_occupied_list(new_coordinates,move)
            printing_board_in_terminal(game1.occupying_coordinates(),board_layout,size)


if __name__ == "__main__":
    main()