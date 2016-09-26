# rpi

Raspberry Pi applications

security_camera
---------------
https://hub.docker.com/r/jelis/cam_server/

Security camera is a raspberry pi application that detects motion and uploads images in which motion was detected to a security camera server. Useful for home security applications.
* setup - create /home/pi/cam_server_settings.json. Include keys
 * CLIENT_KEY: camera server client id
 * CLIENT_SECRET: camera server client secret
 * UPLOAD_ENDPOINT_URL: camera server image upload endpoint.
* start
```
# make sure requirements are installed
pip install -r requirements/base.txt
rpi/security/security_camera.py &
```
* stop
```
kill -INT $(cat /home/pi/security_camera.pid)
```
* installing security_camera as a systemd service
```
cp systemd/security_camera.service /lib/systemd/system
chmod 644 /lib/systemd/system/security_camera.service
sudo systemctl daemon-reload
sudo systemctl enable security_camera.service
# if you want to disable it:
sudo systemctl disable security_camera.service
# check service status
sudo systemctl status security_camera.service
```
* view logs
 * Log levels can be changed by editing security_camera.py. default is logger.setLevel(logging.INFO)
```
tail -f /var/log/syslog
```

dyn_dns
----------
* utils/dyn_dns.py dynamic dns update tool. Schedule it to run from a machine with your network to update your hostname dns address if you're using route53 hosted zones from AWS.

References
* http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/
* http://www.dynacont.net/documentation/linux/Useful_SystemD_commands/

