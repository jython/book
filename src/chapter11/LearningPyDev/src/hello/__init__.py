# -*- coding: utf-8 -*-
greetings = dict(en=u'Hello %s!',
                 es=u'Hola %s!',
                 fr=u'Bonjour %s!',
                 pt=u'Alò %s!')

class LanguageNotSupportedException(ValueError): 
    pass

class UINotSupportedExeption(ValueError):
    pass

uis = {}
def register_ui(ui_name):
    def decorator(f):
        uis[ui_name] = f
        return f
    return decorator

def message(ui, msg):
    '''
    Displays the message `msg` via the specified UI which has to be 
    previously registered.
    '''
    if ui in uis:
        uis[ui](msg)
    else:
        raise UINotSupportedExeption(ui)
    
def list_uis():
    return uis.keys()

def greet(name, lang, ui):
    '''
    Greets the person called `name` using the language `lang` via the 
    specified UI which has to be previously registered.
    '''
    if lang not in greetings:
        raise LanguageNotSupportedException(lang)
    message(ui, greetings[lang] % name)
