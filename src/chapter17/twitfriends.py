# -*- coding: utf-8 -*-
import twitter
import re

from javax.swing import *
from java.lang import *
from java.awt import *
from java.net import URL
from java.lang import Runnable

class JyTwitter(object):
    def __init__(self):
        self.frame = JFrame("Jython Twitter")
        self.frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
 
        self.loginPanel = JPanel(GridLayout(0,2))
        self.frame.add(self.loginPanel)

        self.usernameField = JTextField('',15)
        self.loginPanel.add(JLabel("username:", SwingConstants.RIGHT))
        self.loginPanel.add(self.usernameField)

        self.passwordField = JPasswordField('', 15)
        self.loginPanel.add(JLabel("password:", SwingConstants.RIGHT))
        self.loginPanel.add(self.passwordField)

        self.loginButton = JButton('Log in',actionPerformed=self.login)
        self.loginPanel.add(self.loginButton)

        self.message = JLabel("Please Log in")
        self.loginPanel.add(self.message)

        self.frame.pack()
        self.frame.visible = True

    def login(self,event):
        self.message.text = "Attempting to Log in..."
        self.frame.show()
        username = self.usernameField.text
        try:
            self.api = twitter.Api(username, self.passwordField.text)
            self.frame.size = 300, 400
            self.timeline(username)
            self.loginPanel.visible = False
            self.message.text = "Logged in"
        except:
            self.message.text = "Log in failed."
            raise
        self.frame.size = 300, 400
        self.frame.show()

    def timeline(self, username):
        timeline = self.api.GetFriendsTimeline(username)
        self.resultPanel = JPanel()
        self.resultPanel.layout = BoxLayout(self.resultPanel, BoxLayout.Y_AXIS)
        for s in timeline:
            self.makeLabel(s)

        scrollpane = JScrollPane(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
                                 JScrollPane.HORIZONTAL_SCROLLBAR_NEVER)
        scrollpane.preferredSize = 300, 300
        scrollpane.viewport.view = self.resultPanel

        self.frame.add(scrollpane)

    def makeLabel(self, status):
        user = status.user
        p = JPanel()
        p.add(JLabel(ImageIcon(URL(user.profile_image_url))))
        p.add(JTextArea(text = status.text,
                        editable = False,
                        alignmentX = Component.LEFT_ALIGNMENT,
                        lineWrap = True,
                        size = (300, 30)
             ))
        self.resultPanel.add(p)
        print user.profile_image_url

if __name__ == '__main__':
    JyTwitter()
