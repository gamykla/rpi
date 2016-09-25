# rpi

Raspberry Pi applications

security_camera
---------------
* setup - create /home/pi/cam_server_settings.json. Include keys
 * CLIENT_KEY: camera server client id
 * CLIENT_SECRET: camera server client secret
 * UPLOAD_ENDPOINT_URL: camera server image upload endpoint.
* start
```
rpi/security/security_camera.py &
```
* stop
```
kill -INT $(cat /home/pi/security_camera.pid)
```

