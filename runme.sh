#!/bin/sh

INSTALL=/my_installation_path/blueshop
export BLUESHOP_CFG=$INSTALL/cfg
export BLUESHOP_DEBUG="true"

if [ -e $BLUESHOP_CFG/blueshop.cfg ]; then
	cd $INSTALL/bin
	python blueshop.py
else
	echo "Configuration file not found! Please fix."
fi;

