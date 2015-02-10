#pragma once

#include "CombineTools/interface/CombineHarvester.h"

class HttSystematics {

public:
	static void AddSystematicsETMT(ch::CombineHarvester& cb);
	static void AddSystematicsEM(ch::CombineHarvester& cb);
	static void AddSystematicsEEMM(ch::CombineHarvester& cb);
	static void AddSystematicsTT(ch::CombineHarvester& cb);

};

