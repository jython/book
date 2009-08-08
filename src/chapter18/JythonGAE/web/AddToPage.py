#######################################################################
#  add_to_page.py
#
#  Simple servlet that takes some text from a web page and redisplays
#  it.
#######################################################################

from javax.servlet.http import HttpServlet
from org.plyjy.interfaces import JythonServletInterface

class AddToPage(JythonServletInterface, HttpServlet):


    def doGet(self, request, response):
        self.doPost(request, response)

    def doPost(self, request, response):
        toClient = response.getWriter()
        addtext = request.getParameter("p")
        if not addtext:
            addtext = ""

        request.setAttribute("page_text", addtext)

        dispatcher = request.getRequestDispatcher("testJython.jsp")
        dispatcher.forward(request, response)