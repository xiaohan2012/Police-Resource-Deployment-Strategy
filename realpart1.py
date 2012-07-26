
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
        return 'node id %d at x:%.1f y:%.1f with adjacent %s' \
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


nodelist={}
nodeRelation={}
policelist={}
RANGE=3


def generateNodes(filename):
    """
        read node data from file and generate node list
    """
    with open(filename,'r') as f:
        for l in f.readlines():        
            items=l.split()
            nid=int(items[0])
            x=float(items[1])
            y=float(items[2])
            district=items[3]
            crimerate=float(items[4])
            nodelist[nid]=Node(nid,x,y,crimerate,district)

def generateNodeRelation(filename):
    """
        read route data from file and generate node relation
    """    
    with open(filename,'r') as f:
        for l in f.readlines():
            items=l.split()
            print items
            fromN=int(items[0])
            toN=int(items[1])
            if nodeRelation.has_key(fromN):
                if getNode(toN):
                    nodeRelation[fromN].append(getNode(toN))                
            else:
                if getNode(toN):
                    nodeRelation[fromN]=[getNode(toN)]
                
            if nodeRelation.has_key(toN):
                if getNode(fromN):
                    nodeRelation[toN].append(getNode(fromN))
            else:                
                if getNode(fromN):
                    nodeRelation[toN]=[getNode(fromN)]                
                
                
def assignRelationToNode():
    """
        Assign node relation info to node
    """
    for fromN,tolist in nodeRelation.items():
        try:
            nodelist[fromN].adjacent=tolist
        except KeyError:
            pass

def generatePoliceStation(filename):
    with open(filename,'r') as f:
        for l in f.readlines():
            items=l.split()
            print items
            name=items[0]
            nodeNum=int(items[1])
            policelist[name]=PoliceStation(name,nodelist[nodeNum])

def getNode(nid):
    try:
        n=nodelist[nid]    
        return n
    except:
        print nid
        return None

def getResponsibility():
    for p in policelist.values():
        print 'considering police %s at node %d' %(p.name,p.node.id)
        reslist=[]
        traverse(p.node,0,reslist,None,p.node)
        p.responsibility=reslist
        print 'responsibility',[a.id for a in reslist]
        
def traverse(node,distanceAccum,reslist,prenode,startnode):
    #exclude start node(the station)
    #and the previous traversed node
    s1=set(node.adjacent)
    s2=set([prenode])
    adjacents=list(s1-s2)
    print 'filtered adjacents',[a.id for a in adjacents]
    for adj in adjacents:
        if adj is startnode:
            print 'it is a loop!'
            #prevent loop
            continue
        distance=node.getDistanceTo(adj)
        print 'distance from %d(%.1f,%.1f) to %d(%.1f,%.1f) is %.1f' \
              %(node.id,node.x,node.y,adj.id,adj.x,adj.y,distance)
        print 'accumulate distance %.1f' %(distanceAccum+distance )
        if distanceAccum+distance <= RANGE:            
            if adj not in reslist:
                print 'add %d as responsibility' %adj.id
                reslist.append(adj)
            traverse(adj,distanceAccum+distance,reslist,node,startnode)
        
    
def getResponsibility1():
    print policelist
    for p in policelist.values():
        stack=p.node.adjacent
        pathStack=[]
        stopTrace=[]
        distanceSum=0
        fromN=p.node
        pathStack.append(fromN)
        stopTrace.append(p.node)
        stopTrace.append(p.node.adjacent[0])
        print 'initializing police node %s(node %d)' %(p.name,p.node.id)
        print 'with adjacent %s' %p.node.getAdjacentNum()
        
        while stack:            
            
            toN=stack.pop()
            print 'poping node %d, the stack will be %s' %(toN.id,[i.id for i in stack])
            
            print 'the path:%s' %[i.id for i in pathStack]
            print 'stopTrace %s'  %[i.id for i in stopTrace]
            distance=fromN.getDistanceTo(toN)
            print 'from node %d to node %d is %f' %(fromN.id,toN.id,distance)
            
            distanceSum+=distance
            print 'the cumulative sum is %f' %distanceSum
            if distanceSum < RANGE:
                print 'Yes, it is. It is my responsibility to administer node %d' %toN.id
                p.addResp(toN)
                s1=set(toN.adjacent)
                s2=set([fromN])
                print 'extending %s into stack' %[i.id for i in list(s1.symmetric_difference(s2))]
                tail=list(s1.symmetric_difference(s2))
                stack.extend(tail)
                pathStack.append(toN)
                fromN=toN
                if tail:#if the current node is not none
                    stopTrace.append(tail[0])
                    continue
             
            print 'the path:%s' %[i.id for i in pathStack]
            print 'stopTrace %s'  %[i.id for i in stopTrace]
            if distanceSum< RANGE:
                #the toN has been appended
                pathStack.pop()
                
            while stopTrace[-1] is  toN:
                print 'node %d is end point' %toN.id
                stopTrace.pop()
                toN=pathStack.pop()
                
            print 'the path:%s' %[i.id for i in pathStack]
            print 'stopTrace %s'  %[i.id for i in stopTrace]                
            fromN=pathStack[-1]
            distanceSum-=distance
            print 'the stack will be %s' %[i.id for i in stack]

DIR='testsuite'
def init():
    nodelist={}
    nodeRelation={}
    policelist={}
    

def testGenerateNodes():
    import os
    init()
    generateNodes(os.path.join(DIR,'node.dat'))
    generateNodeRelation(os.path.join(DIR,'route.dat'))
    assignRelationToNode()
    generatePoliceStation(os.path.join(DIR,'police.dat'))
    for k,v in nodelist.items():
        print k,v
    for k,p in policelist.items():
        print k,p.node


def testGenerateAdjacent():
    generateNodeRelation()
    for n in nodeRelation.items():
        print n
        
def testGetDistanceTo():
    n1=Node(x=1,y=1)
    n2=Node(x=2,y=2)
    print n1.getDistanceTo(n2)

    

if __name__=='__main__':
    
    testGenerateNodes()

    print nodelist
    getResponsibility()
##    testGetDistanceTo()
                

