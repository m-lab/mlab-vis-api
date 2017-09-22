#!/bin/bash

USAGE="$0 [production|staging|arbitrary-string-sandbox] travis?"
if [[ -n "$2" ]] && [[ "$2" != travis ]]; then
  echo The second argument can only be the word travis or nothing at all.
  echo $USAGE
  exit 1
fi

set -e
set -x

if [[ $2 == travis ]]; then
  cd $TRAVIS_BUILD_DIR
  GIT_COMMIT=${TRAVIS_COMMIT}
else
  GIT_COMMIT=$(git log -n 1 | head -n 1 | awk '{print $2}')
fi

source "${HOME}/google-cloud-sdk/path.bash.inc"

# Adapted from the one from ezprompt.net
function git_is_dirty {
    status=`git status 2>&1 | tee`
    dirty=`echo -n "${status}" 2> /dev/null | grep "modified:" &> /dev/null; echo "$?"`
    newfile=`echo -n "${status}" 2> /dev/null | grep "new file:" &> /dev/null; echo "$?"`
    renamed=`echo -n "${status}" 2> /dev/null | grep "renamed:" &> /dev/null; echo "$?"`
    deleted=`echo -n "${status}" 2> /dev/null | grep "deleted:" &> /dev/null; echo "$?"`
    bits=''
    if [ "${renamed}" == "0" ]; then
        bits=">${bits}"
    fi
    if [ "${newfile}" == "0" ]; then
        bits="+${bits}"
    fi
    if [ "${deleted}" == "0" ]; then
        bits="x${bits}"
    fi
    if [ "${dirty}" == "0" ]; then
        bits="!${bits}"
    fi
    [[ -n "${bits}" ]]
}

# Initialize correct environment variables based on type of deployment
if [[ "$1" == production ]]; then
  source ./environments/production.sh
  if git_is_dirty ; then
    echo "We won't deploy to production with uncommitted changes"
    exit 1
  fi
elif [[ "$1" == staging ]]; then
  source ./environments/staging.sh
  if git_is_dirty ; then
    echo "We won't deploy to staging with uncommitted changes"
    exit 1
  fi
elif [[ "$1" == sandbox ]]; then
  source ./environments/sandbox.sh
else
  echo "BAD ARGUMENT TO $0"
  exit 1
fi

if [[ $2 == travis ]]; then
  gcloud auth activate-service-account --key-file ${KEY_FILE}
fi

# remove built files so we do not upload them.
find . -name '*.pyc' -delete

# Copy service key locally so that we can upload it as part of the deploy.
cp ${KEY_FILE} cred.json

# Copy templates folder for deploy
rm -rf deploy-build
mkdir deploy-build
cp templates/* deploy-build/

# Build app.yaml template
./travis/substitute_values.sh deploy-build \
    GOOGLE_APPLICATION_CREDENTIALS cred.json \
    KEY_FILE cred.json \
    API_MODE ${API_MODE} \
    PROJECT ${PROJECT} \
    BIGTABLE_INSTANCE ${BIGTABLE_INSTANCE} \
    BIGTABLE_CONFIG_DIR bigtable_configs \
    BIGTABLE_POOL_SIZE ${BIGTABLE_POOL_SIZE}

# Copy app.yaml to root... this is required for the deploy to identify the Dockerfile
cp deploy-build/app.yaml app.yaml

# Run deploy - You might need to approve this.
gcloud app deploy

# Remove cred file after deploy is done.
rm cred.json

