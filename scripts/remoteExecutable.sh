#!/bin/bash
#DATASETNICK="DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV"
#FILE_NAMES="/storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_100.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_101.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_52.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_53.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_54.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_55.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_56.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_57.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_58.root /storage/a/friese/skimming/2014-03-05-sync-exercise/DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV/kappa_DoubleMu_PFembedded_Run2012A_22Jan2013_muelec_8TeV_59.root"
#CONFIG="../data/ArtusWrapperConfigs/smHtautau.cfg"
CONFIG="smHtautau.cfg"

COMMAND="HiggsToTauTauAnalysis.py" #Auslesen
COMMAND=$COMMAND" "
COMMAND=$COMMAND"@"$CONFIG
COMMAND=$COMMAND" "
COMMAND=$COMMAND"--nick "$DATASETNICK
COMMAND=$COMMAND" "
COMMAND=$COMMAND"-i "${FILE_NAMES//[,\"]/}
COMMAND=$COMMAND" "
COMMAND=$COMMAND"-s jobconfig.json"

echo "-------------------------------------------------"
echo "Starting main executable with the following command:"
echo $COMMAND
echo "The logfile of this job is called "$DATASETNICK"_job_"$MY_JOBID"_log.txt"
echo "-------------------------------------------------"

LOGFILE=log.txt
touch $LOGFILE


export LD_LIBRARY_PATH=""$PWD:$LD_LIBRARY_PATH""

echo "command:">>$LOGFILE
eval $COMMAND>>$LOGFILE
echo $?>>$LOGFILE
# Execute binary externally
eval "./HiggsToTauTauAnalysis jobconfig.json"

echo "remoteExecutable.sh finished">>$LOGFILE

exit 0

#chmod u+x ini_KITHiggsToTauTauAnalysis.sh
#eval "./ini_KITHiggsToTauTauAnalysis.sh"
#Pfad des artus ini-scripts anpassen

#echo "files in this folder $PWD:">>$LOGFILE
#ls -al>>$LOGFILE

#run ini_KitHiggsToTauTau script?
#echo "Nick:">>$LOGFILE
#echo $DATASETNICK>>$LOGFILE
#echo "Nick without special chars:">>$LOGFILE
#echo ${DATASETNICK//[,\"]/}>>$LOGFILE
#echo $MY_JOBID>>$LOGFILE
#echo "File names:">>$LOGFILE
#echo $FILE_NAMES>>$LOGFILE


