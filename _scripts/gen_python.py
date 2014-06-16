import re
import markdown
import os
import sys
import yaml
import json
import codecs
import subprocess

# We don't read the index
IGNORED_FILES = "index.md"

# The class for all reql objects
query = 'rethinkdb.ast.RqlQuery.'

# The python class associated with each type
parents = {
    None: '',
    'r': 'rethinkdb.',
    'sequence': query,
    'query': query,
    'stream': query,
    'grouped_stream': query,
    'singleSelection': query,
    'array': query,
    'number': query,
    'bool': query,
    'value': query,
    'string': query,
    'time': query,
    'any': query,
    'connection': 'rethinkdb.net.Connection.',
    'cursor': 'rethinkdb.net.Cursor.',
    'db': 'rethinkdb.ast.DB.',
    'table': 'rethinkdb.ast.Table.',
}

# The real python names for names used in the docs
tags = {
    '[] (get_field)': [(query, '__getitem__')],
    '[] (nth)': [(query, 'nth')],
    'slice, []': [(query, 'slice')],
    '+': [(query, '__add__'), ('rethinkdb.', 'add')],
    '-': [(query, '__sub__'), ('rethinkdb.', 'sub')],
    '*': [(query, '__mul__'), ('rethinkdb.', 'mul')],
    '/': [(query, '__div__'), ('rethinkdb.', 'div')],
    '%': [(query, '__mod__'), ('rethinkdb.', 'mod')],
    '&, and_': [(query, '__and__'), ('rethinkdb.', 'and_')],
    '|, or_': [(query, '__or__'), ('rethinkdb.', 'or_')],
    '==, eq': [(query, '__eq__'), (query, 'eq')],
    '!=, ne': [(query, '__ne__'), (query, 'ne')],
    '<, lt': [(query, '__lt__'), (query, 'lt')],
    '>, gt': [(query, '__gt__'), (query, 'gt')],
    '<=, le': [(query, '__le__'), (query, 'le')],
    '>=, ge': [(query, '__ge__'), (query, 'ge')],
    '~, not_': [(query, '__invert__'), (query, 'not_'), ('rethinkdb.', 'not_')],
    'r': [('', 'rethinkdb')],
    'repl': [('rethinkdb.net.Connection.', 'repl')],
    'count': lambda parent: not parent == 'rethinkdb.' and [(query, 'count')] or []
}

has_methods = { 'rethinkdb.': False, '': False }


# Write the header of the docs.py file
def write_header(file):
    file.write('# This file was generated by _scripts/gen_python.py from the rethinkdb documentation in http://github.com/rethinkdb/docs\n')
    commit = out = subprocess.Popen(['git', 'log', '-n 1', '--pretty=format:"%H"'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    file.write('# hash: '+commit+'\n\n\n')
    file.write('import rethinkdb\n')
    file.write('from ._compat import get_unbound_func\n')

# Browse all the docs
def browse_files(base, result_file):
    subdirlist = []
    # Because we don't read from the json file, that is enough to guarantee an order
    for item in sorted(os.listdir(base)):
        if item[0] != '.' and item not in IGNORED_FILES:
            full_path = os.path.join(base, item)
            if os.path.isfile(full_path):
                add_doc(full_path, result_file)
            else:
                subdirlist.append(full_path)

    for subdir in subdirlist:
        browse_files(subdir, result_file)


# Add docs in result for one file
def add_doc(file_name, result_file):
    limiter_yaml = re.compile('---\s*')
    is_yaml = False
    yaml_header = ""

    parent = ""

    # Reading the JS file to extract the io data
    file_name_js = file_name.replace('python', 'javascript')
    try:
        details_file_js = codecs.open(file_name_js, "r", "utf-8")

        yaml_header_js = ""
        for line in details_file_js:
            if limiter_yaml.match(line) != None:
                # We ignore the yaml header
                if is_yaml == False:
                    is_yaml = True
                else:
                    break
            elif is_yaml == True:
                yaml_header_js += line

        yaml_data_js = yaml.load(yaml_header_js)
 
        parent = parents[yaml_data_js['io'][0][0]]

    except:
        # The file may not exist (for repl for example)
        #print "Opening "+ file_name_js
        #print sys.exc_info()[0]
        pass


    # Open the python file
    details_file = codecs.open(file_name, "r", "utf-8")

    # Define some regex that we will use
    ignore_pattern = re.compile("#.*#.*|<img.*/>") # Used to skip the titles like Description, Related commands etc.

    # Used to skip the body (command syntax)
    start_body_pattern = re.compile("{%\s*apibody\s*%}\s*")
    end_body_pattern = re.compile("{%\s*endapibody\s*%}\s*")
    parsing_body = False

    # Tracking the yaml header, we need it for the command name
    is_yaml = False
    yaml_header_py = ""


    # Track if we are parsing some code
    example_code_start_pattern = re.compile("```py")
    example_code_end_pattern = re.compile("```")
    parsing_example_code = False


    text = ""

    for line in details_file:
        # Ignore titles (h1 tags)
        if ignore_pattern.match(line) != None:
            continue

        if limiter_yaml.match(line) != None:
            # We ignore the yaml header
            if is_yaml == False:
                is_yaml = True
            else:
                yaml_data_py = yaml.load(yaml_header_py)
                name = yaml_data_py["command"]
                is_yaml = False
        elif is_yaml == True:
            yaml_header_py += line
        elif is_yaml == False:
            if start_body_pattern.match(line) != None:
                parsing_body = True
            elif end_body_pattern.match(line) != None:
                parsing_body = False
            elif parsing_body == False:
                if example_code_start_pattern.match(line) != None:
                    example_code_first_line = True
                    parsing_example_code = True
                elif example_code_end_pattern.match(line) != None:
                    parsing_example_code = False
                else:
                    if parsing_example_code == True:
                       if example_code_first_line == True:
                            text += ">>> "+line
                            example_code_first_line = False
                       else:
                            text += "... "+line
                    else:
                        text += line

    def add_line():
        result_file.write("\n")
        result_file.write('get_unbound_func' if has_methods.get(parent, True) else '')
        result_file.write('({}).__doc__ = '.format(parent + name))
        result_file.write(repr(re.sub("(__Example:__)|(__Example__:)", "*Example:*", re.sub("^\n+", "", re.sub("\n{2,}", "\n\n", text)))))
 
    # If the command has multiple name, parents
    if name in tags:
        names = tags[name]
        if type(names) == type(lambda x: x):
            names = names(parent)

        for parent, name in names:
            add_line()
    else: # If the command has just one name and one parent
        add_line()


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__))

    result_file = codecs.open(script_path+"/docs.py", "w", "utf-8")
    
    write_header(result_file)

    browse_files(script_path+"/../api/python/", result_file)

    result_file.close()
