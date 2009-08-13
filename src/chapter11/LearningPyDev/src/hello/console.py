from hello import register_ui

@register_ui('console')
def print_message(msg):
    print msg
