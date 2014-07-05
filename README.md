Activestate Code Recipes magics
-------------------------------

This magic supplies five functions:

 - `%lookup` line magic

  It uses current line as arguments for querying Activestate recipes, then returns indexed list with up to 10 recipe names

 - `%desc` line magic

  Prints recipe's description by index from lookup results or by id

 - `%listing` line magic

  Listing of recipe by index from lookup results or by id

 - `%place` line magic

  Places recipe by index from lookup results or by id, on input line

 - `%imply` line magic

  Imports recipe by index from lookup results or by id, in user namespace


Installation
------------
```
%install_ext https://raw.githubusercontent.com/debjan/ipython-recipes-magic/master/recipes.py
```


Screenshot
---------

![screenshot](http://i.imgur.com/sf04pHT.png)
