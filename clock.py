import datetime
class DigitalClock:
    def __init__(self,clock=True, date=False, stopwatch=False, timer=False):
        self.clock=clock
        self.date=date
        self.stopwatch=stopwatch
        self.timer=timer
        self.time=datetime.datetime.now()
        self.month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31} 
        # stopwatch related
        self.s_state="stopped"
        self.s_laps=0
        self.s_startTime=datetime.datetime.now()
        self.s_stopWatchTime=datetime.timedelta(microseconds=0)
        self.s_hours=0
        self.s_minutes=0
        self.s_seconds=0 
        # timer
        self.t_runnng=False
        self.t_timeSaved=datetime.datetime.now()
        self.t_endTime=datetime.datetime.now()
        self.t_hours=0
        self.t_minutes=0
                     
    def save_SW_time(self, addTime=False):
        delta=datetime.datetime.now()-self.s_startTime
        if addTime==True:
            self.s_hours+=delta.seconds//3600
            self.s_minutes+=(delta.seconds%3600)//60
            if self.s_minutes>=60:
                self.s_minutes-=60
                self.s_hours+=1
            self.s_seconds+=delta.seconds-self.s_hours*3600-self.s_minutes*60
            if self.s_seconds>=60:
                self.s_seconds-=60
                self.s_minutes+=1
                if self.s_minutes>=60:
                    self.s_minutes-=60
                    self.s_hours+=1
        else:
            self.s_hours=delta.seconds//3600
            self.s_minutes=(delta.seconds%3600)//60
            if self.s_minutes>=60:
                self.s_minutes-=60
                self.s_hours+=1
            self.s_seconds=delta.seconds-self.s_hours*3600-self.s_minutes*60
            if self.s_seconds>=60:
                self.s_seconds-=60
                self.s_minutes+=1
                if self.s_minutes>=60:
                    self.s_minutes-=60
                    self.s_hours+=1


    def A(self, longPress=False):
        if self.clock==True:
            if longPress==True and self.time.hour<=18:
                self.time=self.time.replace(hour=self.time.hour+5)
            elif longPress==True:
                newHour=(self.time.hour+5)-24
                print(newHour)
                self.time=self.time.replace(hour=newHour)
            elif self.time.hour==23:
                self.time=self.time.replace(hour=0)
            else:
                self.time=self.time.replace(hour=self.time.hour+1)
        elif self.date==True:
            if self.time.day==self.month[self.time.month]:
                self.time=self.time.replace(day=1)
            else:
                self.time=self.time.replace(day=self.time.day+1)
        elif self.stopwatch==True:
            if self.s_state=="running":
                self.s_state="paused"                       
                self.save_SW_time(True)
            else:
                self.s_state="running"
                self.s_startTime=datetime.datetime.now()
        elif self.timer==True:
            if self.t_hours<24:
                self.t_hours+=1

            

    def B(self, longPress=False):
        if self.clock==True:
            if self.time.minute==59:
                self.time=self.time.replace(minute=0)
            else:
                self.time=self.time.replace(minute=self.time.minute+1)
        elif self.date==True:
                if self.time.month==12:
                    self.time=self.time.replace(month=1)
                else:
                    self.time=self.time.replace(month=self.time.month+1)
        elif self.stopwatch==True:
            if longPress==True:
                self.s_laps=0
            elif self.s_laps<10:
                self.s_laps+=1
            else:
                print("too many laps")
        elif self.timer==True:
            if self.t_minutes<59:
                self.t_minutes+=1
            else:
                self.t_minutes=0
                self.A()


    def C(self):
        if self.clock==True:
            if self.time.second==59:
                self.time=self.time.replace(second=0)
            else:
                self.time=self.time.replace(second=self.time.second+1)
        elif self.date==True:
            if self.time.year==2500:
                self.time=self.time.replace(year=1900)
            else:
                self.time=self.time.replace(year=self.time.year+1)
        elif self.stopwatch==True:
            if self.s_state=="running":
                self.s_state="stopped"

            self.s_hours=0
            self.s_minutes=0
            self.s_seconds=0
        elif self.timer==True:
            if self.t_runnng==True:
                self.t_runnng=False
                delta=self.t_endTime-datetime.datetime.now()
                self.t_hours=delta.seconds//3600
                self.t_minutes=(delta.seconds%3600)//60
            else:
                self.t_runnng=True
                timerTime = datetime.timedelta(hours=self.t_hours, minutes=self.t_minutes) 
                self.t_endTime=datetime.datetime.now()+timerTime
                self.display()
            





    def S(self):
        if self.clock==True:
            self.clock=False
            self.date=True
        elif self.date==True:
            self.date=False
            self.stopwatch=True
        elif self.stopwatch==True:
            self.stopwatch=False
            self.timer=True
        elif self.timer==True:
            self.timer=False
            self.clock=True
    
    def display(self):
        if self.clock==True:
            print(f"Time - {self.time.strftime('%H:%M:%S')}*")
        elif self.date==True:
            print(f"Date - {self.time.strftime('%d/%m/%Y')}*")
        elif self.stopwatch==True:
            if self.s_state=="running":
                self.save_SW_time(False)
            displayHours=self.s_hours
            if displayHours<10:
                displayHours="0"+str(displayHours)
            displayMin=self.s_minutes
            if displayMin<10:
                displayMin="0"+str(displayMin)
            displaySec=self.s_seconds
            if displaySec<10:
                displaySec="0"+str(displaySec)

            print(f"Stopwatch - {self.s_laps}L-{displayHours}:{displayMin}:{displaySec}*")
        elif self.timer==True:
            delta=self.t_endTime-datetime.datetime.now()
            self.t_hours=delta.seconds//3600
            self.t_minutes=(delta.seconds%3600)//60
            t_seconds=delta.seconds-self.t_hours*3600-self.t_minutes*60
            displayHours=self.t_hours
            if displayHours<10:
                displayHours="0"+str(displayHours)
            displayMin=self.t_minutes
            if displayMin<10:
                displayMin="0"+str(displayMin)
            displaySec=t_seconds
            if displaySec<10:
                displaySec="0"+str(displaySec)
            print(f"Timer - {displayHours}:{displayMin}:{displaySec}.00*")

