"""ActiveState Code Recipes magics

This magic supplies this functions:

%lookup line magic
   It uses current line as arguments for querying ActiveState recipes,
   then returns indexed list with up to 10 recipe names

%fetch line magic
   It pretty-prints recipe by index from lookup results or by id

%place line magic
   Places recipe by index from lookup results or by id, on input line

%imply line magic
   Imports recipe by index from lookup results or by id, in user namespace

%desc line magic
   Prints recipe's description by index from lookup results or by id

As not so obvious feature, there is _recipesmagics object in user_ns
that holds the data from last query, with json kind of structure:

_recipesmagics = {idx: {'title': title, 'id': id}}
"""
#-----------------------------------------------------------------------------
# Copyright (C) 2012, debjan
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with IPython package
#-----------------------------------------------------------------------------

try:
    from urllib import quote_plus
    from urllib2 import build_opener
except ImportError:  # Python 3
    from urllib.parse import quote_plus
    from urllib.request import build_opener

from IPython.core.magic import Magics, magics_class, line_magic

ns = "{http://www.w3.org/1999/xhtml}"
opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
_loaded = False


@magics_class
class RecipesMagics(Magics):
    """Provides %lookup, %fetch, %imply and %desc magics"""
    @line_magic
    def lookup(self, line):
        """Searches for ActiveState recipes from supplied terms.

        Usage: %lookup <search terms>

        Returns: indexed list of recipes, that can be fetched by %fetch magic,
        or imported with %imply magic, from returned index in lookup results
        """
        if len(line):
            _recipesmagics = {}
            provider = 'http://www.bing.com/search?q=%s+' % quote_plus(line)
            provider += 'python+site:code.activestate.com/recipes'
            try:
                from lxml import etree
                parser = etree.XMLParser(resolve_entities=0)
                tree = etree.parse(opener.open(provider), parser)
            except ImportError:  # fallback to SPL parser
                import xml.etree.ElementTree as ET
                parser = ET.XMLParser()
                parser.parser.UseForeignDTD(1)
                parser.entity['nbsp'] = '&#x00A0;'
                tree = ET.parse(opener.open(provider), parser=parser)
            except Exception as e:
                self.shell.write(header('Exception:') + '%s\n' % e)

            base_url = 'http://code.activestate.com/recipes'
            path = ".//{0}li//{0}h3/{0}a".format(ns)
            for el in [et.get('href') for et in tree.findall(path)]:
                sn = el.split('/')[4].split('-')
                if sn[0].isdigit():
                    _recipesmagics[len(_recipesmagics)] = {
                        'title': ' '.join(sn[1:]),
                        'id': sn[0]
                    }
            self.shell.push('_recipesmagics')

        if self.shell._ofind('_recipesmagics')['found']:
            _recipesmagics = self.shell.user_ns['_recipesmagics']
            if len(_recipesmagics):
                for k, v in _recipesmagics.items():
                    self.shell.write(header(' %s:' % k, 4) + '%s %s\n' %
                                    (v['title'],
                                     '...' * (len(v['title']) / 49)))
            else:
                self.shell.write('Sorry, no results.')

    @line_magic
    def fetch(self, line):
        """Fetches ActiveState recipe.

        Usage: %fetch <idx|id>

        where "idx" is recipe's index number returned from lookup results
        or "id" is recipe ID

        Returns: pretty-printed recipe
        """
        recipe_code = self.get_recipe(line, 'code')
        if recipe_code:
            self.shell.write(self.shell.pycolorize(recipe_code))

    @line_magic
    def imply(self, line):
        """Imports ActiveState recipe.

        Usage:
          %imply <idx|id>

        where "idx" is recipe's index number returned from lookup results
        or "id" is recipe id

        Returns: imported recipe code as "recipe" in user namespace
        """
        if self.shell._ofind('recipe')['found']:
            msg = header('Warning: ', 9) +\
                '"recipe" variable is already initialized. ' +\
                'Please delete it before importing recipe.\n'
            self.shell.write(msg + header('Suggest: ', 9) + '"del recipe"')
        else:
            # ActiveState recipe 82234
            recipe_code = self.get_recipe(line, 'code')
            if recipe_code:
                import imp
                recipe = imp.new_module('recipe')
                try:
                    exec recipe_code in recipe.__dict__
                    self.shell.push('recipe')
                    self.shell.write('%s Recipe %s imported as "recipe".' %
                                     (header('Info:', 6), line))
                except Exception as e:
                    msg = header('Error:') +\
                        'Recipe %s could not be imported\n' % line
                    self.shell.write(msg + header('Exception:') + '%s\n' % e)

    @line_magic
    def place(self, line):
        """Places ActiveState recipe on next input line.

        Usage: %place <idx|id>

        where "idx" is recipe's index number returned from lookup results
        or "id" is recipe ID

        Returns: Recipe code on input line
        """
        if not self.shell.config.KernelApp or \
            self.shell.config.KernelApp.values()[0] == 'ipython-console':
            self.shell.write(header('Info:', 6) +
                             'Feature not supported in terminal')
        else:
            recipe_code = self.get_recipe(line, 'code')
            if recipe_code:
                self.shell.set_next_input(recipe_code)

    @line_magic
    def desc(self, line):
        """Get ActiveState recipe description

        Usage: %desc <idx|id>

        where "idx" is recipe's index number returned from lookup results
        or "id" is recipe id

        Returns: description string
        """
        description = self.get_recipe(line, 'description')
        if description:
            self.shell.write(description)

    def get_recipe(self, i, k):
        if len(i):
            try:
                import json
                from ast import literal_eval
                n = int(literal_eval(i))
                if n < 10 and self.shell._ofind('_recipesmagics')['found']:
                    i = self.shell.user_ns['_recipesmagics'][n]['id']
                r = 'http://code.activestate.com/recipes/api/2/recipes/%s/'
                req = opener.open(r % i)
                return json.load(req)[k].encode('utf-8')
            except Exception as e:
                msg = header('Error:') +\
                    'Recipe with index or id as %s, not found.\n' % i
                self.shell.write(msg + header('Exception:') + '%s\n' % e)
        else:
            self.shell.write(usage())


def header(t, x=12):
    return('\x1b[0;35m%s\x1b[0m' % t + ' ' * (x - len(t)))


def usage():
    return header('%lookup', 8) + '<search term>\n' +\
        header('%fetch', 8) + '<idx|id>\n' +\
        header('%imply', 8) + '<idx|id>\n' +\
        header('%desc', 8) + '<idx|id>\n'


def load_ipython_extension(ip):
    global _loaded
    if not _loaded:
        ip.register_magics(RecipesMagics)
        ip.write(usage())
        if ip.config.KernelApp and \
            ip.config.KernelApp.values()[0] != 'ipython-console':
            ip.write(header('%place', 8) + '<idx|id>\n')
        _loaded = True
