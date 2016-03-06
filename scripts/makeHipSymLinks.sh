#!/bin/bash

# Create folder for symlinks
mkdir /mnt/hardware
rm /mnt/hardware/*

# PWMs
ln -s /sys/devices/platform/ocp/48304000.epwmss/48304200.ehrpwm/pwm/pwmchip2/pwm1/duty_cycle /mnt/hardware/pwm_rleg_backwards
ln -s /sys/devices/platform/ocp/48304000.epwmss/48304200.ehrpwm/pwm/pwmchip2/pwm0/duty_cycle /mnt/hardware/pwm_rleg_forwards
ln -s /sys/devices/platform/ocp/48300000.epwmss/48300200.ehrpwm/pwm/pwmchip0/pwm0/duty_cycle /mnt/hardware/pwm_lleg_forwards
ln -s /sys/devices/platform/ocp/48300000.epwmss/48300200.ehrpwm/pwm/pwmchip0/pwm1/duty_cycle /mnt/hardware/pwm_lleg_backwards

# Analog inputs
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage4_raw /mnt/hardware/ain_lleg_str_pot   
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage6_raw /mnt/hardware/ain_rleg_str_pot  
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage2_raw /mnt/hardware/ain_lleg_feedback 
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage3_raw /mnt/hardware/ain_rleg_feedback  
ln -s /sys/devices/platform/ocp/44e0d000.tscadc/TI-am335x-adc/iio:device0/in_voltage0_raw /mnt/hardware/ain_battery_voltage

# GPIO
ln -s /sys/class/gpio/gpio26 /mnt/hardware/gpio_M2_statusflag
ln -s /sys/class/gpio/gpio27 /mnt/hardware/gpio_enable_pin
ln -s /sys/class/gpio/gpio31 /mnt/hardware/gpio_M1_statusFlag
ln -s /sys/class/gpio/gpio5  /mnt/hardware/gpio_DIP_switch0
ln -s /sys/class/gpio/gpio4  /mnt/hardware/gpio_DIP_switch1
ln -s /sys/class/gpio/gpio13 /mnt/hardware/gpio_DIP_switch2
ln -s /sys/class/gpio/gpio12 /mnt/hardware/gpio_DIP_switch3
ln -s /sys/class/gpio/gpio17 /mnt/hardware/gpio_DIP_switch4
ln -s /sys/class/gpio/gpio15 /mnt/hardware/gpio_DIP_switch5

# Make stompy user the owner of symlinks
chown -R stompy:stompy /mnt/hardware
