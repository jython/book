# JythonSimpleSwing.py
#
# This is the Jython Swing implementation for a simple interactive interpreter
# GUI.
#
# Author: J Juneau

import javax.swing as swing
import java.awt as awt
from java.io import PrintWriter
from org.python.util import PythonInterpreter
from JythonOutputStream import JythonOutputStream
from jythonswingapp.interfaces import JySwingType

class JythonSimpleSwing(JySwingType, object):
    def __init__(self):
        self.frame=swing.JFrame(title="Simple Jython Interpreter", size=(600,500))
        self.frame.defaultCloseOperation=swing.JFrame.EXIT_ON_CLOSE;
        self.frame.layout=awt.BorderLayout()
        self.panel1=swing.JPanel(awt.BorderLayout())
        self.panel2=swing.JPanel(awt.BorderLayout())


        self.title=swing.JLabel("Jython Code")
        self.title2 = swing.JLabel("Interpreter Output")
        self.button1=swing.JButton("Run", actionPerformed=self.printMessage)
        self.button2=swing.JButton("Clear Output", actionPerformed=self.clearMessage)

        self.buttonPane = swing.JPanel()
        self.buttonPane.layout = swing.BoxLayout(self.buttonPane, swing.BoxLayout.LINE_AXIS)
        self.buttonPane.border = swing.BorderFactory.createEmptyBorder(0, 10, 10, 10)
        self.buttonPane.add(swing.Box.createHorizontalGlue())
        self.buttonPane.add(self.button1)
        self.buttonPane.add(swing.Box.createRigidArea(awt.Dimension(10, 0)))
        self.buttonPane.add(self.button2)

        self.textField=swing.JTextArea(4,15)
        self.textField.lineWrap = True
        self.scrollPaneOne = swing.JScrollPane(self.textField)
        self.scrollPaneOne.verticalScrollBarPolicy = swing.JScrollPane.VERTICAL_SCROLLBAR_ALWAYS
        self.outputText=swing.JTextArea(4,15)
        self.outputText.lineWrap = True
        self.outputText.editable = False
        self.scrollPane2 = swing.JScrollPane(self.outputText)
        self.scrollPane2.verticalScrollBarPolicy = swing.JScrollPane.VERTICAL_SCROLLBAR_ALWAYS
        

        self.panel1.add(self.title, awt.BorderLayout.PAGE_START)
        self.panel1.add(self.scrollPaneOne, awt.BorderLayout.CENTER)
        self.panel2.add(self.title2, awt.BorderLayout.PAGE_START)
        self.panel2.add(self.scrollPane2, awt.BorderLayout.CENTER)

        self.splitPane = swing.JSplitPane(swing.JSplitPane.VERTICAL_SPLIT,
                         self.panel1, self.panel2)
        self.splitPane.oneTouchExpandable = True
        self.minimumSize = awt.Dimension(50, 100)
        self.panel1.minimumSize = self.minimumSize
        self.panel2.minimumSize = self.minimumSize

        self.frame.contentPane.add(self.splitPane, awt.BorderLayout.CENTER)
        self.frame.contentPane.add(self.buttonPane, awt.BorderLayout.PAGE_END)

    def start(self):
        self.frame.visible=1

    def printMessage(self,event):
        self.text = self.textField.getText()
        intrp = PythonInterpreter()
        self.interpreterOut = JythonOutputStream(self.outputText)
        try:
            intrp.setOut(self.interpreterOut)
            intrp.exec(self.text)
        except Exception, ex:
            print ex
            intrp.setErr(self.interpreterOut)

        
    def clearMessage(self, event):
        self.outputText.text = ""

