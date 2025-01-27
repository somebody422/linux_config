
TODO:
* Implement backup in linkctl. Currently the field is ignored

## Directory Structure

* files/ - contains config files to be linked to other place in the filesystem.
* doc/ - Documention for the various configuration and service options
* links/ - .link files


## Templates links files

links files can be templated via the jinja2 templating language.

Example rendering which inserts the path to the user directory:
`./template-links.py links/user-configs.jinja2 links/user-configs-testuser.links home=/home/testuser`


