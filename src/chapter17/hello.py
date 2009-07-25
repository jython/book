from javax.swing import JButton, JFrame

frame = JFrame('Hello, Jython!',
          defaultCloseOperation=JFrame.EXIT_ON_CLOSE,
          size=(300, 300))

def change_text(event):
    print 'clicked!'

button = JButton('Click Me!', actionPerformed=change_text)
frame.add(button)
frame.visible = True
