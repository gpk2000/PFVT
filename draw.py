import tkinter as tk
from tkinter import messagebox
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
        self.delay = 0

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
        self.run = tk.Button(self.window,  width = 5, height = 1, text = 'Run!!', command = self.runBfs)
        self.run.place(x = 0, y = 30)
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
    
    def draw(self, items, fill):
        col, row = items.pop()
        self.delay += 5
        self.canvas.create_rectangle(row * 22, col * 22, (row + 1) * 22, (col + 1) * 22, fill = fill)
        if len(items) > 0:
            self.canvas.after(5, self.draw, items, fill)
            

    def runBfs(self):
        if(self.src_x == -1 or self.src_y == -1 or self.des_x == -1 or self.des_y == -1):
            return

        found, searchspace, path = bfs.bfs(self.src_x, self.src_y, self.des_x, self.des_y, self.invalid, self.canvas)
        if found:
            searchspace.remove([self.src_x, self.src_y])
            path.remove([self.des_x, self.des_y])
            searchspace.reverse()
            self.draw(searchspace, 'blue')
            self.canvas.after((len(searchspace) + len(path)) * 5 + 500, self.draw, path, 'pink')

        else:
            msg = messagebox.showerror(title = "Invalid", message = "Path Not Found") 
            self.clearAll()  

    def clearAll(self):
        self.window.destroy()
        self.__init__()
    

if __name__ == '__main__':
    app = root()
