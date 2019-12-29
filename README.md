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
 

# Build

## Install and Build

Building locally requires Python 3.5 or above. These instructions are for windows. Other platforms should be similar.

1. Clone into a new project directory. 

`git clone <repo>`

These instructions assume you cloned into the directory `book`. The build needs to be run from the parent of the source folder `book`: it will create sibling directory `build` to hold the generated files.

2. (Optional) Use virtualenv to isolate this project's dependencies 

```
virtualenv venv
.\venv\Scripts\activate
```

3. `pip install -r book\requirements.txt`

4. `sphinx-build -N -b html .\book build\html`

Open `build\html\index.html` with your browser to view the generated documentation.

## Edit and Build

After edits to the markdown files, rerun `sphinx-build -N -b html .\book build\html` to regenerate the documentation.

