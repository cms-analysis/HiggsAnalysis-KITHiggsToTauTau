#!/bin/bash -e

# Settings
REPO_PATH=https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau.git
HTML_PATH=docs/html
COMMIT_USER="Documentation Builder"
COMMIT_EMAIL="peter.fackeldey@rwth-aachen.de"
CHANGESET=$(git rev-parse --verify HEAD)

# Get a clean version of the HTML documentation repo.
rm -rf ${HTML_PATH}
mkdir -p ${HTML_PATH}
git clone -b gh-pages "${REPO_PATH}" --single-branch ${HTML_PATH}

# rm all the files through git to prevent stale files.
cd ${HTML_PATH}
git rm -rf .
cd -

echo ${TEST_ENV}

# Generate the HTML documentation.
doxygen Doxyfile
cp docs/resize.js docs/html/-
