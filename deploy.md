SSH

* google for "passwordless ssh"
* http://www.linuxproblem.org/art_9.html

Fabric

* http://www.fabfile.org/
* http://docs.fabfile.org/en/1.11/tutorial.html
* http://docs.fabfile.org/en/1.11/usage/execution.html#execution-strategy


        from fabric.api import run, env

        env.hosts = ['clic.cs.columbia.edu']

        def taskA():
            run('ls')⏎

Staging server

* just same thing running on another port
* run a suite of tests that should work on staging.  
  if it does, then deploy to production