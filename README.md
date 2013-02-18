Activestate Code Recipes magics
-------------------------------

This magic supplies four functions:

 - `%lookup` line magic

  It uses current line as arguments for querying Activestate recipes, then returns indexed list with up to 10 recipe names

 - `%fetch` line magic

  It pretty-prints recipe by index from lookup results or by id

 - `%place` line magic

  Places recipe by index from lookup results or by id, on input line

 - `%imply` line magic

  Imports recipe by index from lookup results or by id, in user namespace

 - `%desc` line magic

  Prints recipe's description by index from lookup results or by id


Installation
------------
```
%install_ext http://ipython-recipes-magic.googlecode.com/svn/trunk/recipes.py
```


In action
---------

[Notebook example](http://nbviewer.ipython.org/url/ipython-recipes-magic.googlecode.com/svn/trunk/recipes.ipynb)

*Screenshot*

![screenshot](http://i.imgur.com/1Du5T.png)

For more information about IPython, do visit their home page: http://ipython.org