

from javax.servlet.http import HttpServlet
from org.plyjy.interfaces import JythonServletInterface

class NewJythonServlet (JythonServletInterface, HttpServlet):
	def doGet(self,request,response):
		self.doPost (request,response)

	def doPost(self,request,response):
		toClient = response.getWriter()
		response.setContentType ("text/html")
		toClient.println ("<html><head><title>Jython Servlet Test Using Object Factory</title>" +
						  "<body><h1>Jython Servlet Test for GAE</h1></body></html>")

        def getServletInfo(self):
            return "Short Description"