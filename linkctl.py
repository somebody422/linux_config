#!/usr/bin/python3

import os
import os.path as path
import sys
import argparse
import json


# no args / status - print
# status - print
# link - create links
# rm / remove - 
parser = argparse.ArgumentParser(description='Manage linked configuration')
subparsers = parser.add_subparsers(help='sub-command help', dest='command')

status_subparser = subparsers.add_parser('status', help='HELP TODO')

create_subparser = subparsers.add_parser('create', help='TODO')
create_subparser.add_argument('links_file', type=str, help="Path to .links file")

#parser.add_argument('command', type=str,
#  choices=['status', 'create', 'rm', 'remove'],
#  default=['status'],
#  nargs='?',  # If argument is not provided, use the default value
#  help='Sub-command to run')


"""
Scratch / planning for redesign:

Status and create will both need to
* parse links file
* check each link to make sure
  * target exists as a valid path. Should be /.../linux_config/files/...
  * get status of link location. Is it currently correct?

If using a single "scan" function to check link status for both 'status' and 'create' commands, return might look like:
{ isCurrent:bool, links:[ {links_path:'', target_path:'', link_path:'', link_is_valid:bool, link_is_backed_up:bool},
  {links_path:'/root/linux_config/links/nfs-service.links', target_path:'/root/linux_config/files/exports', link_path:'/etc/exports', link_is_valid:True, link_is_backed_up: False}
  ]}


"""

class LinksAttributes:
  pass

def parse_links_dir():
  """
  Iterate over files in the links directory, returning a LinksAttributes for each '.links' file
  """
  dir_links = []  # all links in the links/ directory
  links_dir_path = path.join(LINUX_CONFIG_PATH, 'links')
  for links_path in os.listdir(links_dir_path):
    links_path = path.join(links_dir_path, links_path)
    if not path.isfile(links_path) or path.splitext(links_path)[1] != '.links':
      print('continue..')
      continue

    dir_links.append({
      'links_path': links_path,
      'links': parse_links(links_path),
    })
  return dir_links


def parse_links(links_path):
  """
  Parse through links file, returning a linksAttributes
  """
  print('parse_links:', links_path)
  with open(links_path, 'r') as links_f:
    links = json.loads(links_f.read())
  # Validate links
  for link in links:
    print("  link:", link)
    for link_key in link.keys():
      assert link_key in LINKS_JSON_ALLOWED_FIELDS
    for link_required_key in LINKS_JSON_REQUIRED_FIELDS:
      assert link_required_key in link
  return links

def command_status():
  links_dir = parse_links_dir()
  for links in links_dir:
    print(links['links_path'] + ':')
    for link in links['links']:
      target_path = link['target_path'] if path.isabs(link['target_path']) else path.join(LINUX_CONFIG_PATH, link['target_path'])
      if not path.islink(link['link_path']) or os.readlink(link['link_path']) != target_path:
        char = 'x'
      else:
        char = '*'
      print('  {} {}->{}'.format(char, link['link_path'], link['target_path']))


def command_create(links_path):
  print('links_path:', links_path)
  links = parse_links(links_path)
  print('links:', links)
  for link in links:
    # Change target_path into an absolute path if appropriate
    target_path = link['target_path'] if path.isabs(link['target_path']) else path.join(LINUX_CONFIG_PATH, link['target_path'])
    print('Processing link {}->{}'.format(link['link_path'], target_path))
    if path.islink(link['link_path']) and os.readlink(link['link_path']) == target_path:
      print('  Link already exists')
    else:
      #TODO backup here if appropriate
      #if path.xyz(zyx)
      print('  creating link')
      os.symlink(target_path, link['link_path'])



LINUX_CONFIG_PATH = path.dirname(path.realpath(__file__)).split('linux_config')[0] + 'linux_config'
assert path.isdir(LINUX_CONFIG_PATH)
LINKS_JSON_ALLOWED_FIELDS = (
  'target_path', 'link_path', 'backup'
)
LINKS_JSON_REQUIRED_FIELDS = ('target_path', 'link_path')

if __name__ == '__main__':
  print('LINUX_CONFIG_PATH:', LINUX_CONFIG_PATH)
  args = parser.parse_args()
  print('args:', args)

  if args.command is None or args.command == 'status':
    command_status()

  elif args.command == 'create':
    command_create(args.links_file)

