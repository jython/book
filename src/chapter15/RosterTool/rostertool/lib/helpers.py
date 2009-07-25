"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from routes import url_for, redirect_to
from webhelpers.html.tags import *
from webhelpers.pylonslib import Flash as _Flash

# Send alert messages back to the user
flash = _Flash()
