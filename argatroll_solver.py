"""This program performs an algoritm to solve the game 'arga troll'
"""

import argatroll
import time



class Algoritm:

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

    def __init__(self,game,function_buttons_clicked):
        self.game = game
        self.function_to_gui = function_buttons_clicked

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
                
                self.function_to_gui(position,"occupy")
                column = 1
                    
            else: 
                try:
                    removing_coordinate = self.game.trolls[-1]
                    self.function_to_gui(removing_coordinate,"undo")
                    self.solver(removing_coordinate[0],removing_coordinate[1]+1)
                    if len(self.game.trolls) == self.game.size:
                        raise IndexError
                except IndexError:
                    return
                
                
                


def main():
    size = 11
    array = {}
    coordinates = []
    coordinates = argatroll.coordinate_system(size)

    game = argatroll.Gameboard(size=size,array=array,coordinates=coordinates)

    solver = Algoritm(game)

    solver.solver(1,1)


if __name__ == "__main__":
    main()