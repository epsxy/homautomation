# Systemd examples

```bash
# verify service
sudo systemd-analyze verify my.sensor.service

# reload conf
sudo systemctl daemon-reload

# start|stop|status
sudo systemctl start|stop|status my.sensor

# show logs
journalctl -u my.sensor
```