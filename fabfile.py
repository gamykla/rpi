from fabric.api import task, run, local, settings, cd


@task
def push_to_pi():
    """
    fab -u pi -i ~/keys/rpi/id_rsa push_to_pi
    """
    # test()
    # TODO - need to improve image detection algorithm. maybe need variable threshold or configurable
    local('git add .;git commit; git push;')
    with settings(user="pi", host_string="raspberry.pi"):
        with cd('/home/pi/src/rpi'):
            run('git pull')


@task
def test():
    """
    fab test
    """
    local('flake8 . --max-line-length=120')
    local('nosetests')
