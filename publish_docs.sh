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

# Generate the HTML documentation.
doxygen Doxyfile

# Create and commit the documentation repo.
cd ${HTML_PATH}
# create a .nojekyll file to allow html files starting with
# an underscore to be displayed
touch .nojekyll
git add .
git config user.name "${COMMIT_USER}"
git config user.email "${COMMIT_EMAIL}"
git commit -m "Automated documentation build for changeset ${CHANGESET}." || true
git push -f https://${GH_TOKEN}@github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau gh-pages
cd -

