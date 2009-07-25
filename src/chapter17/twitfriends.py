import twitter
import re

from javax.swing import (JButton, JFrame, JLabel, JPanel, JPasswordField,
        JTextField, SwingConstants, WindowConstants)
from java.awt import GridLayout

class JyTwitter(object):
    def execute(self,event):
        self.api = twitter.Api(self.usernameField.text, self.passwordField.text)
        users = self.api.GetFriends()
        for u in users:
            self.makeButton(u.screen_name)

    def showTwitters(self, event):
        statuses = self.api.GetUserTimeline(user=event.actionCommand, count=10)
        if len(self.regexField.text) > 0:
            regex = re.compile(self.regexField.text)
        else:
            regex = re.compile(".")
        print "** ", statuses[0].user.screen_name, statuses[0].user.name, "**"
        for s in statuses:
            if regex.search(s.text) is not None:
                print s.user.screen_name, s.text, s.id, s.relative_created_at

    def makeButton(self, name):
        self.pnl.add(JButton(name, actionPerformed=self.showTwitters))
        self.frame.pack()
        self.frame.show()

    def __init__(self):
        self.frame = JFrame("Jython Twitter")
        self.frame.setSize(800, 150)
        self.frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
 
        self.pnl = JPanel(GridLayout(0,2))
        self.frame.add(self.pnl)

        self.usernameField = JTextField('',15)
        self.pnl.add(JLabel("username:", SwingConstants.RIGHT))
        self.pnl.add(self.usernameField)

        self.passwordField = JPasswordField('', 15)
        self.pnl.add(JLabel("password:", SwingConstants.RIGHT))
        self.pnl.add(self.passwordField)

        executeButton = JButton('Friends',actionPerformed=self.execute)
        self.pnl.add(executeButton)

        self.regexField = JTextField('',15)
        self.pnl.add(self.regexField)

        self.frame.pack()
        self.frame.visible = True
 
if __name__ == '__main__':
    JyTwitter()
