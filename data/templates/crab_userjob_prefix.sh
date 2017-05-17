#!/bin/bash

set -x
set -e
ulimit -s unlimited
ulimit -c 0

echo "<FrameworkJobReport>
	<ReadBranches>
	</ReadBranches>
	<PerformanceReport>
		<PerformanceSummary Metric=\\"StorageStatistics\\">
			<Metric Name=\\"Parameter-untracked-bool-enabled\\" Value=\\"true\\"/>
			<Metric Name=\\"Parameter-untracked-bool-stats\\" Value=\\"true\\"/>
			<Metric Name=\\"Parameter-untracked-string-cacheHint\\" Value=\\"application-only\\"/>
			<Metric Name=\\"Parameter-untracked-string-readHint\\" Value=\\"auto-detect\\"/>
			<Metric Name=\\"ROOT-tfile-read-totalMegabytes\\" Value=\\"0\\"/>
			<Metric Name=\\"ROOT-tfile-write-totalMegabytes\\" Value=\\"0\\"/>
		</PerformanceSummary>
	</PerformanceReport>

	<GeneratorInfo>
	</GeneratorInfo>
</FrameworkJobReport>" > FrameworkJobReport.xml

function error_exit
{
	if [ $1 -ne 0 ]; then
		echo "Error with exit code ${1}"
		if [ -e FrameworkJobReport.xml ]
		then
			cat << EOF > FrameworkJobReport.xml.tmp
			<FrameworkJobReport>
			<FrameworkError ExitStatus="${1}" Type="" >
			Error with exit code ${1}
			</FrameworkError>
EOF
			tail -n+2 FrameworkJobReport.xml >> FrameworkJobReport.xml.tmp
			mv FrameworkJobReport.xml.tmp FrameworkJobReport.xml
		else
			cat << EOF > FrameworkJobReport.xml
			<FrameworkJobReport>
			<FrameworkError ExitStatus="${1}" Type="" >
			Error with exit code ${1}
			</FrameworkError>
			</FrameworkJobReport>
EOF
		fi
		exit 0
	fi
}
trap 'error_exit $?' ERR

