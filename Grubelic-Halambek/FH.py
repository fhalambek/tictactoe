from random import *



def main(mat, val):
    #print("usao")
    turn = 9
    for i in range(3):
        for j in range(3):
            if(mat[i][j] == 0):
                turn -= 1
    
    
    
    #print(mat, val)
    
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
    
    if(turn == 0):
        return (0, 0)
    
    if(turn == 2):
        if(mat[1][1] != 0):
            return(2, 2)
        if((mat[1][0] != 0 and mat[1][0] != val) or (mat[0][1] != 0 and mat[0][1] != val) or (mat[1][2] != 0 and mat[1][2] != val) or (mat[2][1] != 0 and mat[2][1] != val)):
            return (1, 1)
        if(mat[1][0] == 0 and mat[2][0] == 0):
            return (2, 0)
        if(mat[0][1] == 0 and mat[0][2] == 0):
            return (0, 2)
    
    if(turn == 4):
        if(mat[1][1] == 0 and mat[2][2] == 0):
            return(2, 2)
        if(mat[1][0] == 0 and mat[2][0] == 0):
            return (2, 0)
        if(mat[0][1] == 0 and mat[0][2] == 0):
            return (0, 2)
        

    if(turn == 1):
        if(mat[1][1] != 0 and mat[1][1] != val):
            return (0, 0)
        if((mat[0][0] != 0 and mat[0][0] != val) or (mat[0][2] != 0 and mat[0][2] != val) or (mat[2][2] != 0 and mat[2][2] != val) or (mat[2][0] != 0 and mat[2][0] != val)):
            return (1, 1)
        if((mat[1][0] != 0 and mat[1][0] != val) or (mat[0][1] != 0 and mat[0][1] != val)):
            return (0, 0)
        if((mat[1][2] != 0 and mat[1][2] != val) or (mat[2][1] != 0 and mat[2][1] != val)):
            return (2, 2)

    if(turn == 3):
        if(mat[1][1] == val):
            if(mat[1][0] == 0 and mat[0][1] == 0 and mat[1][2] == 0 and mat[2][1] == 0):
                return (1, 0)
            if(mat[0][1] != 0 and mat[0][1] != val):
                if(mat[2][0] != 0 and mat[2][0] != val):
                    return (0, 2)
                if(mat[2][2] != 0 and mat[2][2] != val):
                    return (0, 0)
            if(mat[1][0] != 0 and mat[1][0] != val):
                if(mat[0][2] != 0 and mat[0][2] != val):
                    return (2, 0)
                if(mat[2][2] != 0 and mat[2][2] != val):
                    return (0, 0)
            if(mat[2][1] != 0 and mat[2][1] != val):
                if(mat[0][0] != 0 and mat[0][0] != val):
                    return (2, 2)
                if(mat[0][2] != 0 and mat[0][2] != val):
                    return (2, 0)
            if(mat[1][2] != 0 and mat[1][2] != val):
                if(mat[0][0] != 0 and mat[0][0] != val):
                    return (2, 2)
                if(mat[2][0] != 0 and mat[2][0] != val):
                    return (0, 2)
        if(mat[0][0] == val and mat[1][1] != 0 and mat[2][2] == mat[1][1]):
            return (0, 2)
        return (1, 1)
                
                
        
    while(1):
        xx = randint(0, 2)
        yy = randint(0, 2)
        if(mat[xx][yy] == 0):
            return (xx, yy)
