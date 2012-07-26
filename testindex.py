class obj(object):
    def __init__(self,Id):
        self.id=Id
    def __cmp__(self,another):
        return self.id != another.id
    
class Route(object):
    def __init__(self,fromN,toN,distance,length,averCrim):
        self.fromN=fromN
        self.toN=toN
        self.distance=distance
        self.length=length
        self.averCrim=averCrim
    def __cmp__(self,obj):
        return self.fromN == obj.fromN and self.toN == obj.toN
    
def testset():
    l1=[]
    for i in xrange(3):
        l1.append(obj(i))
    
    l_obj1=l1[2]
    s1=set(l1)
    s2=set([l_obj1])
    print s1.symmetric_difference(s2)
if __name__=='__main__':
    r1=Route(1,2,None,None,None)
    r2=Route(1,2,None,None,None)
    print r1 == r2

    
