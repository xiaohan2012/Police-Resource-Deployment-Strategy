import ipy_autoreload
ipy_autoreload.autoreload_enabled=True
class Node(object):
    def __init__(self,nid=0,x=0.0,y=0.0,crimerate=0.0,district=''):
        self.id=nid
        self.x=x
        self.y=y
        self.district=district
        self.crimerate=crimerate
        self.adjacent=[]
        
    def __repr__(self):
        return 'node id %d at x:%.1f y:%.1f with adjacent %s ' \
               %(self.id,self.x,self.y,self.getAdjacentNum())
    def getAdjacentNum(self):
        return [n.id for n in self.adjacent]
    def getResponsibilityList(self):
        return [n.id for n in self.responsibility]
    def getDistanceTo(self,n):
        from math import sqrt
        return sqrt((self.x-n.x)**2+(self.y-n.y)**2)

class PoliceStation(object):
    def __init__(self,name,node):
        self.node=node
        self.name=name
        self.responsibility=[]
        
    def addResp(self,node):
        self.responsibility.append(node)
