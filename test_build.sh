#!/bin/bash

echo "# ================= #"
echo "# Checking wget "
echo "# ================= #"
if ! which wget; then 
    echo "No wget. Will install"; 
    yum install wget -y
    if ! which wget; then 
        echo "Could not get wget"
        exit 1
    fi
else
    echo "wget found:"; 
    which wget;
fi

echo "# ================= #"
echo "# Setting /etc/cvmfs/config.d/cms.cern.ch.local BEFORE the mount "
echo "# ================= #"
    cat /etc/cvmfs/config.d/cms.cern.ch.local || {
    echo "No /etc/cvmfs/config.d/cms.cern.ch.local was found"
    cat >/etc/cvmfs/config.d/cms.cern.ch.local <<EOL
    # Important setting for CMS, jobs will not work properly without!
    # export CMS_LOCAL_SITE=T2_DE_DESY
    export CMS_LOCAL_SITE=/cvmfs/cms.cern.ch/SITECONF/T2_DE_DESY
    # This only needed if you did not configure Squids in /etc/default.[conf|local]
    #CVMFS_HTTP_PROXY="http://<Squid1-url>:<port>|http://<Squid2-url>:<port>[|...]"" > /etc/cvmfs/config.d/cms.cern.ch.local
EOL
    echo "Was created as:"
    cat /etc/cvmfs/config.d/cms.cern.ch.local
    
    echo "and Was soursed as:"
    source /etc/cvmfs/config.d/cms.cern.ch.local
    echo "testing:"
    echo $CMS_LOCAL_SITE
    }
echo 


echo "# ================= #"
echo "# Mounting: run-cvmfs.sh"
echo "# ================= #"
    /etc/cvmfs/run-cvmfs.sh
echo "# ================= #"
echo

echo "# ================= #"
echo "# Find site-local-config.xml"
echo "# ================= #"
    thesite=local
    echo "ls -ltr /cvmfs/cms.cern.ch/SITECONF"
    ls -ltr /cvmfs/cms.cern.ch/SITECONF
    echo
    echo "ls -ltr /cvmfs/cms.cern.ch/SITECONF/${thesite}"
    ls -ltr /cvmfs/cms.cern.ch/SITECONF/$thesite
    echo

    sitelocaltocheck=/cvmfs/cms.cern.ch/SITECONF/$thesite/JobConfig/site-local-config.xml
    #sitelocaltocheck=/cvmfs/cms.cern.ch/SITECONF/local/JobConfig/site-local-config.xml
    printf " cat \"%s\":\n" "$sitelocaltocheck"
    cat $sitelocaltocheck 
    cat $sitelocaltocheck || {
        printf "\n Could not cat  \"%s\".\n" "$sitelocaltocheck"
        exit 1
    } 
    printf "\n Much wow, could cat  \"%s\".\n" "$sitelocaltocheck"
echo "# ================= #"
echo

echo "# ================= #"
echo "# Download and execute checkout script"
echo "# ================= #"
    mkdir -p /home/build && cd /home/build
    curl -O https://raw.githubusercontent.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau/${TRAVIS_BRANCH}/scripts/checkout_packages.sh
    chmod +x checkout_packages.sh
    set -x
    printf "no\n" | . ./checkout_packages.sh -b ${TRAVIS_BRANCH} -g 'greyxray' -e 'greyxray@gmail.com' -n 'test' || {
        echo "checkout_packages.sh could not be executed"
        exit 1
    }

echo "The end"
