#|/bin/sh

# Update the version.py file with the current GIT version.

FILENAME="bin/version.py"
GIT_TAG=$(git describe --tags|sed -e "s/^\(.*\)-.*/\1/")
GIT_TAG="_version_ = $GIT_TAG"

if [ -f $FILENAME ]; then
	echo $GIT_TAG > $FILENAME
fi

