from javax.swing import JFrame, JLabel
from hello import register_ui

@register_ui('window')
def show_message_as_window(msg):
    frame = JFrame(msg,
                   defaultCloseOperation=JFrame.EXIT_ON_CLOSE,
                   size=(100, 100),
                   visible=True)
    frame.contentPane.add(JLabel(msg))
    