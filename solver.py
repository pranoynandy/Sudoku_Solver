def input_grid(data):
    grid = [[0 for i in range(9)] for j in range(9)]
    for row in range(9):
        for col in range(9):
            ind_name=str(row)+"_"+str(col)
            if(data[ind_name] != None and data[ind_name].isnumeric() and int(data[ind_name])in range(1,10)):
                x=data[ind_name]
                grid[row][col]=int(x)
    return grid

def check(mat, row, col, val):
    for i in range(9):
        if mat[row][i]==val or mat[i][col]==val:
            return False
    bi, bj =  row - row % 3, col - col % 3
    for i in range(bi,bi+3):
        for j in range(bj,bj+3):
            if mat[i][j]==val:
                return False
    return True

def zero(mat):
    for i in range(9):
        for j in range(9):
            if mat[i][j]==0:
                row=i
                col=j
                return row, col
    return -1, -1

def sudoku(mat):
    row, col = zero(mat)
    if row==-1:
        return True
    for i in range(1,10):
        if check(mat, row, col, i):
               mat[row][col]=i
               if sudoku(mat):
                   return True
               else:
                   mat[row][col]=0

def output(mat):
    for i in range(9):
        for j in range(9):
            print(mat[i][j],end=" ")
        print()
    