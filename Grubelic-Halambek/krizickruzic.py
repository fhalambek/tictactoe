#Last changed 27/10 03:22 FH
from tkinter import *
from time import *
from threading import Thread, main_thread

##TODO:

#funkcije koje imaju veze s designom: reset, declareWinner (boja kvadratica kod pobjede i onaj dolje label winnner)
#startGame, refreshCountbotVsBot, humanVsBot, startMenu (menu)
#about (toplevel)
BUTTON_BACKGROUND = "#CCCCCC"
WINDOW_BACKGROUND = "#EEEEEE"
MENU_FONT = ("Verdana", 14)
#fontovi: Arial (Helvetica), Courier New (Courier), Comic Sans MS, Fixedsys, MS Sans Serif, MS Serif, Symbol, System, Times New Roman (Times), Verdana
#stilovi: normal, bold, roman, italic, underline, overstrike

XTO_COLORS = ("#993333", "#333399", "#339933")


VERTICAL_MARGIN = 16
HORIZONTAL_MARGIN = 32
OPTIONS_H_MARGIN = 16
OPTIONS_V_MARGIN = 8
CHART_HEIGHT = 24
CHART_WIDTH = 256
BUTTON_SIZE = 128 #veci ili jednak velicini slike unutar njega
ERROR = 39


turn = 1
isXFirst = 1
X = O = 0
initialized = False
end = False
screenSaverOn = False
optionList = ["HUMAN", "EASY", "MEDIUM", "FH", "DG"]
winX = winO = games = 0
display = []
correctFields = []
isWaiting = True

screenSaverOn = False
ssMatrix = [[0,0,0], [0,0,0], [0,0,0]]
ssX = 1
ssY = 2
ssTurn = 0

#kad stisnem gumb
def onButtonPress(event, y = 4):
    if(end):
        return
    global turn, states
    #ako je funkcija pokrenuta klikom misa
    if(y == 4):
        if((turn + isXFirst) % 2 and X != 1 or not((turn + isXFirst) % 2) and O != 6):
            return
        #znam foru s dictionaryjem, ali necu ju stavljat da ne moramo razmisljat tijekom redesigna
        #o tome hoce li se funkcionalnost promijeniti
        for i in range(3):
            if(event.widget in buttons[i]):
                j = buttons[i].index(event.widget)
                break
    else:
        i = event
        j = y    #Python :')
    if(states[i][j]):
        return
    elif((turn+isXFirst)%2):
        buttons[i][j].config(image = PIC_CROSS)
        states[i][j] = X
    else:
        buttons[i][j].config(image = PIC_CIRCLE)
        states[i][j] = O
    turn += 1
    winner = getWinner(states, 0)
    if(winner):
        declareWinner(winner)
        window.update()
        if isWaiting:
            sleep(.4)
        reset()
    elif(turn == 10):
        declareTie()
        window.update()
        if isWaiting:
            sleep(.4)
        reset()
    else:
        window.update()
    #ako igra insan protiv bota, pokreni bota ako treba
    if((X == 1) != (O == 6)):
        if((turn + isXFirst) % 2 and X != 1):
            x, y = startBot()
            if(x != ERROR):
                sleep(.2)
                onButtonPress(x, y)
        elif(not((turn + isXFirst) % 2) and O != 6):
            x, y = startBot()
            if(x != ERROR):
                sleep(.2)
                onButtonPress(x, y)

#provjerava je li netko pobijedio i ako je, u correctFields
#sprema polja koja treba obojati i vraca tko je pobijedio
def getWinner(matrix, isLeft):
    global correctFields
    correctFields = [(9,9),(9,9),(9,9)]
    for i in range(3):
        for j in range(3):
            if (matrix[i][j] != matrix[i][0] or not(matrix[i][0])):
                break
            if(isLeft):
                correctFields[j] = (j, 2-i)
            else:
                correctFields[j] = (i, j)
        else:
            return matrix[i][0]
    for i in range(3):
        if (matrix[i][i] != matrix[0][0] or not(matrix[0][0])):
            break
    else:
        correctFields = [(0, isLeft * 2), (1, 1), (2, 2 - isLeft * 2)]
        return matrix[1][1]
    if(isLeft):
        return 0
    return getWinner(rotateLeft(matrix), 1)

#rotira matricu
def rotateLeft(matrix):
    result = []
    for i in range(3):
        result.append([])
        for j in range(3):
            result[i].append(matrix[j][2-i])
    return result

#nakon zavrsene partije vraca sve u pocetno stanje osim countera pobjeda
def reset():
    global pics, states, turn, isXFirst, buttons
    isXFirst = (isXFirst - 1) * -1
    turn = 1
    if(winner.winfo_exists()):
        winner.config(text = "")
    for i in range(3):
        for j in range(3):
            states[i][j] = 0
            if(buttons[i][j].winfo_exists()):
                buttons[i][j].config(image = PIC_TRANSPARENT, bg = BUTTON_BACKGROUND, activebackground = BUTTON_BACKGROUND)

#cisti menu kako bi se mogli staviti novi widgeti
def clearMenu():
    global menu
    for child in menu.winfo_children():
        child.destroy()

#odredi koji bot je na redu i pozove ga
#ako bot ima krivi output, gubi partiju
def startBot():
    global states, X, O, isXFirst
    temp = []
    for i in range(3):
        temp.append([])
        for j in range(3):
            temp[i].append(states[i][j])
    if((turn + isXFirst) % 2):
        botName = (X-1)%5 - 1
        botNumber = X
        winner = O
    else:
        botName = (O-1)%5 - 1
        botNumber = O
        winner = X
    try:
        if(botName == 0):
            from easy import main
        elif(botName == 1):
            from medium import main
        elif(botName == 2):
            from FH import main
        elif(botName == 3):
            from DG import main
        try:
            i, j = main(temp, botNumber)
        except(UnboundLocalError):
            print("botName =", botName, "turn =", turn)
    except(TypeError, ValueError) as error:
        declareWinner(winner, ERROR)
        print("Invalid bot output: " + str(error))
        return (ERROR, ERROR)
    if(i in (0, 1, 2) and j in (0, 1, 2) and not(states[i][j])):
        return (i, j)
    print("Wrong bot output(" + str(i) + ", " + str(j), states)
    print(i, j)
    declareWinner(winner, ERROR)
    return (ERROR, ERROR)

#proglasava pobjednika
def declareWinner(code, error = 0):
    global winX, winO, games, correctFields, buttons, winner
    games += 1
    if(code == X):
        winner.config(text = "X WON", font = ("Verdana", 16, "bold"))
        winX += 1
        winnerColor = XTO_COLORS[0]
    else:
        winner.config(text = "O WON", font = ("Verdana", 16, "bold"))
        winO += 1
        winnerColor = XTO_COLORS[2]
    if(not(error)):
        for i in correctFields:
            buttons[i[0]][i[1]].config(bg = winnerColor, activebackground = winnerColor)
    refreshCount(winX, games, winO)

#proglasava nerijesenu partiju
def declareTie():
    global winX, winO, games, winner
    games += 1
    winner.config(text = "TIE", font = ("Verdana", 16, "bold"))
    refreshCount(winX, games, winO)

#kroz ovu funkciju se prode na pocetku igre
#da se postavi menu za igru i odredi
#u kojem trentku se pozivaju botovi
def startGame():
    global X, O, menu, display, screenSaverOn, isXfirst
    screenSaverOn = False
    isXfirst = 1
    reset()
    clearMenu()
    display = []
    menu.config(text = "")
    for i, k in enumerate(("X:", "TIE:", "O:")):
        display.append([Label(menu, text = k), Label(menu, text = "0", width = 5), Label(menu, image = PIC_TRANSPARENT, width = 0, height = CHART_HEIGHT, bg = WINDOW_BACKGROUND, anchor = W)])
        for j in range(3):
            display[i][j].config(bg = WINDOW_BACKGROUND, font = MENU_FONT)
            if(j < 2):
                display[i][j].grid(row = i*2, column = j, pady = OPTIONS_V_MARGIN, sticky = S + N)
            else:
                display[i][2].grid(row = i * 2 + 1, column = 0, columnspan = 2, sticky = W)
        
    mButton = Button(menu, text = "MAIN MENU", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    mButton.bind("<ButtonRelease>", mainMenu)
    mButton.grid(row = i * 2 + 2, column = 0, columnspan = 3, padx = OPTIONS_H_MARGIN, pady = OPTIONS_V_MARGIN)
    while(X != 1 and O != 6):
        x, y = startBot()
        if(x == ERROR):
            continue
        else:
            onButtonPress(x, y)
        #sleep(.2)
        if(O == 6 or end or X == 1):
            return
    if(X != 1 and O == 6):
        sleep(.2)
        x, y = startBot()
        print(x, y)
        if(x != ERROR):
            onButtonPress(x, y)

#updatea chart
def refreshCount(x, g, o):
    global display
    data = (x, g-(x+o), o)
    for i in range(3):
        if(str(data[i]) != display[i][1]["text"]):
            display[i][1].config(text = str(data[i]))
        lWidth = data[i] * CHART_WIDTH // sum(data)
        if(lWidth):
            display[i][2].config(width = lWidth, bg = XTO_COLORS[i])
        else:
            
            display[i][2].config(width = 0, bg = WINDOW_BACKGROUND)

#intercepta pritisak na X kod gasenja prozora da ne dobijemo ruznu poruku
def finisHim():
    global end, window, screenSaverOn
    screenSaverOn = 0
    end = True
    window.destroy()

#kad igrac u main menu odabere hvh
def humanVsHuman(event):
    global X, O, end
    end = False
    X = 1
    O = 6
    startGame()
    return

#povratak iz igre u main menu
def mainMenu(event):
    global winX, winO, isXFirst, games, end, isWaiting
    isWaiting = True
    end = True
    reset()
    isXFirst = 1
    winX = winO = games = 0
    startMenu()

#kad igrac u main menu odabere bvb ili nakon sto u hvb odabere human
def botVsBot(isX, picked):
    global optionList, menu, X, O, end, isWaiting
    isWaiting = False
    end = False
    clearMenu()
    bots = []
    if(not(isX)):
        X = picked
        menu.config(text = "\nPLAYER O", font = ("Verdana", 16))
    else:
        menu.config(text = "\nPLAYER X", font = ("Verdana", 16))
    for i, j in enumerate(optionList[1:]):
        bots.append(Button(menu, text = j, bg = BUTTON_BACKGROUND, font = MENU_FONT))
        if(isX):
            bots[i].bind("<ButtonRelease>", lambda x: botVsBot(False, optionList.index(x.widget["text"])+1))
        else:
            bots[i].bind("<ButtonRelease>", lambda x: lilHelper(optionList.index(x.widget["text"]) + 6))
        bots[i].grid(row = i, column = 0, columnspan = 2, sticky = E + W, padx = OPTIONS_H_MARGIN, pady = OPTIONS_V_MARGIN)
    bButton = Button(menu, text = "BACK", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    if(isX):
        bButton.bind("<ButtonRelease>", lambda x: startMenu())
    elif(X == 1):
        bButton.bind("<ButtonRelease>", lambda x: humanVsBot(x))
    else:
        bButton.bind("<ButtonRelease>", lambda event: botVsBot(True, ""))
    bButton.grid(row = i+1, column = 1, sticky = E, padx = (0, OPTIONS_H_MARGIN), pady = OPTIONS_V_MARGIN)

#kad igrac u main menu odabere hvb, ako sad igrac odabere bota, automatski je protivnik 6
def humanVsBot(event):
    clearMenu()
    global optionList, menu, end
    end = False
    menu.config(text = "\nPLAYER X", font = ("Verdana", 16))
    bots = []
    for i in range(len(optionList)):
        bots.append(Button(menu, text = optionList[i], bg = BUTTON_BACKGROUND, font = MENU_FONT))
        if(i):
            bots[i].bind("<ButtonRelease>", lambda x: lilHelper(optionList.index(x.widget["text"]) + 1))
        else:
            bots[0].bind("<ButtonRelease>", lambda x: botVsBot(False, optionList.index(x.widget["text"]) + 1))
        bots[i].grid(row = i, column = 0, columnspan = 2, sticky = E + W, padx = OPTIONS_H_MARGIN, pady = OPTIONS_V_MARGIN)
    bButton = Button(menu, text = "BACK", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    bButton.bind("<ButtonRelease>", lambda x: startMenu())
    bButton.grid(row = i+1, column = 1, sticky = E, padx = (0, OPTIONS_H_MARGIN), pady = OPTIONS_V_MARGIN)

#funkcija koja sredi to sto se ne mogu pozvati dvije naredbe u lambdi
def lilHelper(botToRun):
    global X, O
    if(botToRun > 5):
        O = botToRun
    else:
        X = botToRun
        O = 6
    startGame()

#kad igrac u main menu stisne about
def about(event):
    global window
    aboutWindow = Toplevel(window)
    aboutWindow.config(bg = WINDOW_BACKGROUND)
    aboutWindow.resizable(False, False)
    aboutWindow.attributes('-topmost', 1)
    creditsLabel = Label(aboutWindow, text = "Made by Fran Halambek\n& Damjan Grubelic, 2017", font = ("Verdana", 16), padx = 10, pady = 10)
    creditsEscape = Button(aboutWindow, text = "CLOSE", font = ("Verdana", 12), bg = BUTTON_BACKGROUND)
    creditsEscape.bind("<ButtonRelease>", lambda x: aboutWindow.destroy())
    creditsLabel.pack()
    creditsEscape.pack()
    Label(aboutWindow).pack()
    aboutWindow.mainloop()
    
#ovo radi main menu
def startMenu():
    global menu, screenSaverOn, ssTurn, ssMatrix
    if(initialized):
        clearMenu()
    menu.columnconfigure(0, weight = 1)
    menu.columnconfigure(1, weight = 1)
    menu.columnconfigure(2, minsize = 0)
    menu.grid_propagate(0)
    menu.config(text = "\nKRIZIC-KRUZIC", font = ("Verdana", 18, "bold"))
    
    hvh = Button(menu, text = "HUMAN VS HUMAN", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    hvh.bind("<ButtonRelease>", humanVsHuman)
    hvb = Button(menu, text = "HUMAN VS BOT", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    hvb.bind("<ButtonRelease>", humanVsBot)
    bvb = Button(menu, text = "BOT VS BOT", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    bvb.bind("<ButtonRelease>", lambda event: botVsBot(True, ""))
    for i, j in enumerate((hvh, hvb, bvb)):
        j.grid(row = i, column = 0, columnspan = 2, sticky = E + W, padx = OPTIONS_H_MARGIN, pady = OPTIONS_V_MARGIN)
    aButton = Button(menu, text = "ABOUT", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    aButton.bind("<ButtonRelease>", about)
    aButton.grid(row = 3, column = 0, sticky = E + W, padx = (OPTIONS_H_MARGIN, OPTIONS_H_MARGIN/2), pady = OPTIONS_V_MARGIN) 
    qButton = Button(menu, text = "QUIT", bg = BUTTON_BACKGROUND, font = MENU_FONT)
    qButton.bind("<ButtonRelease>", lambda event: finisHim())
    qButton.grid(row = 3, column = 1, sticky = E + W, padx = (OPTIONS_H_MARGIN/2, OPTIONS_H_MARGIN), pady = OPTIONS_V_MARGIN)
    
    window.update()
    if(not(screenSaverOn)):
        screenSaverOn = True
        ssTurn = 0
        ssMatrix = [[0,0,0], [0,0,0], [0,0,0]]
        proba = Thread(target = startSS)
        proba.start()

def startSS():
    global screenSaverOn
    while screenSaverOn and main_thread().is_alive():
        screenSaver()

def screenSaver():
    global ssMatrix, ssX, ssY, ssTurn, correctFields, screenSaverOn
    ssTurn += 1
    if(ssTurn%2):
        ssPlayer = ssX
        winnerColor = XTO_COLORS[0]
    else:
        ssPlayer = ssY
        winnerColor = XTO_COLORS[2]
    from medium import main
    x, y = main(ssMatrix, ssPlayer)
    ssMatrix[x][y] = ssPlayer
    if(ssTurn%2):
        buttons[x][y].config(image = PIC_CROSS)
    else:
        buttons[x][y].config(image = PIC_CIRCLE)
    ssWinner = getWinner(ssMatrix, 0)
    if(ssWinner):
        for i in correctFields:
            buttons[i[0]][i[1]].config(bg = winnerColor, activebackground = winnerColor)
    window.update()
    sleep(1)
    if(not(main_thread().is_alive())):
        screenSaverOn = False
        return
    if not(screenSaverOn):
        return
    if(ssWinner or ssTurn >= 9):
        for i in range(3):
            for j in range(3):
                ssTurn = 0
                ssMatrix[i][j] = 0
                buttons[i][j].config(image = PIC_TRANSPARENT, bg = BUTTON_BACKGROUND, activebackground = BUTTON_BACKGROUND)
    

#postavke glavnog prozora
window = Tk()
window.title("KRIZIC-KRUZIC")
window.config(bg = WINDOW_BACKGROUND)
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", finisHim)


#tablica 3x3
states = []
buttons = []
PIC_CROSS = PhotoImage(file = "png/cross.png")
PIC_CIRCLE = PhotoImage(file = "png/circle.png")
PIC_TRANSPARENT = PhotoImage()
for i in range(3):
    states.append([])
    buttons.append([])
    for j in range(3):
        states[i].append(0)
        buttons[i].append(Button(window, bg = BUTTON_BACKGROUND, width = BUTTON_SIZE, height = BUTTON_SIZE, image = PIC_TRANSPARENT))
        buttons[i][j].grid(row = i, column = j)
        if(i == 0):
            buttons[i][j].grid(pady = (VERTICAL_MARGIN, 0))
        if(i == 2):
            buttons[i][j].grid(pady = (0, VERTICAL_MARGIN))
        if(j == 0):
            buttons[i][j].grid(padx = (HORIZONTAL_MARGIN, 0))
        if(j == 2):
            buttons[i][j].grid(padx = (0, HORIZONTAL_MARGIN))
        buttons[i][j].bind('<ButtonRelease>', onButtonPress)
#ono dolje di se prikazuje tko je pobijedio na kraju partije
winner = Label(window, bg = WINDOW_BACKGROUND)
winner.grid(row = 4, column = 0, columnspan = 3, padx = HORIZONTAL_MARGIN, pady = (0, VERTICAL_MARGIN))
#inicijalizacija menua, osnovne karakteristike koje se ne mijenjaju
menu = LabelFrame(window, width = BUTTON_SIZE * 2, bg = WINDOW_BACKGROUND, text = "\nKRIZIC-KRUZIC", pady = 10, labelanchor = N, bd = 0)
menu.grid(row = 0, column = 3, rowspan = 3, sticky = N + S + E, pady = VERTICAL_MARGIN, padx = HORIZONTAL_MARGIN)
startMenu()
initialized = True      
window.mainloop()


