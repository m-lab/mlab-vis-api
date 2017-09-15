#!/bin/bash

###
# Staging environment variable setup
###

KEY_FILE=../mlab-keys/mlab-sandbox-pipeline-bigtable@mlab-sandbox.iam.gserviceaccount.com-creds.json
PROJECT=mlab-staging
BIGTABLE_INSTANCE=mlab-ndt-agg
API_MODE=staging
BIGTABLE_POOL_SIZE=10