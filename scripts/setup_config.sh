#!/bin/sh -e

echo "Creating local directories..."
mkdir /home/pi/oasis-grow/configs
mkdir /home/pi/oasis-grow/data_out
mkdir /home/pi/oasis-grow/data_out/image_feed
mkdir /home/pi/oasis-grow/data_out/sensor_feed
mkdir /home/pi/oasis-grow/data_out/logs

echo "Moving configuration files..."
cp /home/pi/oasis-grow/defaults/hardware_config_default_template.json /home/pi/oasis-grow/configs/hardware_config.json
cp /home/pi/oasis-grow/defaults/access_config_default_template.json /home/pi/oasis-grow/configs/access_config.json
cp /home/pi/oasis-grow/defaults/feature_toggles_default_template.json /home/pi/oasis-grow/configs/feature_toggles.json
cp /home/pi/oasis-grow/defaults/device_state_default_template.json /home/pi/oasis-grow/configs/device_state.json
cp /home/pi/oasis-grow/defaults/grow_params_default_template.json /home/pi/oasis-grow/configs/grow_params.json

echo "Creating new lock_file..."
cp /home/pi/oasis-grow/defaults/locks_default_template.json /home/pi/oasis-grow/configs/locks.json

echo "Creating placeholder image..."
cp /home/pi/oasis-grow/defaults/default_placeholder_image.jpg /home/pi/oasis-grow/data_out/image.jpg
