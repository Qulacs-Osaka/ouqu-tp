#!/bin/bash
set -e

# $1: Project name which is renamed to.
function validate_project_name() {
    local pattern="[a-z]|_"
    if [[ ! $1 =~ $pattern ]]
    then
        echo "Project name must consists of a-z and underscore(_)."
        exit 1
    fi
}

function rename_project_in_file() {
    local platform="$OSTYPE"
    case $platform in
        "linux-gnu"*) sed -i "s/$1/$2/g" $3 ;;
        "darwin"*) sed -i \"\" "s/$1/$2/g" $3 ;;
        *) echo "Unsupported platform: $platform"; exit 1 ;;
    esac
}

# Rename project name in files.
# $1: Project name which is renamed from.
# $2: Project name which is renamed to.
function rename_project() {
    local files=$(find . \
    -not \( -path "./.venv" -prune \) \
    -not \( -path "./.git" -prune \) \
    -not \( -path "./.pytest_cache" -prune \) \
    -not \( -path "./.mypy_cache" -prune \) \
    -type f)
    for file in $files; do
        rename_project_in_file $1 $2 $file
    done
}

RENAME_FROM="wonderful_project"
RENAME_TO=$1
validate_project_name "$RENAME_TO"
rename_project "$RENAME_FROM" "$RENAME_TO"