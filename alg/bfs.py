from queue import Queue

def bfs(src_x, src_y, des_x, des_y, invalid, canvas):
    if(src_x == -1 or src_y == -1 or des_x == -1 or des_y == -1):
        return
    
    def valid(x, y):
        if x < 33 and x >= 0 and y < 62 and y >= 0 and grid[x][y] == 1: return True
        return False

    grid = []
    used = []
    par = []
    searchspace = []
    for i in range(70):
        grid.append([1] * 70)
        used.append([0] * 70)
        par.append([[-1, -1]] * 70)
    
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    for x, y in invalid:
        grid[x][y] = 0
    
    used[src_x][src_y] = 1
    q = Queue()
    q.put((src_x, src_y))
    
    while not q.empty():
        row, col = q.get()
        if row == des_x and col == des_y:
            break

        searchspace.append([row, col])
        for i in range(4):
            tx = row + dx[i]
            ty = col + dy[i]

            if valid(tx, ty) and used[tx][ty] == 0:
                used[tx][ty] = 1
                q.put((tx, ty))
                par[tx][ty] = [row, col]
    
    path = []
    x, y = des_x, des_y
    while par[x][y] != [-1, -1]:
        path.append([x, y])
        x = par[x][y][0]
        y = par[x][y][1]
    
    path.reverse()
    return used[des_x][des_y], searchspace, path
    
    
    
    


    



