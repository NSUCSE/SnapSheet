import sys
import subprocess

def django_run_server():
	cmd = ["py","manage.py","runserver"]
	subprocess.run(cmd)

def django_run_manage():
	cmd = ["py","manage.py"]
	cmd += sys.argv[1:]
	subprocess.run(cmd)