# fabfile.py
# for droplet deployment

from fabric.api import *

env.hosts = ['192.241.179.74']
env.user = 'root'

def update():
	run('pwd')
	with cd('../../home/GPaaS/expDeploy/'):
		run('git pull')
		run('python src/manage.py makemigrations')
		run('python src/manage.py migrate')
		run('sudo service apache2 restart')
