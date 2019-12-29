# The Jython Book

This is an open reference book on the Jython language, an implementation of Python implemented in, and highly interoperable with, Java. It is maintained as a reference to the current version of Jython (perhaps with a touch of lag).


## Project

This book is formatted for and available at https://jython.readthedocs.io/en/latest/

## License and Contributions

This book is licensed under CC-BY-SA http://creativecommons.org/licenses/by-sa/3.0/ . Contributions in the form of pull requests are welcome, and are covered by the same license under the "inbound=outbound" part of the github terms of service https://help.github.com/en/articles/github-terms-of-service#6-contributions-under-repository-license . More detail on the open book license can be found in the book index and preamble (index.rst).

## Version History


| Jython Version | Book version | Book citation |
| -------------- | ------------ | ---------| 
| Jython 2.5     | 1.0          | Juneau, J., Baker, J., Wierzbicki, F., Muoz, L. S., Ng, V., Ng, A., & Baker, D. L. (2010). The definitive guide to Jython: Python for the Java platform. Apress. |
 

## How to Create the Jython Book from Source

Create a working directory, say `dg-jython` and `cd` into it. There, clone this repo (here using Windows Posh):
```
PS dg-jython> git clone https://github.com/jython/book.git

```
This creates a sub-directory `book`.
The book builds using Sphinx and Python 3 in a virtual environment. All you need to begin with is Python.
If you do not have `virtualenv`, install it:
```
PS dg-jython> python3 -m pip install virtualenv
```
(You may need to specify ``python3`` explicitly as shown, or `py -3`, or it may just be `python` depending on your set-up.)
Now create a virtual environment, activate it and install the tools.
```
PS dg-jython> python3 -m virtualenv venv
...
PS dg-jython> .\venv\Scripts\activate
(venv) PS dg-jython> pip install -r .\book\requirements.txt
...
```

On Linux, it looks like this:
```
$ python3 -m pip install virtualenv
...
$ python3 -m virtualenv venv
Using base prefix '/usr'
...
$ source venv/bin/activate
(venv) $ pip install -r book/requirements.txt
...
```

You can now build the book as HTML in `./build` with the command:
```
(venv) $ sphinx-build -M html book build
```
and open `build/html/index.html` with a browser.
