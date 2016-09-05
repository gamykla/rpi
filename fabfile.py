from fabric.api import task, run, settings, cd

@task
def pull_code():
    """
    fab -u pi -i ~/keys/rpi/id_rsa pull_code
    """
    with settings(host_string="raspberry.pi"):
        with cd('/home/pi/src/rpi'):
            run('git pull')
