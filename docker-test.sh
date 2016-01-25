#!/bin/sh

FLAVOUR=$1
FLAVOUR_SLUG=$(echo "$FLAVOUR" | sed 's/\W/-/')

docker run --rm -it \
    --name "flockcontext-test-$FLAVOUR_SLUG" \
    -v "$PWD:/home/docker/code" \
    $FLAVOUR \
    /bin/sh -c "cd /home/docker/code && python setup.py install && python setup.py test"
