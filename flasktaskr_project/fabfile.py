from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
    with settings(warn_only=True):
        result = local("python2 test_tasks.py -v && python2 test_users.py -v",
                        capture=True)
        if result.failed and not confirm("Tests failed. Continue?"):
            abort("Aborted at user request.")

def commit():
    message = raw_input("Enter a commit message: ")
    local("git add . && git commit -am '{}'".format(message))

def pull():
    local("git --git-dir=../.git pull origin master")

def push():
    local("git --git-dir=../.git push origin master")

def prepare():
    test()
    commit()
    push()

# deploy

def heroku():
    local("git push heroku master")

def heroku_test():
    local("heroku run python test_tasks.py -v &&\
         heroku run python test_users.py -v")

def rollback():
    local("heroku rollback")

def deploy():
    pull()
    test()
    commit()
    heroku()
    heroku_test()
    

