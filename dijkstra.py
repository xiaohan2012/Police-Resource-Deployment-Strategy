graph={}
def generateGraph(nodelist):
    for n in nodelist.values():
        for adj in n.adjacent:
            graph[(n.id,adj.id)]=n.getDistanceTo(adj)

 
def dijkstra(initP,nodelist,graph):
    visited=[initP]
    print 'visited',visited
    unvisited=list(set(nodelist)-set(visited))
    print 'unvisited',unvisited
    #0:previous node
    #1:distance
    from collections import namedtuple
    disAndPre=namedtuple('disAndPre',['dis','pre'])
    path={initP:disAndPre(dis=0,pre=initP)}
    from fpconst import PosInf
    
    toN=None
    fromN=None
    while unvisited:
        mindis=PosInf
        for v in visited:
            for u in unvisited:
##                print 'from node %d to node %d' %(v,u)
                try:
##                    print 'from original to node %d is %f' %(v,path[v].dis)
##                    print 'add %f' %graph[(v,u)]
                    
                    curdis=path[v].dis+graph[(v,u)]
##                    print 'yields %f' %curdis
                    
                    if mindis>curdis:
##                        print 'wow! new smallest, %f compared with %f' %(curdis,mindis)
                        fromN=v
                        toN=u
                        mindis=curdis                    
                except KeyError:
                    #the distance between v and u is infinite(unreachable)
                    #so, ignore it
##                    print 'find a infinite path'
                    pass
        path[toN]=disAndPre(dis=mindis,pre=fromN)
##        print 'finally add node %d to visited set' %toN
        visited.append(toN)
        del unvisited[unvisited.index(toN)]
##        print 'visited',visited
##        print 'unvisited',unvisited
##        print '-'*40
    shortestdis={}
    for to,p in path.items():
        shortestdis[(initP,to)]=p.dis
        
    return shortestdis
def postwork():
    from responsibility import *
    testGenerateNodes()
    generateGraph(nodelist)
    
    dijkstra(nodelist[1].id,\
             [k for k in nodelist.keys()],\
             graph)    
    
def inittest():
    nodelist=range(1,7)
    graph[(1,2)]=7
    graph[(1,3)]=9
    graph[(1,6)]=14
    graph[(2,3)]=10
    graph[(2,4)]=15
    graph[(3,4)]=11
    graph[(3,6)]=2
    graph[(5,6)]=9
    graph[(4,5)]=6

    for pair,dis in graph.items():
        graph[(pair[1],pair[0])]=dis

if __name__=='__main__':
    from responsibility import *
    testGenerateNodes()
    generateGraph(nodelist)
    nodeIdList=[n for n in nodelist]
    policeIdList=[p.node.id for p in policelist.values()]
    policeIdList.sort()
    targetroad=[int(k) for k in open('targetroad.dat','r').readlines()]

    matrix={}
    for pid in policeIdList:
        shortest=dijkstra(pid,nodeIdList,graph)
        for road in targetroad:
            matrix[(pid,road)]=shortest[pid,road]
    print len(matrix)
    with open('shortest_matrix.dat','w') as f:        
        f.write("\t".join([str(p) for p in policeIdList]))
        f.write("\n")
        for r_mat_id in xrange(len(targetroad)):
            f.write('%d \t' %targetroad[r_mat_id])
            for p_mat_id in xrange(len(policeIdList)):
                r_id=targetroad[r_mat_id]
                p_id=policeIdList[p_mat_id]
                distance=matrix[(p_id,r_id)]
                f.write('%.4f\t' %distance)
            f.write('\n')
                
            
    
        
    
    



