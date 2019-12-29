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
 

# How to Build the Jython Book from Source

## Install and Build

Building locally requires Python 3.5 or above.
Use of a virtual environment is recommended in order to to isolate this project’s dependencies (the tools).
All you need to begin with is an installed Python.

### Instructions for Windows Powershell.

1. Create a working directory, say `dg-jython`, and `cd` into it.
There, clone this repository:
```
PS dg-jython> git clone https://github.com/jython/book.git
```

These instructions assume you cloned into the directory `book`, a sub-directory of your working directory.
Do *not* `cd` into `book`: the build runs from the current directory: it will create a sub-directory `build` to hold the generated files.

2. If you do not have `virtualenv`, install it:
```
PS dg-jython> python3 -m pip install virtualenv
```
(You may need to specify ``python3`` explicitly as shown, or `py -3`, or it may just be `python` depending on your set-up.)

3. Now create a virtual environment, activate it and install the tools.
```
PS dg-jython> python3 -m virtualenv venv
...
PS dg-jython> .\venv\Scripts\activate
(venv) PS dg-jython> pip install -r .\book\requirements.txt
...
```

4. You can now build the book as HTML in `./build` with the command:
```
(venv) PS dg-jython> sphinx-build -N -b html book build\html
```
(The option `-N` suppresses output formatting that impedes reading on a PoSH console.) 

Open `build\html\index.html` with your browser to view the generated documentation.

### Instructions for Linux.

On Linux, it looks like this:
```
$ python3 -m pip install virtualenv
...
$ python3 -m virtualenv venv
Using base prefix '/usr'
...
$ source venv/bin/activate
(venv) $ pip install -r book/requirements.txt
(venv) $ sphinx-build -b html book build/html
...
```
Open `build/html/index.html` with your browser to view the generated documentation.


## Edit and Build

After edits to the restructured text files, rerun `sphinx-build -b html book build/html` to regenerate the documentation.

