#!/bin/bash

# Create folder for symlinks
mkdir /mnt/hardware

# PWMs
ln -s /sys/class/pwm/pwmchip2/pwm1/duty_cycle /mnt/hardware/pwm_rleg_backwards 
ln -s /sys/class/pwm/pwmchip2/pwm0/duty_cycle /mnt/hardware/pwm_rleg_forwards 
ln -s /sys/class/pwm/pwmchip0/pwm0/duty_cycle /mnt/hardware/pwm_lleg_forwards 
ln -s /sys/class/pwm/pwmchip0/pwm1/duty_cycle /mnt/hardware/pwm_lleg_backwards 

# Analog inputs
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage4_raw /mnt/hardware/ain_lleg_str_pot   
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage6_raw /mnt/hardware/ain_rleg_str_pot  
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage2_raw /mnt/hardware/ain_lleg_feedback 
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage3_raw /mnt/hardware/ain_rleg_feedback  
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage0_raw /mnt/hardware/ain_battery_voltage

# Make stompy user the owner of symlinks
chown -R stompy:stompy /mnt/hardware
