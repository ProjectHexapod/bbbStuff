#!/bin/bash

mkdir /mnt/hardware
ln -s /sys/class/pwm/pwmchip2/pwm1/duty_cycle /mnt/hardware/pwm_knee_extend 
ln -s /sys/class/pwm/pwmchip2/pwm0/duty_cycle /mnt/hardware/pwm_knee_retract 
ln -s /sys/class/pwm/pwmchip0/pwm0/duty_cycle /mnt/hardware/pwm_thigh_down 
ln -s /sys/class/pwm/pwmchip0/pwm1/duty_cycle /mnt/hardware/pwm_thigh_up 
chown -r stompy:stompy /mnt/hardware
