"""This program performs an algoritm to solve the game 'arga troll'
"""

import argatroll
import time



class Algoritm:
    """This program is used to display in the terminal an not used in the final project"""

    def __init__(self,game):
        self.game = game
        self.current_path = []
        self.complete_paths = []


    def returning_position(self,current_row,start_column):

        row = current_row


        for column in range(start_column,self.game.size+1):

            position = (row,column)

            if self.game.angry_troll_check(position):
                return position

        return False
    
    def solver(self,start_row=1,start_column=1):

        column = start_column
        current_row = start_row

        for row in range(current_row,self.game.size+1):

            position = self.returning_position(row,column)

            if position != False:
                new_coordinates = self.game.changing_coordinates(self.game.adding_troll(position))
                self.game.changing_occupied_list(new_coordinates,"occupy")
                self.current_path.append(position)
                column = 1


                if len(self.current_path) == self.game.size:
                    print(self.current_path)
                    quit()
                else:
                    print(self.current_path)
            
            else:

                removing_coordinate = self.game.trolls.pop()
                self.current_path.remove(removing_coordinate)
                new_coordinates = self.game.changing_coordinates(removing_coordinate)
                self.game.changing_occupied_list(new_coordinates,"undo")

                self.solver(removing_coordinate[0],removing_coordinate[1]+1)


class Algoritm2:
    """This klass performs an algoritmic solution to the game 'argatroll'
    """

    def __init__(self,game,function_buttons_clicked):
        """the intakes are the game itself so functions can be used
        and the 'function button' will be a method inside th class 'Gamewindow'
        for automatically pressing a coordinate button.
        """
        self.game = game
        self.function_to_gui = function_buttons_clicked

    def returning_position(self,current_row,start_column):
        """This will take argument of which row to go through
        and which column to start from, in order to jump over
        unwanted part of the row
        """

        row = current_row #this is the current row to check on

        #in the current row go though all possible positions starting from a specifik coloumn
        for column in range(start_column,self.game.size+1):

            position = (row,column)#creates a position to try

            if self.game.angry_troll_check(position):
                return position #if the position is possible return it 

        return False
    
    def solver(self,start_row=1,start_column=1):
        """this method orcistrates the whole algoritm
        default starting cooridnate is (1,1)
        """

        column = start_column 
        current_row = start_row

        for row in range(current_row,self.game.size+1):
            
            position = self.returning_position(row,column)#retrives the first possible coordinate in this row

            if position != False: #if there is a possible coordinate
                
                self.function_to_gui(position,"occupy") #the algoritm occupies it (places a troll)
                column = 1
                    
            else: #the algoritm takes away the last placed troll, since the solver has in this case gone to a 'dead end'
                try:
                    removing_coordinate = self.game.trolls[-1]
                    self.function_to_gui(removing_coordinate,"undo")
                    #back tracks to the latest row, altough now starting on the next coloumn
                    self.solver(removing_coordinate[0],removing_coordinate[1]+1)
                    if len(self.game.trolls) == self.game.size:
                        raise IndexError #if all possible trolls are placed it will raise an index problem
                except IndexError:
                    return #algoritm stops
                
                
                


def main():
    """main is used to disply the algoritm inside the terminal"""
    size = 11
    array = {}
    coordinates = []
    coordinates = argatroll.coordinate_system(size)

    game = argatroll.Gameboard(size=size,array=array,coordinates=coordinates)

    solver = Algoritm(game)

    solver.solver(1,1)


if __name__ == "__main__":
    main()