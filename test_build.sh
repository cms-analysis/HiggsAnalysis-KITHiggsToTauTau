#!/bin/bash
echo "what is 0: $0"
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


if [ "$ADDITIONAL_OUTPUT" = true ]; then
    echo "# ================= #"
    echo "# Environment checks "
    echo "# ================= #"
        # echo
        # echo "# very specific tests of input files"
        # echo "Testing most probably included in the image files"
        # echo "1) /etc/yum.repos.d/cernvm.repo "
        # cat /etc/yum.repos.d/cernvm.repo
        # echo

        echo ":: /etc/cvmfs/default.local"
        cat /etc/cvmfs/default.local
        echo

        echo ":: /etc/cvmfs/domain.d/cern.ch.local"
        cat /etc/cvmfs/domain.d/cern.ch.local
        echo 

        echo ":: CMS_LOCAL_SITE"
        echo $CMS_LOCAL_SITE
        echo

        # echo ":: /etc/cvmfs/keys"
        # cat /etc/cvmfs/keys
        # echo

        # echo "/etc/cvmfs/run-cvmfs.sh"
        # cat /etc/cvmfs/run-cvmfs.sh
        # echo

        # echo "# ================= #"
        # echo "# ls cvmfs"
        # echo "# ================= #"
        # ls /etc/cvmfs/
        # echo

        echo ":: /etc/cvmfs/run-cvmfs.sh"
        cat /etc/cvmfs/run-cvmfs.sh
        echo
    echo "# ================= #"
    echo
fi


echo "# ================= #"
echo "# Mounting: run-cvmfs.sh"
echo "# ================= #"
    /etc/cvmfs/run-cvmfs.sh
echo "# ================= #"
echo


if [ "$ADDITIONAL_OUTPUT" = true ]; then
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
fi


# export SCRAM_ARCH=slc6_amd64_gcc481
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
if [ "$ADDITIONAL_OUTPUT" = true ]; then
    echo "# ================= #"
    echo "# cmsset_default.sh"
    echo "# ================= #"
        cat $VO_CMS_SW_DIR/cmsset_default.sh
    echo "# ================= #"
    echo
    echo "number of processors:"
    cat /proc/cpuinfo | awk '/^processor/{print $3}'
    echo
fi

echo "# ================= #"
echo "# curl -O root files"
echo "# ================= #"
    files=(/home/short/*)
    if [ ! ${#files[@]} -gt 0 ]
    then
        echo "curl -o /home/short_rootfiles.tar https://cernbox.cern.ch/index.php/s/WeawecKp2BD2BH2/download" # single file: curl -O https://cernbox.cern.ch/index.php/s/BgWZaBJFB2y4688/download 
        curl -o /home/short_rootfiles.tar https://cernbox.cern.ch/index.php/s/WeawecKp2BD2BH2/download
        echo "tar -xvf /home/short_rootfiles.tar /home/"
        tar -xvf /home/short_rootfiles.tar -C /home/
        echo
        #echo "# ================= #"
        #echo "# xrootd"
        #echo "# ================= #"
        #xrootd -d l -f root://eosuser.cern.ch://eos/user/o/ohlushch/kappatest_inputfiles/input/SUSYGluGluToHToTauTau_M-160_fall15_miniAOD.root
        #root -l root://eosuser.cern.ch://eos/user/o/ohlushch/kappatest_inputfiles/input/SUSYGluGluToHToTauTau_M-160_fall15_miniAOD.root
        #echo
    fi
    if [ "$ADDITIONAL_OUTPUT" = true ]; then
        echo "HOME:" $HOME
        ls $HOME
        echo "Content /home/short:"
        ls /home/short
        echo
        echo "Content /home:"
        ls /home
        echo
        echo "Content ~"
        ls ~
    fi
echo "# ================= #"
echo


echo "# ================= #"
echo "# Download checkout script for Kappa"
echo "# ================= #"
    mkdir -p /home/build && cd /home/build
    curl -O https://raw.githubusercontent.com/KappaAnalysis/Kappa/${KAPPA_BRANCH}/Skimming/scripts/${CHECKOUTSCRIPT}
    chmod +x ${CHECKOUTSCRIPT}
    cat ${CHECKOUTSCRIPT}
    set -x
    printf "no\n" | . ./${CHECKOUTSCRIPT} -b ${KAPPA_BRANCH} -g 'greyxray' -e 'greyxray@gmail.com' -n 'kappa test' || {
        echo "The ${CHECKOUTSCRIPT} could not be executed"
        exit 1
    }
echo "# ================= #"
echo

echo "# ================= #"
echo "# Set CMSSW variables"
echo "# ================= #"
    source $VO_CMS_SW_DIR/cmsset_default.sh;
    echo "cd TEST_CMSSW_VERSION"
    cd $TEST_CMSSW_VERSION/src
    eval `scramv1 runtime -sh`
    cd $CMSSW_BASE/src
echo "# ================= #"
echo

if [ "$ADDITIONAL_OUTPUT" = true ]; then
    echo "# =================== #"
    echo "# Env var checks #"
    echo "# =================== #"
        uname -a
        echo "HOSTNAME=$HOSTNAME"
        echo "SHELL=$SHELL"
        python --version

        echo "python:" $(which python)
        echo "PYTHONSTARTUP=$PYTHONSTARTUP"
        echo "PYTHONPATH=$PYTHONPATH"
        echo "SCRAM_ARCH=$SCRAM_ARCH"
        echo "VO_CMS_SW_DIR=$VO_CMS_SW_DIR"
        echo "CMSSW_VERSION=$CMSSW_VERSION"
        echo "CMSSW_GIT_HASH=$CMSSW_GIT_HASH"
        echo "CMSSW_BASE=$CMSSW_BASE"
        echo "CMSSW_RELEASE_BASE=$CMSSW_RELEASE_BASE"

        echo
    echo "# ================= #"
    echo
fi

echo "# =================== #"
echo "# Cat the Config #"
echo "# =================== #"
    cat $CMSSW_BASE/src/$SKIMMING_SCRIPT || {
        echo "The ${CMSSW_BASE}/src/${SKIMMING_SCRIPT} could not be read"
        exit 1
    }
    #Kappa/Skimming/examples/travis/skim_tutorial1_basic.py
echo "# ================= #"
echo

echo "# =================== #"
echo "# Test python #"
echo "# =================== #"
    cd $CMSSW_BASE/src/Kappa && mkdir kappa_run && cd kappa_run
    python $CMSSW_BASE/src/$SKIMMING_SCRIPT || {
        echo "Possible python syntax error "
        #exit 5
    }
    #Kappa/Skimming/examples/travis/skim_tutorial1_basic.py
    #higgsTauTau/kSkimming_run2_cfg.py
echo "# ================= #"
echo

echo "# =================== #"
echo "# Test cmsRun #"
echo "# =================== #"
    cmsRun $CMSSW_BASE/src/$SKIMMING_SCRIPT || {
        echo "The cmsRun could not be run"
        exit 1
    }
    #Kappa/Skimming/examples/travis/skim_tutorial1_basic.py
    #higgsTauTau/kSkimming_run2_cfg.py
echo "# ================= #"
echo

echo "# =================== #"
echo "# Test Output root file #"
echo "# =================== #"
    ls -l *.root || {
        echo "The root file was not created"
        exit 1
    }
echo "# ================= #"
echo

echo "The end"
#make -C Kappa/DataFormats/test -j2 || exit 1
