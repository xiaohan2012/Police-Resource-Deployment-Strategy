from classes import *

import ipy_autoreload
ipy_autoreload.autoreload_enabled=True


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
