# http://mail.python.org/pipermail/python-dev/2008-January/076194.html 
# - a recipe of Guido van Rossum

def monkeypatch_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

# and a useful variant, with a good ugly name

def monkeypatch_method_if_not_set(cls):
    def decorator(func):
        if not hasattr(cls, func.__name__):
            setattr(cls, func.__name__, func)
        return func
    return decorator
