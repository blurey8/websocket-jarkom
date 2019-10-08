import subprocess as sp

sp.run("lscpu", shell=True, check=True).stdout

# from subprocess import Popen, PIPE

# p = Popen(['lscpu'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
# output, err = p.communicate(b"input data that is passed to subprocess' stdin")
# rc = p.returncode