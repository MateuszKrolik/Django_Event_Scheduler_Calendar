#!/bin/bash

#! /bin/bash

source .env

gcloud iam service-accounts create build-event-scheduler-dev-sa \
  --description="Service account for build process in Django Event Scheduler development environment" \
  --display-name="Build event-scheduler Dev SA" \
  --project=$GCLOUD_ID

SA_EMAIL="build-event-scheduler-dev-sa@$GCLOUD_ID.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $GCLOUD_ID \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/artifactregistry.writer

gcloud projects add-iam-policy-binding $GCLOUD_ID \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/run.admin

gcloud projects add-iam-policy-binding $GCLOUD_ID \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/iam.serviceAccountUser

gcloud projects add-iam-policy-binding $GCLOUD_ID \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/secretmanager.secretAccessor

gcloud projects add-iam-policy-binding $GCLOUD_ID \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/cloudbuild.builds.editor

gcloud projects add-iam-policy-binding $GCLOUD_ID \
  --member=serviceAccount:$SA_EMAIL \
  --role=roles/logging.admin

# chmod +x gcloud_custom.sh
# ./gcloud_custom.sh

gcloud projects get-iam-policy $GCLOUD_PROJECT_NUMBER  \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:build-event-scheduler-dev-sa@$GCLOUD_ID.iam.gserviceaccount.com"

# ROLE
# roles/artifactregistry.writer
# roles/cloudbuild.builds.editor
# roles/iam.serviceAccountUser
# roles/logging.admin
# roles/logging.logWriter
# roles/run.admin
# roles/secretmanager.secretAccessor

# To avoid CloudBuild Error - "Permission denied on secret":

gcloud projects add-iam-policy-binding $GCLOUD_PROJECT_NUMBER \
  --member="serviceAccount:$GCLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"


gcloud projects get-iam-policy $GCLOUD_PROJECT_NUMBER \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="$GCLOUD_PROJECT_NUMBER-compute@developer.gserviceaccount.com"

# ROLE
# roles/editor
# roles/secretmanager.secretAccessor