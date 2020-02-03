#!/bin/sh

cp version-counter.service /etc/systemd/system/version-counter.service
chmod 644 /etc/systemd/system/version-counter.service
systemctl enable version-counter
systemctl restart version-counter

