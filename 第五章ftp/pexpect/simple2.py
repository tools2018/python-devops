from __future__ import unicode_literals

import winpexpect
import sys

child = winpexpect.winspawn('ftp ftp.openbsd.org')
child.winpexpect('(?i)name .*: ')
child.sendline('anonymous')
child.winexpect('(?i)password')
child.sendline('pexpect@sourceforge.net')
child.winexpect('ftp> ')
child.sendline('bin')
child.winexpect('ftp> ')
child.sendline('get robots.txt')
child.winexpect('ftp> ')
sys.stdout.write(child.before)
print("Escape character is '^]'.\n")
sys.stdout.write(child.after)
sys.stdout.flush()
child.interact()# Escape character defaults to ^]
child.sendline('bye')
child.close()
