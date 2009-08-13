from com.sun.speech.freetts import VoiceManager, Voice
from hello import register_ui

@register_ui('speech')
def speech_message(msg): 
    voice = VoiceManager.getInstance().getVoice("kevin16")
    voice.allocate()
    voice.speak(msg)
    voice.deallocate()
