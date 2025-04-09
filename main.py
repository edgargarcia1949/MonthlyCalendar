import pygame, sys, asyncio 
from datetime import datetime, time
import calendar
import textwrap
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import textwrap
import os.path

pygame.font.init()
font13r = pygame.font.Font("OpenSans-Regular.ttf", 13)
font14 = pygame.font.Font("OpenSans-SemiBold.ttf", 14)
font16 = pygame.font.Font("OpenSans-Bold.ttf", 16)
font18 = pygame.font.Font("OpenSans-Regular.ttf", 18)
font24 = pygame.font.Font("OpenSans-SemiBold.ttf", 24)
font25 = pygame.font.Font(None, 25)
font26b = pygame.font.Font("OpenSans-Bold.ttf", 26)
font55b = pygame.font.Font("OpenSans-Bold.ttf", 55)

BLACK, WHITE, BLUE, GREEN, MAROON = (0,0,0), (255,255,255), (0,0,255), (0,128,0), (128,0,0) 
PURPLE, TEAL, FUCHSIA, LIME, OLIVE = (128,0,128), (0,128,128), (255,0,255), (0,255,0), (128,128,0) 
NAVYBLUE, RED, ORANGE, AQUA, TAN = (0,0,128), (255,0,0), (255,165,0), (0,255,255), (255,255,200)
COLOURS = [BLUE, GREEN, MAROON, PURPLE, TEAL, FUCHSIA, LIME, OLIVE, NAVYBLUE, RED, ORANGE, AQUA]

MONTH_STRINGS=["DECEMBER", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST",
            "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER", "JANUARY"]
WEEK_STRINGS_LONG=["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]
WEEK_STRINGS_SHORT=["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
DAY_NUMBERS=[" 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9","10","11","12","13","14","15",
      "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

RECT1 = (45, 68, 34, 90)      # first and second are position coordinates of rects
RECT2 = (640, 68, 34, 90)      # third and fourth are widths and heights of rects
RECT3 = (45, 158, 119, 25)
RECT4 = (45, 43, 238, 25)
RECT5 = (283, 43, 357, 115)
RECT6 = (45, 183, 833, 480)

WIDTH = 924
HEIGHT = 714

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

class MV:
    year = datetime.now().year
    current_month = datetime.now().month
    month = current_month-1
    monthObj = []    # will hold 12 instances of MonthCls class

class MonthClass:
    yr = MV.year   
    def __init__(self, name):
        self.name = name
        self.stday = 0
        self.dysinmth = 0
        self.yoffset = 0
        self.days = []  # 28 to 31 DayClass class instances
        self.mthcomments = ["" for i in range(31)]  # daily comments in monthly calendar

class Rect:            
    def do_rect(screen, x, y, w, h):
        pygame.draw.rect(screen, BLACK, (x, y, w, h), 1)
        
    def do_rects(screen, x, y, w, h, offset, qty):    
        [Rect.do_rect(screen, x+i*offset, y, w, h) for i in range(qty)]
        
    def do_hiLite_rect(screen, x, y, w, h):
        pygame.draw.rect(screen, TAN, (x, y, w, h))
      
    def do_note_rect(screen, x, y, w, h):
        pygame.draw.rect(screen, (255, 100, 255), (x, y, w, h))


class Text:   
    def do_text_year(screen, str, x, y, w, h, color, font):
        i, j = font.size(str)
        text = font.render(str, True, color)
        screen.blit(text, dest = (x+w/2-i/2, y+h/2-j/2))
    
    def do_text2(screen, str, x, y, font):
        text = font.render(str, True, BLACK)
        screen.blit(text, dest = (x, y))
    
    def do_text3(screen, str, x, y, font):
        text = font.render(str, True, BLUE)
        screen.blit(text, dest = (x, y))

    def do_text(screen, str, px, py, sx, sy, tuple, font):
        w, h = font.size(str)
        text = font.render(str, True, tuple)
        screen.blit(text, dest = (px+sx/2-w/2, py+sy/2-5))    

class DayClass:
    yr = MV.year   
    def __init__(self, month, dy):
        self.month = month
        self.dy = dy
        self.x = 0      # will be used as pos x on screen
        self.y = 0      # will be used as pos y on screen
       
class DSM:        
    def initialize_month(yr):
        MV.monthObj = []      # start with empty month instance list        
        for i in range(12):
            MV.monthObj.append(MonthClass(MONTH_STRINGS[i+1]))   \
                  # create 12 instances of MonthClass each called monthObj[i]
            temp = calendar.monthrange(yr, i+1)
            MV.monthObj[i].stday = (temp[0]+1)%7            # calc start day for each Month
            MV.monthObj[i].dysinmth = temp[1]               # calc number of days in Month for each Month
            for j in range(temp[1]):
                MV.monthObj[i].days.append(DayClass(i+1,j+1))   \
                      # create 28 to 31 instances of Day class in each Month instance called monthObj[i].days[i]
        for i in range(12):
            MV.monthObj[i].yoffset = 96                               # calc yoffsets      
            if MV.monthObj[i].stday >=5 and MV.monthObj[i].dysinmth == 31:    # happens about 3 times a year
                MV.monthObj[i].yoffset = 80
            if MV.monthObj[i].stday == 6 and MV.monthObj[i].dysinmth >= 30:
                MV.monthObj[i].yoffset = 80
            if MV.monthObj[1].stday == 0 and MV.monthObj[1].dysinmth == 28:    # happens about once in 10 years
                MV.monthObj[1].yoffset = 120
        for i in range(12):
            ctr = MV.monthObj[i].stday
            for j in range (MV.monthObj[i].dysinmth):
                MV.monthObj[i].days[j].x = 45 + ctr%7 * 119     # all days in year have x coordinate for display
                MV.monthObj[i].days[j].y = 183 + ctr//7 * MV.monthObj[i].yoffset    # all days in year have y coordinate
                ctr += 1        
        filename = "StaticHolidays.txt"    # load text file of holidays that do not change        
        DSM.load_monthly_comments(filename)           
        if yr > 2023 and yr < 2035:
            filename = str(yr) + "FloatHolidays.txt"    # load text file of holidays that do change
            DSM.load_monthly_comments(filename)    
        filename = "PersonalHolidays.txt"    # load file of personal birthdays, anniversaries and misc. days of importance
        DSM.load_monthly_comments(filename)

    def load_monthly_comments(filename):
        Holidays = []
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                Holidays = eval(f.read())
                for holiday in Holidays:
                    if MV.monthObj[holiday[0]-1].mthcomments[holiday[1]-1] == "":
                        MV.monthObj[holiday[0]-1].mthcomments[holiday[1]-1] = holiday[2]
                    else:
                        MV.monthObj[holiday[0]-1].mthcomments[holiday[1]-1] += "  " + holiday[2]

               
    def do_all_rectangles(screen):
        Rect.do_rects(screen, *RECT1, RECT1[2], 7)    # left side small calendar rectangles
        Rect.do_rects(screen, *RECT2, RECT2[2], 7)    # right side small calendar rectangles
        Rect.do_rects(screen, *RECT3, RECT3[2], 7)    # day of week headings
        Rect.do_rects(screen, *RECT4, 595, 2)         # small calendar headings
        Rect.do_rect(screen, *RECT5)                  # Month and year rectangle
        Rect.do_rect(screen, *RECT6)                  # main body of calendar rectangle
        pygame.draw.rect(screen, BLACK, (45, 43, 833, 620), 2)  # for looks
        
    def do_all_texts(screen, mth, yr):      
        if MV.month==0:
            Text.do_text(screen, MONTH_STRINGS[mth] + "  " + str(yr-1), 45, 39, 238, 25, BLACK, font14)
        else:    
            Text.do_text(screen, MONTH_STRINGS[mth] + "  " + str(yr), 45, 39, 238, 25, BLACK, font14)   # upper left calendar title
        if MV.month==11:
            Text.do_text(screen, MONTH_STRINGS[mth+2] + "  " + str(yr+1), 640, 39, 238, 25, BLACK, font14)
        else:    
            Text.do_text(screen, MONTH_STRINGS[mth+2] + "  " + str(yr), 640, 39, 238, 25, BLACK, font14)    # upper right calendar title
        [Text.do_text(screen, WEEK_STRINGS_LONG[i], 45 + i * 119, 150, 119, 25, BLACK, font18)
        for i in range(7)]                       # display main body column titles
        [Text.do_text(screen, WEEK_STRINGS_SHORT[j], 45 + i * 595 + j * 34, 64, 34, 13, BLACK, font14)    
        for i in range(2) for j in range(7)]     # display small cal headings
        
    def do_small_calendar_month(screen, stday, dsinmo, x):    # draws small calendars of previous month and next month
        ctr=stday
        for i in range(dsinmo):
            Text.do_text(screen, DAY_NUMBERS[i], x+ctr%7*34, 77+ctr//7*12, 34, 13, BLACK, font14)
            ctr+=1
            
    def do_small_calendar(screen, m):
        if MV.month == 0:
            temp = calendar.monthrange(MV.year-1, 12) # sets up December of previous year
            stdy = (temp[0]+1)%7
            dsinmo = 31
        else:
            stdy = MV.monthObj[m-1].stday               # otherwise sets up previous month
            dsinmo = MV.monthObj[m-1].dysinmth
        DSM.do_small_calendar_month(screen, stdy, dsinmo, 45)    
        if MV.month == 11:
            temp = calendar.monthrange(MV.year+1, 1)  # sets up January of next year
            stdy = (temp[0]+1)%7
            dsinmo = 31
        else:
            stdy = MV.monthObj[m+1].stday               # otherwise sets up next month
            dsinmo = MV.monthObj[m+1].dysinmth
        DSM.do_small_calendar_month(screen, stdy, dsinmo, 640)
         
    def month_text_boxes(screen):     # defines all text boxes and buttons
        def output_month():
            if(textbox.getText()).isdigit():
                if(int(textbox.getText())) >= 1 and (int(textbox.getText())) <= 12:
                    MV.month = int(textbox.getText()) - 1
            
        def output_year():
            if(textbox2.getText()).isdigit():
                if(int(textbox2.getText())) >= 1000:
                    MV.year = int(textbox2.getText())
                    DSM.initialize_month(MV.year)
            
        def go_ahead():
            MV.month += 1
            if MV.month == 12:
                MV.month = 0
                MV.year += 1
                DSM.initialize_month(MV.year)          
        
        def go_back():
            MV.month -= 1
            if MV.month < 0:
                MV.month = 11
                MV.year -= 1
                DSM.initialize_month(MV.year)
        
        global textbox       
        textbox = TextBox(screen, 114, 673, 33, 25, colour=(TAN),
                  font = font25, onSubmit=output_month, borderThickness=3)
            
        global textbox2                            
        textbox2 = TextBox(screen, 228, 673, 50, 25, colour=(TAN),
                   font = font25, onSubmit=output_year, borderThickness=3)
            
        global button
        button = Button(screen, 850, 0, 40, 40, text = '+', font=font26b, margin=10,
            inactiveColour=(255, 255, 200), hoverColour=(255, 100, 255),
            pressedColour=(0, 200, 20), radius=20, onClick=lambda: go_ahead())
            
        global button2
        button2 = Button(screen, 800, 0, 40, 40, text = '-', font=font26b, margin=10,
            inactiveColour=(255, 255, 200), hoverColour=(255, 100, 255),
            pressedColour=(0, 200, 20), radius=20, onClick=lambda: go_back())             
    
async def main():
    DSM.initialize_month(MV.year)
    DSM.month_text_boxes(screen)
    show_text_boxes = True
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:            # up arrow toggles showing of text boxes
                    show_text_boxes = not show_text_boxes
                if event.key == pygame.K_DOWN:          # down arrow saves screenshot as png file
                    pygame.image.save(screen, datetime.now().strftime("MonthlyCalendar-%m-%d-%y-%H-%M-%S")+".png")
        screen.fill(WHITE)  #clear background
        pygame.display.set_caption("Monthly Calendar")      #draw scene
        Text.do_text(screen, MV.monthObj[MV.month].name, 283, 16, 357, 40, COLOURS[MV.month], font55b)
             # display current Month
        Text.do_text(screen, str(MV.year), 283, 79, 357, 35, COLOURS[MV.month], font55b)
               # display current year
        DSM.do_all_rectangles(screen)
        DSM.do_all_texts(screen, MV.month, MV.year)
        DSM.do_small_calendar(screen, MV.month)
        if show_text_boxes:
            pygame_widgets.update(events)      # text boxes can be turned off with up arrow
            Text.do_text(screen, "MONTH:", 34, 667, 80, 25, BLACK, font16)
            Text.do_text(screen, "YEAR:", 150, 667, 100, 25, BLACK, font16)
            pygame.draw.circle(screen, BLACK, (870, 20), 20, 3)     # for looks
            pygame.draw.circle(screen, BLACK, (820, 20), 20, 3)
        for i in range(MV.monthObj[MV.month].dysinmth):
            Rect.do_rect(screen, 45, 183, MV.monthObj[MV.month].stday * 119, MV.monthObj[MV.month].yoffset)  \
                # cleans up left side of top row
            Rect.do_rect(screen, MV.monthObj[MV.month].days[i].x, MV.monthObj[MV.month].days[i].y,
                          119, MV.monthObj[MV.month].yoffset)   # big rectangle
            Rect.do_rect(screen, MV.monthObj[MV.month].days[i].x, MV.monthObj[MV.month].days[i].y, 30, 30)    # small rectangle             
            Text.do_text(screen, DAY_NUMBERS[i], MV.monthObj[MV.month].days[i].x, MV.monthObj[MV.month].days[i].y-9, 30, 22, BLACK, font24)   # number in small rectangle
            value = MV.monthObj[MV.month].mthcomments[i]       # if there is a comment in the mthcomments list, then wordwrap it
            if value != '':
                wrapper = textwrap.TextWrapper(width = 14)    
                word_list=wrapper.wrap(text=value)
                ctr2 = 0
                for line in word_list:
                    Text.do_text(screen, line, MV.monthObj[MV.month].days[i].x, 7+MV.monthObj[MV.month].days[i].y+(ctr2*13),
                                  119, 50, BLACK, font13r) # display it to screen
                    ctr2 += 1                             # one line at a time
            temp2 = MV.monthObj[MV.month].yoffset                                                                
            temp3 = MV.monthObj[MV.month].dysinmth-1
            Rect.do_rect(screen, MV.monthObj[MV.month].days[temp3].x+119, MV.monthObj[MV.month].days[temp3].y,
                          (6-(MV.monthObj[MV.month].days[temp3].x-45)//119)*119, temp2)                
                           # above cleans up right side of bottom row     
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())                     
           
       
    




