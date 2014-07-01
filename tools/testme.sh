#!/bin/sh

# Change this to your fully installation path.
INSTALL=$(pwd)
export BLUESHOP_CFG=$INSTALL/test
export BLUESHOP_DEBUG="true"

if [ -e $BLUESHOP_CFG/blueshop.cfg ]; then
	cd $INSTALL/bin
	python blueshop.py
else
	echo "Configuration file not found! Please fix."
fi;

