#!/usr/bin/env python3
import os
import sys
import tkinter as tk
from tkinter import messagebox as box
########################################################################################################################################
def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
########################################################################################################################################
playerShipData = {}
########################################################################################################################################
class MainApplication(tk.Frame):
    def __init__(self, master=None, width=586, height=586):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height

        #Setup window parameters
        master.title("Battleships")
        master.geometry("586x586")
        master.minsize(586,586)
        master.resizable(False, False)

        #Set icon image
        master.tk.call("wm", "iconphoto", self.master._w, tk.PhotoImage(file=resource_path("icon.png")))

        #Create and place the canvas for the player's grid
        self.playerGrid = tk.Canvas(self.master, width=width, height=height, highlightthickness=0, bg='black')
        self.playerGrid.grid(row=0,column=0)

        #Start the player grid functionality
        self.start(DoPlayerGrid(self))

    def start(self,area):
        self.master.bind("<r>", area.changeRotation)
        self.playerGrid.bind("<Motion>", area.cursor)
        self.playerGrid.bind("<Button-1>", area.placeShip)
########################################################################################################################################
class DoPlayerGrid(object):
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        self.playerGrid = mainWindow.playerGrid

        self.game = Game()

        self.playGrid = [[0 for y in range(10)] for x in range(10)]

        self.shipLengthToPixels = {2:75,3:128,4:181,5:234}
        self.shipLength = 5
        self.shipType = self.game.shipsLeftToPlace[0]
        self.shipLengthPixels = self.shipLengthToPixels[self.shipLength]
        self.rotation = "r"
        self.takenCoords = set()

        self.boxesX = {}
        for i in range(10):
            self.boxesX[range(((i*53)+56),(((i+1)*53)+56))] = ((i*53)+69.5)

        self.boxesY = {}
        for i in range(10):
            self.boxesY[range(((i*53)+56),(((i+1)*53)+56))] = ((i*53)+67.5)

        self.playerGridImage = tk.PhotoImage(file="grid/grid.png")
        self.playerGrid.create_image(0, 0, image=self.playerGridImage, anchor="nw")

        self.rect = self.playerGrid.create_rectangle(0, 0, 0, 0, fill="blue")

    def checkMove(self,rotate=False):
        if self.rotation == "r":
            if self.posX + self.shipLength -1 > 9:
                if not rotate:
                    self.posX = 9 - self.shipLength
                    self.x = 546.5 - (53*(self.shipLength-1))
                elif rotate:
                    self.changeRotation()

        elif self.rotation == "l":
            if self.posX - self.shipLength +1 < 0:
                if not rotate:
                    self.posX = 0 + self.shipLength
                    self.x = 69.5 + (53*(self.shipLength-1))
                elif rotate:
                    self.changeRotation()

        elif self.rotation == "d":
            if self.posY + self.shipLength -1 > 9:
                if not rotate:
                    self.posY = 9 - self.shipLength
                    self.y = 544.5 - (53*(self.shipLength-1))
                elif rotate:
                    self.changeRotation()

        elif self.rotation == "u":
            if self.posY - self.shipLength +1 < 0:
                if not rotate:
                    self.posY = 0 + self.shipLength
                    self.y = 67.5 + (53*(self.shipLength-1))
                elif rotate:
                    self.changeRotation()

    def cursor(self,event):
        self.x, self.y = event.x, event.y
        for key in self.boxesX:
                if self.x in key:
                    self.x = self.boxesX[key]
                    break

        for key in self.boxesY:
                if self.y in key:
                    self.y = self.boxesY[key]
                    break

        if self.x < 69.5:
            self.x = 69.5
        elif self.x > 546.5:
            self.x = 546.5
        if self.y < 67.5:
            self.y = 67.5
        elif self.y > 544.5:
            self.y = 544.5

        self.posX = int((self.x // 53)-1)
        self.posY = int((self.y // 53)-1)


        self.checkMove()
        self.playerGrid.coords(self.rect, self.getRotateCoords())


    def getRotateCoords(self):
        if self.rotation == "r":
            return self.x, self.y, self.x + self.shipLengthPixels, self.y + 25
        elif self.rotation == "l":
            return self.x + 22, self.y, (self.x +22)- self.shipLengthPixels, self.y + 25
        elif self.rotation == "d":
            return self.x , self.y, self.x + 25, self.y + self.shipLengthPixels
        elif self.rotation == "u":
            return self.x , self.y + 22, self.x + 25, (self.y +22)- self.shipLengthPixels

    def changeRotation(self,event=None):
        if self.rotation == "r":
            self.rotation = "d"
            self.checkMove(rotate=True)
        elif self.rotation == "d":
            self.rotation = "l"
            self.checkMove(rotate=True)
        elif self.rotation == "l":
            self.rotation = "u"
            self.checkMove(rotate=True)
        else:
            self.rotation = "r"
            self.checkMove(rotate=True)
        self.playerGrid.coords(self.rect, self.getRotateCoords())

    def checkPlacement(self):
        for i in range(self.shipLength):
            if self.rotation == "r":
                current = (self.posX + i,self.posY)
            elif self.rotation == "l":
                current = (self.posX - i,self.posY)
            elif self.rotation == "d":
                current = (self.posX,self.posY + i)
            elif self.rotation == "u":
                current = (self.posX,self.posY - i)

            if current in self.takenCoords:
                return True
        return False

    def placeShip(self,event):
        if len(self.game.shipsLeftToPlace) != 0:
            check = self.checkPlacement()
            if not check:
                self.game.addShip(self.shipType,self.posX,self.posY,self.rotation)
                self.playerGrid.create_rectangle(self.getRotateCoords(), fill="blue")

                for i in range(self.shipLength):
                    if self.rotation == "r":
                        self.takenCoords.add((self.posX + i,self.posY))
                    elif self.rotation == "l":
                        self.takenCoords.add((self.posX - i,self.posY))
                    elif self.rotation == "d":
                        self.takenCoords.add((self.posX,self.posY + i))
                    elif self.rotation == "u":
                        self.takenCoords.add((self.posX,self.posY - i))

                self.game.shipsLeftToPlace.remove(self.game.shipsLeftToPlace[0])
                try:
                    self.shipType = self.game.shipsLeftToPlace[0]
                    self.shipLength = self.game.shipTypeLength[self.shipType]
                    self.shipLengthPixels = self.shipLengthToPixels[self.shipLength]
                except:
                    self.stop()
            else:
                box.showwarning("Placement Error", "You cannot place a ship on top of another.")
        else:
            self.stop()

    def stop(self,event=None):
        self.mainWindow.unbind("<r>")
        self.playerGrid.unbind("<Motion>")
        self.playerGrid.unbind("<Button-1>")
########################################################################################################################################
class Game(object):
    def __init__(self):
        self.shipTypeLength = {"Carrier":5, "Battleship":4,"Cruiser":3,
                                "Submarine":3,"Destroyer":2}

        self.shipsLeftToPlace = ["Carrier","Battleship","Cruiser","Submarine","Destroyer"]

    def addShip(self,shipType,posX,posY,dir):
        playerShipData[shipType] = {"X":posX,"Y":posY,"Direction":dir}
########################################################################################################################################
def main():
    root = tk.Tk()
    app = MainApplication(master=root)
    app.mainloop()
########################################################################################################################################
if __name__ == "__main__":
	main()
