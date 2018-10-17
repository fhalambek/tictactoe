from random import *



def main(mat, val):
    #print("usao")
    turn = 9
    for i in range(3):
        for j in range(3):
            if(mat[i][j] == 0):
                turn -= 1
    
    
    
    #print(mat, val)
    '''
    for i in range(3):
        if(mat[i][0] == mat[i][1] and mat[i][0] == val):
            if(mat[i][2] == 0): return (i, 2)
        if(mat[i][1] == mat[i][2] and mat[i][1] == val):
            if(mat[i][0] == 0): return (i, 0)
        if(mat[i][0] == mat[i][2] and mat[i][2] == val):
            if(mat[i][1] == 0): return (i, 1)
        
        if(mat[0][i] == mat[1][i] and mat[0][i] == val):
            if(mat[2][i] == 0): return (2, i)
        if(mat[1][i] == mat[2][i] and mat[1][i] == val):
            if(mat[0][i] == 0): return (0, i)
        if(mat[0][i] == mat[2][i] and mat[2][i] == val):
            if(mat[1][i] == 0): return (1, i)
        
        if(mat[i][0] == mat[2-i][2] and mat[i][0] == val):
            if(mat[1][1] == 0): return (1, 1)
        if(mat[i][0] == mat[1][1] and mat[i][0] == val):
            if(mat[2-i][2] == 0): return (2-i, 2)
        if(mat[i][2] == mat[1][1] and mat[i][2] == val):
            if(mat[2-i][0] == 0): return (2-i, 0)
    
    for i in range(3):
        if(mat[i][0] == mat[i][1] and mat[i][0] != 0):
            if(mat[i][2] == 0): return (i, 2)
        if(mat[i][1] == mat[i][2] and mat[i][1] != 0):
            if(mat[i][0] == 0): return (i, 0)
        if(mat[i][0] == mat[i][2] and mat[i][2] != 0):
            if(mat[i][1] == 0): return (i, 1)
        
        if(mat[0][i] == mat[1][i] and mat[0][i] != 0):
            if(mat[2][i] == 0): return (2, i)
        if(mat[1][i] == mat[2][i] and mat[1][i] != 0):
            if(mat[0][i] == 0): return (0, i)
        if(mat[0][i] == mat[2][i] and mat[2][i] != 0):
            if(mat[1][i] == 0): return (1, i)
        
        if(mat[i][0] == mat[2-i][2] and mat[i][0] != 0):
            if(mat[1][1] == 0): return (1, 1)
        if(mat[i][0] == mat[1][1] and mat[i][0] != 0):
            if(mat[2-i][2] == 0): return (2-i, 2)
        if(mat[i][2] == mat[1][1] and mat[i][2] != 0):
            if(mat[2-i][0] == 0): return (2-i, 0)
    '''

    while(1):
        xx = randint(0, 2)
        yy = randint(0, 2)
        if(mat[xx][yy] == 0):
            return (xx, yy)
