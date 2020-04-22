#!/usr/bin/env python3
import os
import sys
import tkinter as tk
from tkinter import messagebox as box
from random import randint,choice
########################################################################################################################################
def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
########################################################################################################################################
playerShipData = {}
enemyShipData = {}
takenPlayerShipCoords = set()
takenPlayerGuessCoords = set()
takenEnemyShipCoords = set()
takenEnemyGuessCoords = set()
########################################################################################################################################
class MainApplication(tk.Frame):
    def __init__(self, master=None, width=586, height=586):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height

        #Setup window parameters
        master.title("Battleships")
        master.geometry("1172x586")
        master.minsize(1172,586)
        master.resizable(False, False)

        #Set icon image
        master.tk.call("wm", "iconphoto", self.master._w, tk.PhotoImage(file=resource_path("icon.png")))

        #Create and place the canvas for the player's grid
        self.playerGrid = tk.Canvas(self.master, width=width, height=height, highlightthickness=0, bg='black')
        self.playerGrid.grid(row=0,column=0)

        self.enemyGrid = tk.Canvas(self.master, width=width, height=height, highlightthickness=0, bg='black')
        self.enemyGrid.grid(row=0,column=1)
        #Start the player grid functionality
        self.player = DoPlayerGrid(self)
        self.enemy = DoEnemyGrid(self)

        self.start(self.player)
        self.start2(self.enemy)

    def start(self,area):
        self.master.bind("<r>", area.changeRotation)
        self.playerGrid.bind("<Motion>", area.cursorShip)
        self.playerGrid.bind("<Button-1>", area.placeShip)
        #self.master.bind("<Insert>", area.addGuess)

    def start2(self,area):
        self.enemyGrid.bind("<Motion>", area.cursor)
        area.randomShipGeneration()
        self.master.bind("<q>", area.addGuess)
########################################################################################################################################
class DoPlayerGrid(object):
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        self.playerGrid = mainWindow.playerGrid

        self.game = Game()

        self.shipLengthToPixels = {2:75,3:128,4:181,5:234}
        self.shipLength = 5
        self.shipType = self.game.playerShipsLeftToPlace[0]
        self.shipLengthPixels = self.shipLengthToPixels[self.shipLength]
        self.rotation = "r"

        self.takenPlayerShipCoords = takenPlayerShipCoords
        self.takenPlayerGuessCoords = takenPlayerGuessCoords

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

    def cursorShip(self,event):
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

    def cursorGuess(self,event):
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

    def getRotateCoords(self):
        if self.rotation == "r":
            return self.x-5, self.y-3, self.x + self.shipLengthPixels+5, self.y + 27
        elif self.rotation == "l":
            return self.x + 22, self.y-3, (self.x +22)- self.shipLengthPixels - 2, self.y + 27
        elif self.rotation == "d":
            return self.x-5 , self.y, self.x + 25, self.y + self.shipLengthPixels + 2
        elif self.rotation == "u":
            return self.x-5 , self.y + 24, self.x + 25, (self.y +22)- self.shipLengthPixels -2

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

            if current in self.takenPlayerShipCoords:
                return True
        return False

    def placeShip(self,event):
        if len(self.game.playerShipsLeftToPlace) != 0:
            check = self.checkPlacement()
            if not check:
                self.game.addPlayerShip(self.shipType,self.posX,self.posY,self.rotation)
                self.playerGrid.create_rectangle(self.getRotateCoords(), fill="blue")

                for i in range(self.shipLength):
                    if self.rotation == "r":
                        self.takenPlayerShipCoords.add((self.posX + i,self.posY))
                    elif self.rotation == "l":
                        self.takenPlayerShipCoords.add((self.posX - i,self.posY))
                    elif self.rotation == "d":
                        self.takenPlayerShipCoords.add((self.posX,self.posY + i))
                    elif self.rotation == "u":
                        self.takenPlayerShipCoords.add((self.posX,self.posY - i))

                self.game.playerShipsLeftToPlace.remove(self.game.playerShipsLeftToPlace[0])
                try:
                    self.shipType = self.game.playerShipsLeftToPlace[0]
                    self.shipLength = self.game.shipTypeLength[self.shipType]
                    self.shipLengthPixels = self.shipLengthToPixels[self.shipLength]
                except:
                    self.stop()
            else:
                box.showwarning("Placement Error", "You cannot place a ship on top of another.")
        else:
            self.stop()

    def addGuess(self,event=None):
        guessX = ((self.posX+1) * 53) + 1 + 26.25
        guessY = ((self.posY+1) * 53) + 1 + 26.25
        guess = self.game.guessPlayer(self.posX,self.posY)
        self.playerGrid.create_oval(guessX-10,guessY-10,guessX+10,guessY+10,fill=guess)

    def stop(self,event=None):
        self.mainWindow.unbind("<r>")
        self.playerGrid.unbind("<Motion>")
        #self.playerGrid.bind("<Motion>", self.cursorGuess)
        self.playerGrid.unbind("<Button-1>")
        #self.mainWindow.start2(self.mainWindow.enemy)
########################################################################################################################################
class DoEnemyGrid(object):
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        self.enemyGrid = mainWindow.enemyGrid

        self.game = Game()


        self.shipLength = 5
        self.shipType = self.game.enemyShipsLeftToPlace[0]
        self.rotation = "r"

        self.takenEnemyShipCoords = takenEnemyShipCoords
        self.takenEnemyGuessCoords = takenEnemyGuessCoords

        self.boxesX = {}
        for i in range(10):
            self.boxesX[range(((i*53)+56),(((i+1)*53)+56))] = ((i*53)+69.5)

        self.boxesY = {}
        for i in range(10):
            self.boxesY[range(((i*53)+56),(((i+1)*53)+56))] = ((i*53)+67.5)

        self.enemyGridImage = tk.PhotoImage(file="grid/grid.png")
        self.enemyGrid.create_image(0, 0, image=self.enemyGridImage, anchor="nw")

        self.rect = self.enemyGrid.create_rectangle(0, 0, 0, 0, fill="blue")

    def randomShipGeneration(self):
        while len(self.game.enemyShipsLeftToPlace) != 0:
            self.rotation = choice(["r","d","l","u"])
            if self.rotation == "r":
                self.posX = randint(0,self.shipLength)
                self.posY = randint(0,9)
            elif self.rotation == "l":
                self.posX = randint(self.shipLength-1,9)
                self.posY = randint(0,9)
            elif self.rotation == "d":
                self.posX = randint(0,9)
                self.posY = randint(0,self.shipLength)
            elif self.rotation == "l":
                self.posX = randint(0,9)
                self.posY = randint(self.shipLength-1,9)
            self.placeShip()
        pass

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

    def addGuess(self,event=None):
        guessX = ((self.posX+1) * 53) + 1 + 26.25
        guessY = ((self.posY+1) * 53) + 1 + 26.25
        guess = self.game.guessEnemy(self.posX,self.posY)
        self.enemyGrid.create_oval(guessX-10,guessY-10,guessX+10,guessY+10,fill=guess)

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

            if current in self.takenEnemyShipCoords:
                return True
        return False

    def placeShip(self,event=None):
        if len(self.game.enemyShipsLeftToPlace) != 0:
            check = self.checkPlacement()
            if not check:
                self.game.addEnemyShip(self.shipType,self.posX,self.posY,self.rotation)
                for i in range(self.shipLength):
                    if self.rotation == "r":
                        self.takenEnemyShipCoords.add((self.posX + i,self.posY))
                    elif self.rotation == "l":
                        self.takenEnemyShipCoords.add((self.posX - i,self.posY))
                    elif self.rotation == "d":
                        self.takenEnemyShipCoords.add((self.posX,self.posY + i))
                    elif self.rotation == "u":
                        self.takenEnemyShipCoords.add((self.posX,self.posY - i))

                self.game.enemyShipsLeftToPlace.remove(self.game.enemyShipsLeftToPlace[0])
                try:
                    self.shipType = self.game.enemyShipsLeftToPlace[0]
                    self.shipLength = self.game.shipTypeLength[self.shipType]
                except:
                    self.stop()
            else:
                None
        else:
            self.stop()

    def stop(self):
        #print(self.takenEnemyShipCoords)
########################################################################################################################################
class Game(object):
    def __init__(self):
        self.shipTypeLength = {"Carrier":5, "Battleship":4,"Cruiser":3,
                                "Submarine":3,"Destroyer":2}

        self.playerShipsLeftToPlace = ["Carrier","Battleship","Cruiser","Submarine","Destroyer"]
        self.playerShipData = playerShipData

        self.enemyShipsLeftToPlace = ["Carrier","Battleship","Cruiser","Submarine","Destroyer"]
        self.enemyShipData = enemyShipData

        self.takenPlayerShipCoords = takenPlayerShipCoords
        self.takenPlayerGuessCoords = takenPlayerGuessCoords

        self.takenEnemyShipCoords = takenEnemyShipCoords
        self.takenEnemyGuessCoords = takenEnemyGuessCoords

    def addPlayerShip(self,shipType,posX,posY,dir):
        self.playerShipData[shipType] = {"Coords":(posX,posY),"Direction":dir}

    def addEnemyShip(self,shipType,posX,posY,dir):
        self.enemyShipData[shipType] = {"Coords":(posX,posY),"Direction":dir}

    def guessPlayer(self,x,y):
        currentGuess = (x,y)
        if currentGuess in self.takenPlayerGuessCoords:
            box.showwarning("Guess Error", "This coordinate has already been guessed.")
        else:
            self.takenPlayerGuessCoords.add(currentGuess)
            if currentGuess in self.takenPlayerShipCoords:
                return "red"
            else:
                return "white"

    def guessEnemy(self,x,y):
        currentGuess = (x,y)
        if currentGuess in self.takenEnemyGuessCoords:
            box.showwarning("Guess Error", "This coordinate has already been guessed.")
        else:
            self.takenEnemyGuessCoords.add(currentGuess)
            if currentGuess in self.takenEnemyShipCoords:
                return "red"
            else:
                return "white"


########################################################################################################################################
def main():
    root = tk.Tk()
    app = MainApplication(master=root)
    app.mainloop()
########################################################################################################################################
if __name__ == "__main__":
	main()
