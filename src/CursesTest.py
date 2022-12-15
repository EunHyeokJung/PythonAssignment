import curses
import string

# arrowOptions function (수제작)
def arrowOptions(options: list, title: string, indicator = ">"):
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    class OptionPoint:
        Min = 2
        Max = 4
        current = Min

    myCursor = OptionPoint

    screen.addstr(0, 0, title)

    for idx, option in enumerate(options):
        screen.addstr(idx+2, 2, option)
    
    screen.addstr(myCursor.Min, 0, indicator)

    def cursorUp():
        screen.addstr(myCursor.current, 0, " ")
        if myCursor.current == myCursor.Min:
            myCursor.current = myCursor.Max
        else:
            myCursor.current -= 1
        screen.addstr(myCursor.current, 0, ">")

    def cursorDown():
        screen.addstr(myCursor.current, 0, " ")
        if myCursor.current == myCursor.Max:
            myCursor.current = myCursor.Min
        else:
            myCursor.current += 1
        screen.addstr(myCursor.current, 0, ">")


    while True:
        char = screen.getch()
        if char == curses.KEY_ENTER or char == 10 or char == 13:
            break
        elif char == curses.KEY_UP:
            cursorUp()
        elif char == curses.KEY_DOWN:
            cursorDown()

    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

    return myCursor.current - myCursor.Min, options[myCursor.current-myCursor.Min]  
