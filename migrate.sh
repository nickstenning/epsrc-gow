#!/bin/bash

SCHEMAS_DIR="./schema"

if [[ "$#" != "2" ]]; then
  echo "Usage: migrate.sh <database> <toversion>"
  exit 1
else
  DB="${1}"
  DEST="${2}"
fi

function migrateup () {
  for n in $(eval echo {${1}..${2}}); do
    FNAME="${SCHEMAS_DIR}/$(printf "%03g" ${n})_up.sql"
    echo "sqlite3 ${DB} < ${FNAME}"
    sqlite3 "${DB}" < "${FNAME}"
  done   
}

function migratedown () {
  for n in $(eval echo {${1}..${2}}); do
    FNAME="${SCHEMAS_DIR}/$(printf "%03g" ${n})_down.sql"
    echo "sqlite3 ${DB} < ${FNAME}"
    sqlite3 "${DB}" < "${FNAME}"
  done    
}

CUR=$(sqlite3 "${DB}" "select version from schema limit 1" 2> /dev/null || echo 0)

if (( ${DEST} == ${CUR} )); then
  echo "Destination version is current version, aborting."
  exit
elif (( ${DEST} > ${CUR} )); then
  read -p "Migrating up from version ${CUR} to version ${DEST}. Continue? "
  if [[ $REPLY =~ ^[Yy] ]]; then
    migrateup $(( ${CUR} + 1 )) ${DEST}
    exit
  fi
elif (( ${DEST} < ${CUR} )); then
  read -p "Migrating down from version ${CUR} to version ${DEST}. Continue? "
  if [[ $REPLY =~ ^[Yy] ]]; then
    migratedown ${CUR} $(( ${DEST} + 1 ))
    exit
  fi     
fi   

echo "Aborted!"
exit 1