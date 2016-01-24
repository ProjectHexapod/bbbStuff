#!/bin/bash

# Create folder for symlinks
mkdir /mnt/hardware

# PWMs
ln -s /sys/class/pwm/pwmchip2/pwm1/duty_cycle /mnt/hardware/pwm_knee_extend 
ln -s /sys/class/pwm/pwmchip2/pwm0/duty_cycle /mnt/hardware/pwm_knee_retract 
ln -s /sys/class/pwm/pwmchip0/pwm0/duty_cycle /mnt/hardware/pwm_thigh_down 
ln -s /sys/class/pwm/pwmchip0/pwm1/duty_cycle /mnt/hardware/pwm_thigh_up 

# Analog inputs
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage4_raw /mnt/hardware/ain_knee_str_pot   
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage6_raw /mnt/hardware/ain_thigh_str_pot  
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage5_raw /mnt/hardware/ain_complient_link 
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage2_raw /mnt/hardware/ain_thigh_feedback 
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage3_raw /mnt/hardware/ain_knee_feedback  
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage0_raw /mnt/hardware/ain_battery_voltage

# Make stompy user the owner of symlinks
chown -R stompy:stompy /mnt/hardware
