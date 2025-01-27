#!/usr/bin/python3

import os
import os.path as path
import sys
import argparse
import jinja2


"""
Render a jinja2 template into a links file

Usage: PROG TEMPLATE_PATH OUTPUT_PATH VAR1=VAL1 VAR2=VAL2 ...
e.g.: ./template-links.py ./test-template.jinja test-template-output var1=testval1 'var2=a longer test value for var2'
"""


parser = argparse.ArgumentParser(description='Manage linked configuration')
parser.add_argument('template', type=str)
parser.add_argument('destination', type=str)
parser.add_argument('variables', nargs='*')
args = parser.parse_args()
print(args)

jinja_vars = {key:val for (key, val) in [jinja_var.split('=')[:2] for jinja_var in args.variables]}
print("jinja_vars:", jinja_vars)

environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(path.dirname(__file__))
)
template = environment.get_template(args.template)
print(template)
with open(args.destination, 'w') as f:
  f.write(template.render(jinja_vars))



