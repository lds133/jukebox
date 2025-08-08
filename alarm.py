import datetime


class Alarm():


    class Entry():
        def __init__(self, keynone:int, keyalarm:int, hours:int, mins:int ):
            self.KEYNONE = keynone
            self.KEYALARM = keyalarm
            self.H = hours
            self.M = mins
            self.lastchecktime = None
            self.Check()
            
        def Check(self):
            now = datetime.datetime.now()
            alarmsignaled = False

            if (self.lastchecktime != None):
                chk = self.lastchecktime
                alr1 = datetime.datetime(chk.year,chk.month,chk.day,self.H,self.M,0)
                alr2 = datetime.datetime(now.year,now.month,now.day,self.H,self.M,0)
                if (alr1>=chk) and (alr1<now):
                    alarmsignaled = True
                if (alr2>=chk) and (alr2<now):
                    alarmsignaled = True
                #print("Check ",chk," - ",now, "   ",alr1," , ",alr2, " -> ",alarmsignaled)

            self.lastchecktime = now
            return self.KEYALARM if alarmsignaled else self.KEYNONE
            
            

    def __init__(self, keynone:int ):
        self.alarms = []
        self.keynone = keynone
        
    def Add(self, key:int, hours:int, mins:int):
        self.alarms.append ( Alarm.Entry(self.keynone,key,hours,mins) )

    def Check(self)->int:
        for a in self.alarms:
            key = a.Check()
            if (key!=self.keynone):
                return key
        return self.keynone