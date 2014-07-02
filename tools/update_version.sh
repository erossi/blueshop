#!/bin/sh

set -e

# Update the version.py file with the current GIT version.

FILENAME="modules/__init__.py"

if (type git > /dev/null 2>&1); then
    MAJOR=$(git describe --tags|sed -e "s/^\([^-]*\).*/\1/")
    TAGGED=$(git describe --tags|sed -e "s/^\(.*\)-.*/\1/")
    FULL=$(git describe --tags)

    echo "_version_ = \"$MAJOR\"" > $FILENAME
    echo "_tagged_version_ = \"$TAGGED\"" >> $FILENAME
    echo "_git_version_ = \"$FULL\"" >> $FILENAME
    echo "_lastupdate_ = \"$(date +%d/%m/%Y)\"" >> $FILENAME
fi

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
