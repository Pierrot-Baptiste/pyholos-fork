# default_enums.py
# This script contains default values for enums classes to use when instanciating a Farm with create_farm function
from pyholos.farm.enums import (ResidueInputCalculationMethod,
                                SoilDataAcquisitionMethod,
                                ChosenClimateAcquisition,
                                YieldAssignmentMethod,
                                CarbonModellingStrategies)


class DefaultEnums:
    ResidueInputCalculationMethod = ResidueInputCalculationMethod.Default
    SoilDataAcquisitionMethod = SoilDataAcquisitionMethod.Default
    ChosenClimateAcquisition = ChosenClimateAcquisition.NASA
    YieldAssignmentMethod = YieldAssignmentMethod.SmallAreaData
    CarbonModellingStrategies = CarbonModellingStrategies.ICBM
