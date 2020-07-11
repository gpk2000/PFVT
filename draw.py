import tkinter as tk
from tkinter import messagebox, OptionMenu, StringVar
from alg import bfs

class root:
    def __init__(self):

        self.cors = []
        self.x_cors = []
        self.y_cors = []
        self.src_x, self.src_y = -1, -1
        self.des_x, self.des_y = -1, -1
        self.invalid = []
        self.color = 'green'
        self.drawn = False

        self.window = tk.Tk()
        self.init()
        self.window.mainloop()
    
    def init(self):
        self.canvas = tk.Canvas(self.window, width = 1300, height = 700 , bg = 'white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Configure>', self.draw_grid) 
        self.windowState = True
        self.window.resizable(False, False)
        self.window.attributes('-zoomed', self.windowState)
        self.window.title('Path-Find Visualizer')
        self.window.bind('<Button-1>', self.fill_square)
        self.window.bind('<B1-Motion>', self.fill_square)
        self.clear = tk.Button(self.window, width = 5, height = 1, text = 'Clear!!', command = self.clearAll)
        self.clear.place(x = 0, y = 0)
        self.run = tk.Button(self.window,  width = 5, height = 1, text = 'Run!!', command = self.runAlg)
        self.run.place(x = 0, y = 30)
        self.var = StringVar(self.window)
        self.var.set("BFS")
        self.menu = OptionMenu(self.window, self.var, 'BFS', 'A-Star')
        self.menu.place(x = 68, y = 0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Configure>', self.draw_grid) 
        self.windowState = True
        self.window.attributes('-zoomed', self.windowState)
        self.window.title('Path-Find Visualizer')
        self.window.bind('<F11>', self.toggleFullScreen)
        self.window.bind('<Escape>', self.quitFullScreen)
        self.window.bind('<Button-1>', self.fill_square)
        self.window.bind('<B1-Motion>', self.fill_square)

    def toggleFullScreen(self, event):
        self.windowState = not self.windowState
        self.window.attributes('-zoomed', self.windowState)
        self.window.geometry('1000x600')
       
    
    def quitFullScreen(self, event):
        self.windowState = False
        self.window.attributes('-zoomed', self.windowState)
    
    def draw_grid(self, event):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.delete('grid_line')

        # Creates all vertical lines at intevals of 100
        for i in range(0, w, 22):
            self.x_cors.append(i)
            self.canvas.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, h, 22):
            self.y_cors.append(i)
            self.canvas.create_line([(0, i), (w, i)], tag='grid_line')
        
        for i in range(len(self.y_cors)):
            for j in range(len(self.x_cors)):
                self.cors.append([i, j])
        
    def fill_square(self, event):
        x, y = event.x, event.y
        row, col = -1, -1

        for i in range(len(self.x_cors)):
            if(self.x_cors[i] <= x):
                row = i
        for i in range(len(self.y_cors)):
            if(self.y_cors[i] <= y):
                col = i
        
        if row == 0 and col == 0: return
        if row == 1 and col == 0: return

        ids = self.canvas.find_overlapping(x, y, x, y)
        if(len(ids) > 0):
            return
            
        self.canvas.create_rectangle(row * 22, col * 22, (row + 1) * 22, (col + 1) * 22, fill = self.color)
        if(self.color == 'green'):
            self.src_x, self.src_y = col, row
            self.color = 'red'
        elif(self.color == 'red'):
            self.des_x, self.des_y = col, row
            self.color = 'black'
        else:
            self.invalid.append([col, row])
    
    
    def draw(self, items, fill, delay):
        col, row = items.pop()
        if [col, row]== [self.src_x, self.src_y] or [col, row] == [self.des_x, self.des_y]:
            if len(items) > 0:
                self.canvas.after(delay, self.draw, items, fill, delay)
        else:
            self.canvas.create_rectangle(row * 22, col * 22, (row + 1) * 22, (col + 1) * 22, fill = fill)
            if len(items) > 0:
                self.canvas.after(delay, self.draw, items, fill, delay)
            

    def runAlg(self):
        if(self.src_x == -1 or self.src_y == -1 or self.des_x == -1 or self.des_y == -1):
            return

        found, searchspace, path = False, [], []

        if self.var.get() == 'BFS':
            found, searchspace, path = bfs.main(self.src_x, self.src_y, self.des_x, self.des_y, self.invalid)
        elif self.var.get() == 'Dijkstra':
            pass
        elif self.var.get() == 'A-Star':
            pass

        if not found:
            msg = messagebox.showerror(title = "Invalid", message = "Path Not Found") 
            self.clearAll()
            return

        if self.drawn == True:
            row, col = self.src_x, self.src_y
            self.drawn = False
            self.redraw(searchspace, path)
            return
            
        self.drawn = True
        self.prev_y = self.des_y
        self.prev_x = self.des_x
        searchspace.reverse()
        
        # Removed the bug. When there is a left turn
        for i in range(1, len(path)):
            diff = abs(path[i][0] - path[i - 1][0])
            diff += abs(path[i][1] - path[i - 1][1])
            if diff > 1:
                path.insert(i, [path[i - 1][0], path[i - 1][1] + 1])
        
        self.draw(searchspace, 'blue', 5)
        self.canvas.after((len(searchspace) + len(path)) * 5 + 500, self.draw, path, 'pink', 5)

    def redraw(self, searchspace, path):
        self.draw(searchspace, 'white', 0)
        self.canvas.after(500, self.runAlg)

    def clearAll(self):
        self.window.destroy()
        self.__init__()
    

if __name__ == '__main__':
    app = root()
