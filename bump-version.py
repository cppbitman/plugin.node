
import os
import sys
import colorama
import semver
from shell import shell as call
from conans.client.loader_parse import load_conanfile_class
from conans.client.output import ConanOutput,Color

__dir__ =os.path.dirname(os.path.abspath(__file__))

colorama.init()
m = ConanOutput(sys.stdout, True)

# Shim for raw_input,print in python3
if sys.version_info > (3,):
    input_func = input
else:
    input_func = raw_input
def prompt(message, options=[]):
    ''' Prompts the user for input with the message and options '''
    if len(options) != 0:
        message = "%s [%s] " % (message, '/'.join(options))
    res = input_func(message)
    while res not in [str(x) for x in options]:
        res = input_func(message)
    return res


def check():
    status = call('git status -s --show-stash')
    if len(status.output()):
        m.error('There umcommit files, plsease commit them.')
        m.info("".join(status.output()))
        return False
    return True

def hint():
    conanfile = load_conanfile_class(os.path.join(__dir__,'conanfile.py'))
    m.writeln('')
    m.writeln('WE WILL BUMP THIS REPO TO NEW VERSION AND TAG IT.',
                   Color.BRIGHT_MAGENTA)
    m.writeln('current version : %s\n'%conanfile.version)

    m.info('[major] => %s'%semver.inc(conanfile.version,'major',loose=True))
    m.info('[minor] => %s'%semver.inc(conanfile.version,'minor',loose=True))
    m.info('[patch] => %s'%semver.inc(conanfile.version,'patch',loose=True))
    m.info('[cancel] cancel the version bump\n')
    res = prompt('which version to bump ?',['major','minor','patch','cancel'])
    if res == 'cancel':
        m.warn('you have cancel this version bumping.')
        return None
    return semver.inc(conanfile.version,res,loose=True)


def bump(version):
    pass
def confirm():
    pass

if __name__ == '__main__':
    check()
    hint()
