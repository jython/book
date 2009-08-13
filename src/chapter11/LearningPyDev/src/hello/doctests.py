"""
>>> from hello import console
>>> console.print_message("testing")
testing
"""
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    

