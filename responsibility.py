
import ipy_autoreload
ipy_autoreload.autoreload_enabled=True

from collections import defaultdict
from itertools import izip

class Node(object):
    def __init__(self,nid=0,x=0.0,y=0.0,crimerate=0.0,district=''):
        self.id=nid
        self.x=x
        self.y=y
        self.district=district
        self.crimerate=crimerate
        self.adjacent=[]
        
        
    def __repr__(self):
        return 'node %d ' \
               %(self.id)
    def __str__(self):
##        return '%d'%(self.id)
        return '%d (%f %f)'%(self.id,self.x,self.y)
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
        self.route=[]
        self.load=0

    def addResp(self,node):
        self.responsibility.append(node)
    def __repr__(self):
        return '%s with res %s' %(self.name,[str(r) for r in self.responsibility])
    
class Route(object):
    def __init__(self,fromN,toN,distance,length,averCrim):
        self.fromN=fromN
        self.toN=toN
        self.distance=distance
        self.length=length
        self.averCrim=averCrim
        self.police=None
    def __repr__(self):
        return 'Road: %d -> %d \n' %(self.fromN.id,self.toN.id)
    def __eq__(self,obj):
        return self.fromN.id == obj.fromN.id and self.toN.id == obj.toN.id


nodelist={}
nodeRelation={}
policelist={}
g_routes=[]
org_routes=[]
route_assign={}


n2p=defaultdict(list)
r2p=defaultdict(list)
##from collections import namedtuple
##Route=namedtuple('Route','fromN toN averCrim length distance')

RANGE=30
DIR='question2'
############
## read from file start
############
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
##            print items
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
            if getNode(fromN) is None or getNode(toN) is None:
                continue
            if fromN<toN:
                org_routes.append((getNode(fromN),getNode(toN)))
            else:
                org_routes.append((getNode(toN),getNode(fromN)))
            
                
                
                
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
    """
        construct policestation list from file
    """
    with open(filename,'r') as f:
        for l in f.readlines():
            items=l.split()
##            print items
            name=items[0]
            nodeNum=int(items[1])
            policelist[name]=PoliceStation(name,nodelist[nodeNum])

############
## read from file end
############

            
############
## responsibility assigment start
############            
def getNode(nid):
    """
        get node from nodelist according to id
    """
    try:
        n=nodelist[nid]    
        return n
    except:
        print 'node %d not found' %nid
        return None

def searchResponsibility():
    """
        search for the responsibility range for each police station
        
    """
    for p in policelist.values():
        print 'considering police %s at node %d' %(p.name,p.node.id)
        reslist=[]
        route=[]
        traverse(p.node,0,reslist,p.node,p.node,route=route)
        p.responsibility=reslist
        p.route=route
        for r in p.route:
            r.police=p
        print 'responsibility',[a.id for a in reslist]
        
def traverse(node,distanceAccum,reslist,prenode,startnode,route):
    
    def addnode():
        print 'add %d as responsibility' %adj.id
        reslist.append(adj)
        print 'add route from node %d to node %d' %(node.id,adj.id)
        #make fromN's id smaller than adj's id
        if node.id<adj.id:                
            r=Route(fromN=node,toN=adj,\
                           averCrim=(float(node.crimerate)+float(adj.crimerate))/2,\
                           distance=(distanceAccum+distance),\
                           length=node.getDistanceTo(adj)
                           )
        else:
            r=Route(fromN=adj,toN=node,\
                           averCrim=(float(node.crimerate)+float(adj.crimerate))/2,\
                           distance=(distanceAccum+distance),\
                           length=node.getDistanceTo(adj)
                           )                
            
        route.append(r)                                                                       
        
        traverse(adj,distanceAccum+distance,reslist,node,startnode,route)
        
    #exclude start node(the station)
    #and the previous traversed node
    s1=set(node.adjacent)
    s2=set([prenode])
    adjacents=list(s1-s2)
##    print 'filtered adjacents',[a.id for a in adjacents]
    
    for adj in adjacents:

        distance=node.getDistanceTo(adj)
        print 'distance from %d(%.1f,%.1f) to %d(%.1f,%.1f) is %.1f' \
              %(node.id,node.x,node.y,adj.id,adj.x,adj.y,distance)
        print 'accumulate distance %.1f' %(distanceAccum+distance )
        
        if prenode is startnode:
            #if the adj is adjacent to the start node
            #add it unconditionally
            addnode()
            continue
        if adj is startnode:
            print 'it is a loop!'
            #prevent loop
            continue
        
        if distanceAccum+distance <= RANGE:
            addnode()           
def transformN_R2P():
    """
        transform
        from
            police station to res points
            
        to
            res point to police stations
        from
            police station to route
        to
            route to police station
    """
    
           
        
    for p in policelist.values():
        
        
        for n,r in izip(p.responsibility,p.route):            
            n2p[n].append(p)
            r2p[(r.fromN,r.toN)].append(r)
            
        

    
        
def determin_min_route():
    """
        determin the min police station for each route from the candidates
    """
    #clear policelist in order to receive updated list
    for p in policelist.values():        
        p.route=[]
        
    for k,routes in r2p.items():
        route=min(routes,key=lambda p:p.distance)
        
        route_assign[route]=route.police

        #add this route to the winning police
        route.police.route.append(route)

############
## responsibility assigment end
############     


############
## utility section start
############        
def init():
    import os
    nodelist={}
    nodeRelation={}
    policelist={}
    generateNodes(os.path.join(DIR,'node.dat'))
    generateNodeRelation(os.path.join(DIR,'route.dat'))
    assignRelationToNode()
    generatePoliceStation(os.path.join(DIR,'police.dat'))


        
def assign_responsibilities():
    """
        initialize data from file
        and assign responsibilities to police
    """
    init()
    
    searchResponsibility()
    transformN_R2P()
    determin_min_route()
      

def getUnassignedRoads():
    assigned=[(r.fromN,r.toN) for r in route_assign.keys()]
    print 'assigned:',len(assigned)
    print 'total:',len(org_routes)
    un_ass=set(org_routes)-set(assigned)
    print len(un_ass),'left'
    return un_ass

def getAssignedRoads():    
    return [(r.fromN,r.toN) for r in route_assign.keys()]

def getRoadLoad(roadlist):
    
    
    load_by_area=defaultdict(float)
    count_by_area=defaultdict(float)
    dis_vec=[f.getDistanceTo(t) for f,t in roadlist]
    crim_vec=[(f.crimerate+t.crimerate)/2 for f,t in roadlist]
    
    maxdis=max(dis_vec)
    mindis=min(dis_vec)
    maxcrim=max(crim_vec)
    mincrim=min(crim_vec)

    dis_std =lambda s:(s-mindis)/(maxdis-mindis)
    crim_std =lambda s:(s-mincrim)/(maxcrim-mincrim)

    loadfunc=lambda dis,crim: dis*crim
    for f,t in roadlist:
        load=loadfunc(dis_std(f.getDistanceTo(t)),crim_std(f.crimerate+t.crimerate))
        if f.district is t.district:            
            load_by_area[f.district]+=load
            count_by_area[f.district]+=1
        else:
            load_by_area[f.district]+=load/2
            count_by_area[f.district]+=.5
            load_by_area[t.district]+=load/2
            count_by_area[t.district]+=.5
    for k,v in load_by_area.items():
        print k,v
        
    for k,v in count_by_area.items():
        print k,v
    
############
## utility section end
############        

##########
##print section start
##########             
def print_node_list():
    for n in nodelist.values():
        print n
def print_police_route():
    for p in policelist.values():
        print 'police %s(node %d) regulates roads:' %(p.name,p.node.id)
        
        for r in p.route:
         print 'from node %d to node %d(road length %f,distance %.4f and average crime rate %.4f)' \
              %(r.fromN.id,r.toN.id,r.length,r.distance,r.averCrim)

def print_n2p():
    for k,plist in n2p.items():
        print k,[p.name for p in plist]
        
def print_r2p():
    for k,plist in r2p.items():
        print k,[p.police.name for p in plist]

def print_route_assign():
    
    for r,p in route_assign.items():
        print "%s %s %s" %(r.fromN,r.toN,p.name)

##########
## print section end
##########             
        

    
      

        


##########
## write to file section start
##########    
def write_road_assignment_2file():
    with open('route_assign.csv','w') as f:
        for r,p in route_assign.items():           
            string="%d,%d,%s,%.5f,%.3f \n" \
                    %(r.fromN.id,r.toN.id,p.name,r.distance,r.averCrim)            
            f.write(string)

##########
## write to file section end
##########
                
def cal_standardized_sum():
    
    assign_responsibilities()
    dis_vec=[r.distance for r in g_routes]


    
    
    determin_min_route()
    print_route_assign()

    len_key=lambda r:r.length
    crim_key=lambda c:c.averCrim
    
    maxlen=max(route_assign.keys(),key=len_key).length
    minlen=min(route_assign.keys(),key=len_key).length

    maxcrim=max(route_assign.keys(),key=crim_key).averCrim    
    mincrim=min(route_assign.keys(),key=crim_key).averCrim
    
    print "maxlen:%(maxlen)f  minlen:%(minlen)f maxcrim:%(maxcrim)f mincrim:%(mincrim)f"    %locals()

    len_std =lambda s:(s-minlen)/(maxlen-minlen)
    crim_std =lambda s:(s-mincrim)/(maxcrim-mincrim)

    for r,p in route_assign.items():
        p.load+=len_std(r.length)*crim_std(r.averCrim)

    from collections import namedtuple
    PoliceLoad=namedtuple('PoliceLoad','name load')
    policeloadlist=[]
    for p in policelist.viewvalues():
         policeloadlist.append(PoliceLoad(name=p.name,load=p.load))
    policeloadlist.sort(key=lambda pl: pl.load,reverse=True)
    
    with open('load.dat','w') as f:
        for pl in policeloadlist:
            f.write("%s %f \n" %(pl.name,pl.load))
        

##########
##plot  start
##########     
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
def plot_original():
    """
        plot the original figure
        without any manipulation
    """
    xlist=[n.x for n in nodelist.values()]
    ylist=[n.y for n in nodelist.values()]
    plt.scatter(xlist,ylist,s=10)
    
    for n in nodelist.values():
        plt.text(n.x+1, n.y+1, '%d' %n.id,fontsize=10)
    plt.hold(True)
    
def plot_route():
    """
        plot the original route
        without any manipulation
    """    
    colorMap={'A':'r','B':'y','C':'c','D':'y','E':'b','F':'y'}
    for f,t in org_routes:
        
        plt.plot([f.x,t.x],[f.y,t.y],color=colorMap[f.district])
    
    plt.hold(True)
def plot_unassgined():
    for f,t in getUnassignedRoads():
        plt.plot([f.x,t.x],[f.y,t.y],color='b',linewidth=5)
    plt.hold(True)
def plot_assigned():
    for p in policelist.values():
        import random
        color=random.choice(['b','r','r','c','m','y','k'])
        for r in p.route:
             plt.plot([r.fromN.x,r.toN.x],[r.fromN.y,r.toN.y],color=color)           
    plt.hold(True)    
def plot_police():
    x=[p.node.x for p in policelist.values()]
    y=[p.node.y for p in policelist.values()]
    
    plt.scatter(x,y,s=40,c='r')
    for p in policelist.values():
        plt.text(p.node.x,p.node.y,p.name)
    plt.hold(True)
def plot_summary():
    
    plot_original()
    plot_route()
    plot_police()
    plot_unassgined()
    plot_assigned()
    plt.hold(False)
    plt.show()
def plot_escape(route):
    plot_original()
    plot_route()
    plot_police()
    for r in route:
        plt.plot([r.fromN.x,r.toN.x],[r.fromN.y,r.toN.y],linewidth=3,color='b')
        
    plt.scatter([getNode(32).x],[getNode(32).y],c='g',s=120)
    
    plt.hold(False)
    plt.show()

##########
##plot  end
##########           

def distance_sum_by_area():
    dis_sum=defaultdict(int)
    for r in org_routes:
        if r[0].district is r[1].district:
            dis_sum[r[0].district]+=r[0].getDistanceTo(r[1])
        else:
            distance=r[0].getDistanceTo(r[1])/2
            dis_sum[r[0].district]+=distance
            dis_sum[r[1].district]+=distance
    with open('distance_sum_by_area.csv','w') as f:
        for d,l in dis_sum.items():
            f.write("%s,%.4f \n" %(d,l))
    return dis_sum
def assigned_distance_sum_by_area():
    dis_sum=defaultdict(int)
    for r in route_assign:
        distance=r.toN.getDistanceTo(r.fromN)
        if r.fromN.district is r.toN.district:
            dis_sum[r.fromN.district]+=distance
        else:            
            dis_sum[r.fromN.district]+=distance
            dis_sum[r.toN.district]+=distance
    with open('assigned_distance_sum_by_area.csv','w') as f:
        for d,l in dis_sum.items():
            f.write("%s,%.4f \n" %(d,l))
    return dis_sum
def get_coverage_ratio():
    total=distance_sum_by_area()
    assigned=assigned_distance_sum_by_area()
    with open('coverage_ratio.csv','w') as f:
        for a,t in izip(assigned.items(),total.items()):
            f.write('%s,%.5f \n' %(a[0],a[1]/t[1]))


def escape(node,distanceAccum,prenode,prenodelist,startnode,route,lifedistance):
    
    def addnode():
        print 'add route from node %d to node %d' %(node.id,adj.id)
        #make fromN's id smaller than adj's id

        r=Route(fromN=node,toN=adj,\
                       averCrim=(float(node.crimerate)+float(adj.crimerate))/2,\
                       distance=(distanceAccum+distance),\
                       length=node.getDistanceTo(adj)
                       )                
        #update the trace
        route.append(r)                                                                       
        prenodelist.append(node)
        escape(adj,distanceAccum+distance,prenode,prenodelist,startnode,route,lifedistance)
        
    #exclude start node(the station)
    #and the previous traversed node
    s1=set(node.adjacent)
    s2=set([prenode])
    adjacents=list(s1-s2)
##    print 'filtered adjacents',[a.id for a in adjacents]
    
    for adj in adjacents:

        distance=node.getDistanceTo(adj)
        print 'distance from %d(%.1f,%.1f) to %d(%.1f,%.1f) is %.1f' \
              %(node.id,node.x,node.y,adj.id,adj.x,adj.y,distance)
        print 'accumulate distance %.1f' %(distanceAccum+distance )
        

        if adj is startnode:
            print 'it is a loop!'
            #prevent loop
            continue
        if adj in prenodelist:
            continue
        if distanceAccum+distance <= lifedistance:
            addnode()
        else:
            #add the "uncompleted" road
            remaindis=lifedistance-distanceAccum
            ratio=remaindis/node.getDistanceTo(adj)
            new_x=node.x+(adj.x-node.x)*ratio
            new_y=node.y+(adj.y-node.y)*ratio
            adj=Node(x=new_x,y=new_y)
            addnode()

        #pop the node
        prenodelist.pop(prenodelist.index(node))
            
def capture():
    
    lifedistance=120

    
    crimenode=getNode(32)

    

    reslist=[]
    route=[]
    
    escape(crimenode,0,prenode=crimenode,prenodelist=[crimenode],startnode=crimenode,route=route,lifedistance=lifedistance)
    plot_escape(route)
    
    
if __name__=='__main__':
    assign_responsibilities()
    
##    getUnassignedRoadLoad()
    
##    plot_summary()
    capture()
    plt.hold(False)
##    roadlist=getAssignedRoads()
##    getRoadLoad(roadlist)




