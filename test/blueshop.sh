#!/bin/sh

# Change this to your fully installation path.
INSTALL=$(pwd)
export BLUESHOP_PATH=$(pwd)
export BLUESHOP_CFG=$INSTALL/tmp
export BLUESHOP_DEBUG="true"

if [ -e $BLUESHOP_CFG/blueshop.cfg ]; then
	python blueshop
else
	echo "Configuration file not found! Please fix."
fi;
