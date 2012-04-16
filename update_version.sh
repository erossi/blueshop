#|/bin/sh

# Update the version.py file with the current GIT version.

FILENAME="bin/version.py"
GIT_TAG="_version_ = \"$(git describe --tags)\""

if [ -f $FILENAME ]; then
	echo $GIT_TAG > $FILENAME
fi

