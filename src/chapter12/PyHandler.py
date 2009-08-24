class PyHandler(DataHandler):                              
    def __init__(self, handler):                           
       self.handler = handler
       print 'Inside DataHandler'
    def getPyObject(self, set, col, datatype):             
        return self.handler.getPyObject(set, col, datatype)
    def getJDBCObject(self, object, datatype):             
        print "handling prepared statement"                
        return self.handler.getJDBCObject(object, datatype)
    def preExecute(self, stmt):
        print "calling pre-execute to alter behavior"
        return self.handler.preExecute(stmt)
