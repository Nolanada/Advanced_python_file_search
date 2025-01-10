class rectangle :
   # self.length=20
   # self.width=10
    def __init__(self,length=25,width=10 ):
        self.length=length
        self.width=width
    
    def findArea(self):
        Area=self.length*self.width
        print(Area)
rect=rectangle(5,3)
rect.findArea()
#self should be passed as parameter to a function thought in java it is no tthe same