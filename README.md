# rootkh

## INSTALL
1. Install debian pkgs:

`$ cat requirements-debian.txt | xargs sudo apt-get install`

2. Install virtualenv

`$ mkvirtualenv rootkh -r requirements.txt`

3. Patch tinydav

~/.virtualenvs/rootkh/lib/python3.4/site-packages/tinydav/__init__.py:717
kwargs = dict()
