from fabric.api import task, run, local, settings, cd


@task
def pull_code():
    """
    fab -u pi -i ~/keys/rpi/id_rsa pull_code
    """
    with settings(host_string="raspberry.pi"):
        with cd('/home/pi/src/rpi'):
            run('git pull')


@task
def flake8():
    local('flake8 . --max-line-length=120')
