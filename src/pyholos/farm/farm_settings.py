from pathlib import Path
from typing import Any

from pyholos.common import HolosVar
from pyholos.core_constants import CoreConstants
from pyholos.defaults import Defaults
from pyholos.defaults_enums import DefaultEnums
from pyholos.farm.enums import (CarbonModellingStrategies,
                                ChosenClimateAcquisition,
                                YieldAssignmentMethod,
                                ResidueInputCalculationMethod,
                                SoilDataAcquisitionMethod)
from pyholos.soil import set_soil_properties


class FarmSettingsVar(HolosVar):
    def __init__(
            self,
            name: str,
            value: Any
    ):
        super().__init__(
            name=name,
            value=value)

    def to_text(self):
        return f'{self.name} = {self.value}'


class ParamGeneric:
    def __init__(self, title: str):
        self.title = f'# {title}'

    def to_list(self) -> list[str]:
        return [self.title] + [getattr(self, v).to_text() for v in self.__dict__ if
                               (not v.startswith(('title', '_', '__')) and not callable(v))]


class ParamsGeneral(ParamGeneric):
    def __init__(
        self,
        polygon_id: int,
        latitude: float,
        longitude: float,
        yield_assignment_method: YieldAssignmentMethod = YieldAssignmentMethod.SmallAreaData,
        path_to_custom_yield_input_file: str = '',
        use_custom_starting_soil_organic_carbon_value: bool = False,
        starting_soc_value: float = 0,
        residue_input_calculation_method: ResidueInputCalculationMethod = ResidueInputCalculationMethod.Default,
        soil_data_acquisition_method: SoilDataAcquisitionMethod = SoilDataAcquisitionMethod.Default,
        carbon_concentration: float = 0.45,
        emergence_day: int = 141,
        ripening_day: int = 197,
        variance: float | float = 300,
        alfa: float = 0.7,
        decomposition_minimum_temperature: float = -3.78,
        decomposition_maximum_temperature: float = 30,
        moisture_response_function_at_saturation: float = 0.42,
        moisture_response_function_at_wilting_point: float = 0.18,
        **kwargs
    ):
        super().__init__(title="General")

        self.yield_assignment_method = FarmSettingsVar(
            name="Yield Assignment Method", value=yield_assignment_method)
        self.path_to_custom_yield_input_file = FarmSettingsVar(
            name="Path To Custom Yield Input File", value=path_to_custom_yield_input_file
        )
        self.polygon_number = FarmSettingsVar(name="Polygon Number", value=polygon_id)
        self.latitude = FarmSettingsVar(name="Latitude", value=latitude)
        self.Longitude = FarmSettingsVar(name="Longitude", value=longitude)
        self.use_custom_starting_soil_organic_carbon_value = FarmSettingsVar(
            name="Use Custom Starting Soil Organic Carbon Value",
            value=use_custom_starting_soil_organic_carbon_value
        )
        self.starting_soc_value = FarmSettingsVar(name="Starting SOC Value", value=starting_soc_value)
        self.residue_input_calculation_method = FarmSettingsVar(
            name="Residue Input Calculation Method", value=residue_input_calculation_method
        )
        self.soil_data_acquisition_method = FarmSettingsVar(
            name="Soil Data Acquisition Method", value=soil_data_acquisition_method
        )
        self.carbon_concentration = FarmSettingsVar(name="Carbon Concentration  (kg kg^-1)", value=carbon_concentration)
        self.emergence_day = FarmSettingsVar(name="Emergence Day", value=emergence_day)
        self.ripening_day = FarmSettingsVar(name="Ripening Day", value=ripening_day)
        self.variance = FarmSettingsVar(name="Variance", value=variance)
        self.alfa = FarmSettingsVar(name="Alfa", value=alfa)
        self.decomposition_minimum_temperature = FarmSettingsVar(
            name="Decomposition Minimum Temperature  (°C)", value=decomposition_minimum_temperature)
        self.decomposition_maximum_temperature = FarmSettingsVar(
            name="Decomposition Maximum Temperature  (°C) ", value=decomposition_maximum_temperature)
        self.moisture_response_function_at_saturation = FarmSettingsVar(
            name="Moisture Response Function At Saturation", value=moisture_response_function_at_saturation)
        self.moisture_response_function_at_wilting_point = FarmSettingsVar(
            name="Moisture Response Function At Wilting Point", value=moisture_response_function_at_wilting_point)

        pass


class ParamsAnnualCrops(ParamGeneric):
    def __init__(
            self,
            percentage_of_product_returned_to_soil_for_annuals: int | float = 2,
            percentage_of_straw_returned_to_soil_for_annuals: int | float = 100,
            percentage_of_roots_returned_to_soil_for_annuals: int | float = 100,
            **kwargs
    ):
        super().__init__(title="Annual Crops")

        self.percentage_of_product_returned_to_soil_for_annuals = FarmSettingsVar(
            name="Percentage Of Product Returned To Soil For Annuals",
            value=percentage_of_product_returned_to_soil_for_annuals)
        self.percentage_of_straw_returned_to_soil_for_annuals = FarmSettingsVar(
            name="Percentage Of Straw Returned To Soil For Annuals",
            value=percentage_of_straw_returned_to_soil_for_annuals)
        self.percentage_of_roots_returned_to_soil_for_annuals = FarmSettingsVar(
            name="Percentage Of Roots Returned To Soil For Annuals",
            value=percentage_of_roots_returned_to_soil_for_annuals)


class ParamsSilageCrops(ParamGeneric):
    def __init__(
            self,
            percentage_of_product_yield_returned_to_soil_for_silage_crops: int | float = 35,
            percentage_of_roots_returned_to_soil_for_silage_crops: int | float = 100,
            **kwargs
    ):
        super().__init__(title="Silage Crops")

        self.percentage_of_product_yield_returned_to_soil_for_silage_crops = FarmSettingsVar(
            name="Percentage Of Product Yield Returned To Soil For Silage Crops",
            value=percentage_of_product_yield_returned_to_soil_for_silage_crops)
        self.percentage_of_roots_returned_to_soil_for_silage_crops = FarmSettingsVar(
            name="Percentage Of Roots Returned To Soil For Silage Crops",
            value=percentage_of_roots_returned_to_soil_for_silage_crops)


class ParamsCoverCrops(ParamGeneric):
    def __init__(
            self,
            percentage_of_product_yield_returned_to_soil_for_cover_crops: int | float = 100,
            percentage_of_product_yield_returned_to_soil_for_cover_crops_forage: int | float = 35,
            percentage_of_product_yield_returned_to_soil_for_cover_crops_produce: int | float = 0,
            percentage_of_straw_returned_to_soil_for_cover_crops: int | float = 100,
            percentage_of_roots_returned_to_soil_for_cover_crops: int | float = 100,
            **kwargs
    ):
        super().__init__(title="Cover Crops")

        self.percentage_of_product_yield_returned_to_soil_for_cover_crops = FarmSettingsVar(
            name="Percentage Of Product Yield Returned To Soil For Cover Crops",
            value=percentage_of_product_yield_returned_to_soil_for_cover_crops)
        self.percentage_of_product_yield_returned_to_soil_for_cover_crops_forage = FarmSettingsVar(
            name="Percentage Of Product Yield Returned To Soil For Cover Crops Forage",
            value=percentage_of_product_yield_returned_to_soil_for_cover_crops_forage)
        self.percentage_of_product_yield_returned_to_soil_for_cover_crops_produce = FarmSettingsVar(
            name="Percentage Of Product Yield Returned To Soil For Cover Crops Produce",
            value=percentage_of_product_yield_returned_to_soil_for_cover_crops_produce)
        self.percentage_of_straw_returned_to_soil_for_cover_crops = FarmSettingsVar(
            name="Percentage Of Straw Returned To Soil For Cover Crops",
            value=percentage_of_straw_returned_to_soil_for_cover_crops)
        self.percentage_of_roots_returned_to_soil_for_cover_crops = FarmSettingsVar(
            name="Percentage Of Roots Returned To Soil For Cover Crops",
            value=percentage_of_roots_returned_to_soil_for_cover_crops)


class ParamsRootCrops(ParamGeneric):
    def __init__(
            self,
            percentage_of_product_returned_to_soil_for_root_crops: int | float = 0,
            percentage_of_straw_returned_to_soil_for_root_crops: int | float = 100,
            **kwargs
    ):
        super().__init__(title="Root Crops")

        self.percentage_of_product_returned_to_soil_for_root_crops = FarmSettingsVar(
            name="Percentage Of Product Returned To Soil For Root Crops",
            value=percentage_of_product_returned_to_soil_for_root_crops)
        self.percentage_of_straw_returned_to_soil_for_root_crops = FarmSettingsVar(
            name="Percentage Of Straw Returned To Soil For Root Crops",
            value=percentage_of_straw_returned_to_soil_for_root_crops)


class ParamsPerennialCrops(ParamGeneric):
    def __init__(
            self,
            percentage_of_product_returned_to_soil_for_perennials: int | float = 35,
            percentage_of_roots_returned_to_soil_for_perennials: int | float = 100,
            **kwargs
    ):
        super().__init__(title="Perennial Crops")

        self.percentage_of_product_returned_to_soil_for_perennials = FarmSettingsVar(
            name="Percentage Of Product Returned To Soil For Perennials",
            value=percentage_of_product_returned_to_soil_for_perennials)
        self.percentage_of_roots_returned_to_soil_for_perennials = FarmSettingsVar(
            name="Percentage Of Roots Returned To Soil For Perennials",
            value=percentage_of_roots_returned_to_soil_for_perennials)


class ParamsRangeland(ParamGeneric):
    def __init__(
            self,
            percentage_of_product_returned_to_soil_for_rangeland_due_to_harvest_loss: int | float = 35,
            percentage_of_roots_returned_to_soil_for_rangeland: int | float = 100,
            **kwargs
    ):
        super().__init__(title="Rangeland")
        self.percentage_of_product_returned_to_soil_for_rangeland_due_to_harvest_loss = FarmSettingsVar(
            name="Percentage Of Product Returned To Soil For Rangeland Due To Harvest Loss",
            value=percentage_of_product_returned_to_soil_for_rangeland_due_to_harvest_loss)
        self.percentage_of_roots_returned_to_soil_for_rangeland = FarmSettingsVar(
            name="Percentage Of Roots Returned To Soil For Rangeland",
            value=percentage_of_roots_returned_to_soil_for_rangeland)


class ParamsFodderCorn(ParamGeneric):
    def __init__(
            self,
            percentage_of_product_returned_to_soil_for_fodder_corn: int | float = 35,
            percentage_of_roots_returned_to_soil_for_fodder_corn: int | float = 100,
            decomposition_rate_constant_young_pool: float = 0.8,
            decomposition_rate_constant_old_pool: float = 0.00605,
            old_pool_carbon_n: float = 0.1,
            no_ratio: float = 0.1,
            emission_factor_for_leaching_and_runoff: float = 0.011,
            emission_factor_for_volatilization: float = 0.01,
            fraction_of_n_lost_by_volatilization: float = 0.21,
            microbe_death: float = 0.2,
            denitrification: float = 0.5,
            carbon_modelling_strategy: CarbonModellingStrategies = CarbonModellingStrategies.ICBM,
            run_in_period_years: int = 15,
            **kwargs
    ):
        super().__init__(title="Fodder Corn")
        self.percentage_of_product_returned_to_soil_for_fodder_corn = FarmSettingsVar(
            name="Percentage Of Product Returned To Soil For Fodder Corn",
            value=percentage_of_product_returned_to_soil_for_fodder_corn)
        self.percentage_of_roots_returned_to_soil_for_fodder_corn = FarmSettingsVar(
            name="Percentage Of Roots Returned To Soil For Fodder Corn",
            value=percentage_of_roots_returned_to_soil_for_fodder_corn)
        self.decomposition_rate_constant_young_pool = FarmSettingsVar(
            name="Decomposition Rate Constant Young Pool",
            value=decomposition_rate_constant_young_pool)
        self.decomposition_rate_constant_old_pool = FarmSettingsVar(
            name="Decomposition Rate Constant Old Pool",
            value=decomposition_rate_constant_old_pool)
        self.old_pool_carbon_n = FarmSettingsVar(
            name="Old Pool Carbon N",
            value=old_pool_carbon_n)
        self.no_ratio = FarmSettingsVar(
            name="NO Ratio",
            value=no_ratio)
        self.emission_factor_for_leaching_and_runoff = FarmSettingsVar(
            name="Emission Factor For Leaching And Runoff  (kg N2O-N (kg N)^-1)",
            value=emission_factor_for_leaching_and_runoff)
        self.emission_factor_for_volatilization = FarmSettingsVar(
            name="Emission Factor For Volatilization  (kg N2O-N (kg N)^-1)",
            value=emission_factor_for_volatilization)
        self.fraction_of_n_lost_by_volatilization = FarmSettingsVar(
            name="Fraction Of N Lost By Volatilization",
            value=fraction_of_n_lost_by_volatilization)
        self.microbe_death = FarmSettingsVar(
            name="Microbe Death",
            value=microbe_death)
        self.denitrification = FarmSettingsVar(
            name="Denitrification",
            value=denitrification)
        self.carbon_modelling_strategy = FarmSettingsVar(
            name="Carbon modelling strategy",
            value=carbon_modelling_strategy)
        self.run_in_period_years = FarmSettingsVar(
            name="Run In Period Years",
            value=run_in_period_years)


class ParamsIcbm(ParamGeneric):
    def __init__(
            self,
            humification_coefficient_above_ground: float = 0.125,
            humification_coefficient_below_ground: float = 0.3,
            humification_coefficient_manure: float = 0.31,
            climate_filename: str = "climate.csv",
            climate_data_acquisition: ChosenClimateAcquisition = ChosenClimateAcquisition.NASA,
            use_climate_parameter_instead_of_management_factor: bool = True,
            enable_carbon_modelling: bool = True,
            **kwargs
    ):
        super().__init__(title="ICBM/Climate")
        self.humification_coefficient_above_ground = FarmSettingsVar(
            name="Humification Coefficient Above Ground",
            value=humification_coefficient_above_ground)
        self.humification_coefficient_below_ground = FarmSettingsVar(
            name="Humification Coefficient Below Ground",
            value=humification_coefficient_below_ground)
        self.humification_coefficient_manure = FarmSettingsVar(
            name="Humification Coefficient Manure",
            value=humification_coefficient_manure)
        self.climate_filename = FarmSettingsVar(
            name="Climate filename",
            value=climate_filename)
        self.climate_data_acquisition = FarmSettingsVar(
            name="Climate Data Acquisition",
            value=climate_data_acquisition)
        self.use_climate_parameter_instead_of_management_factor = FarmSettingsVar(
            name="Use climate parameter instead of management factor",
            value=use_climate_parameter_instead_of_management_factor)
        self.enable_carbon_modelling = FarmSettingsVar(
            name="Enable Carbon Modelling",
            value=enable_carbon_modelling)


class MonthlyWeather(ParamGeneric):
    def __init__(
            self,
            title: str,
            variable_name: str,
            variable_monthly_values: list[int | float],
            months_of_growing_season: tuple[str, ...] = ("may", "june", "july", "august", "september", "october"),
            **kwargs
    ):
        super().__init__(title=title)

        self._months_of_growing_season = months_of_growing_season
        self._months = ["january", "february", "march", "april", "may", "june",
                        "july", "august", "september", "october", "november", "december"]
        for month, value in zip(self._months, variable_monthly_values):
            setattr(self, month, FarmSettingsVar(name=f'{month.capitalize()} {variable_name}', value=value))

    def calc_seasonal_sum(self) -> float:
        return sum([getattr(self, month).value for month in self._months_of_growing_season])

    def calc_seasonal_average(self) -> float:
        return self.calc_seasonal_sum() / len(self._months_of_growing_season)

    def calc_annual_sum(self) -> float:
        return sum([getattr(self, month).value for month in self._months])

    def calc_annual_average(self) -> float:
        return sum([getattr(self, month).value for month in self._months]) / 12.


class ParamsSoil(ParamGeneric):
    def __init__(
            self,
            year: int,
            **kwargs
    ):
        super().__init__(title="Soil Data")

        self.province = FarmSettingsVar(name="Province", value=kwargs['province'])
        self.year = FarmSettingsVar(name="Year Of Observation", value=year)
        self.ecodistrict_id = FarmSettingsVar(name="Ecodistrict ID", value=kwargs['ecodistrict_id'])
        self.soil_great_group = FarmSettingsVar(
            name="Soil Great Group", value=kwargs['soil_great_group'])
        self.soil_functional_category = FarmSettingsVar(
            name="Soil functional category", value=kwargs['soil_functional_category'])
        self.bulk_density = FarmSettingsVar(
            name="Bulk Density", value=kwargs['bulk_density'])
        self.soil_texture = FarmSettingsVar(
            name="Soil Texture", value=kwargs['soil_texture'])
        self.soil_ph = FarmSettingsVar(
            name="Soil Ph", value=kwargs['soil_ph'])
        self.top_layer_thickness = FarmSettingsVar(
            name="Top Layer Thickness  (mm)", value=kwargs['top_layer_thickness'])
        self.proportion_of_sand_in_soil = FarmSettingsVar(
            name="Proportion Of Sand In Soil", value=kwargs['sand_proportion'])
        self.proportion_of_clay_in_soil = FarmSettingsVar(
            name="Proportion Of Clay In Soil", value=kwargs['clay_proportion'])
        self.proportion_of_soil_organic_carbon = FarmSettingsVar(
            name="Proportion Of Soil Organic Carbon", value=kwargs['organic_carbon_proportion'])


class ParamsFarmSettings:
    def __init__(
        self,
        # Required parameters
        year: int,
        latitude: float,
        longitude: float,
        monthly_precipitation: list,
        monthly_potential_evapotranspiration: list,
        monthly_temperature: list,

        # General parameters
        yield_assignment_method: YieldAssignmentMethod = DefaultEnums.YieldAssignmentMethod,
        path_to_custom_yield_input_file: str = Defaults.PathToCustomYieldInputFile,
        use_custom_starting_soil_organic_carbon_value: bool = Defaults.UseCustomStartingSoilOrganicCarbonValue,
        starting_soc_value: float = Defaults.StartingSOCValue,
        residue_input_calculation_method: ResidueInputCalculationMethod = DefaultEnums.ResidueInputCalculationMethod,
        soil_data_acquisition_method: SoilDataAcquisitionMethod = DefaultEnums.SoilDataAcquisitionMethod,
        carbon_concentration: float = CoreConstants.CarbonConcentration,
        emergence_day: int = Defaults.EmergenceDay,
        ripening_day: int = Defaults.RipeningDay,
        variance: int | float = Defaults.Variance,
        alfa: float = Defaults.Alfa,
        decomposition_minimum_temperature: float = Defaults.DecompositionMinimumTemperature,
        decomposition_maximum_temperature: float = Defaults.DecompositionMaximumTemperature,
        moisture_response_function_at_saturation: float = Defaults.MoistureResponseFunctionAtSaturation,
        moisture_response_function_at_wilting_point: float = Defaults.MoistureResponseFunctionAtWiltingPoint,

        # Annual Crops parameters
        percentage_of_product_returned_to_soil_for_annuals: int | float = (
            Defaults.PercentageOfProductReturnedToSoilForAnnuals
        ),
        percentage_of_straw_returned_to_soil_for_annuals: int | float = (
            Defaults.PercentageOfStrawReturnedToSoilForAnnuals
        ),
        percentage_of_roots_returned_to_soil_for_annuals: int | float = (
            Defaults.PercentageOfRootsReturnedToSoilForAnnuals
        ),

        # Silage Crops parameters
        percentage_of_product_yield_returned_to_soil_for_silage_crops: int | float = (
            Defaults.PercentageOfProductYieldReturnedToSoilForSilageCrops
        ),
        percentage_of_roots_returned_to_soil_for_silage_crops: int | float = (
            Defaults.PercentageOfRootsReturnedToSoilForSilageCrops
        ),

        # Cover Crops parameters
        percentage_of_product_yield_returned_to_soil_for_cover_crops: int | float = (
            Defaults.PercentageOfProductYieldReturnedToSoilForCoverCrops
        ),
        percentage_of_product_yield_returned_to_soil_for_cover_crops_forage: int | float = (
            Defaults.PercentageOfProductYieldReturnedToSoilForCoverCropsForage
        ),
        percentage_of_product_yield_returned_to_soil_for_cover_crops_produce: int | float = (
            Defaults.PercentageOfProductYieldReturnedToSoilForCoverCropsProduce
        ),
        percentage_of_straw_returned_to_soil_for_cover_crops: int | float = (
            Defaults.PercentageOfStrawReturnedToSoilForCoverCrops
        ),
        percentage_of_roots_returned_to_soil_for_cover_crops: int | float = (
            Defaults.PercentageOfRootsReturnedToSoilForCoverCrops
        ),

        # Root Crops parameters
        percentage_of_product_returned_to_soil_for_root_crops: int | float = (
            Defaults.PercentageOfProductReturnedToSoilForRootCrops
        ),
        percentage_of_straw_returned_to_soil_for_root_crops: int | float = (
            Defaults.PercentageOfStrawReturnedToSoilForRootCrops
        ),

        # Perennial Crops parameters
        percentage_of_product_returned_to_soil_for_perennials: int | float = (
            Defaults.PercentageOfProductReturnedToSoilForPerennials
        ),
        percentage_of_roots_returned_to_soil_for_perennials: int | float = (
            Defaults.PercentageOfRootsReturnedToSoilForPerennials
        ),

        # Rangeland parameters
        percentage_of_product_returned_to_soil_for_rangeland_due_to_harvest_loss: int | float = (
            Defaults.PercentageOfProductReturnedToSoilForRangelandDueToHarvestLoss
        ),
        percentage_of_roots_returned_to_soil_for_rangeland: int | float = (
            Defaults.PercentageOfRootsReturnedToSoilForRangeland
        ),

        # Fodder Crops parameters
        percentage_of_product_returned_to_soil_for_fodder_corn: int | float = (
            Defaults.PercentageOfProductReturnedToSoilForFodderCorn
        ),
        percentage_of_roots_returned_to_soil_for_fodder_corn: int | float = (
            Defaults.PercentageOfRootsReturnedToSoilForFodderCorn
        ),
        decomposition_rate_constant_young_pool: float = Defaults.DecompositionRateConstantYoungPool,
        decomposition_rate_constant_old_pool: float = Defaults.DecompositionRateConstantOldPool,
        old_pool_carbon_n: float = Defaults.OldPoolCarbonN,
        no_ratio: float = Defaults.NORatio,
        emission_factor_for_leaching_and_runoff: float = Defaults.EmissionFactorForLeachingAndRunoff,
        emission_factor_for_volatilization: float = Defaults.EmissionFactorForVolatilization,
        fraction_of_n_lost_by_volatilization: float = Defaults.FractionOfNLostByVolatilization,
        microbe_death: float = Defaults.MicrobeDeath,
        denitrification: float = Defaults.Denitrification,
        carbon_modelling_strategy: CarbonModellingStrategies = DefaultEnums.CarbonModellingStrategies,
        run_in_period_years: int = Defaults.DefaultRunInPeriod,

        # ICBM/Climate parameters
        humification_coefficient_above_ground: float = Defaults.HumificationCoefficientAboveGround,
        humification_coefficient_below_ground: float = Defaults.HumificationCoefficientBelowGround,
        humification_coefficient_manure: float = Defaults.HumificationCoefficientManure,
        climate_filename: str = Defaults.ClimateFilename,
        climate_data_acquisition: ChosenClimateAcquisition = DefaultEnums.ChosenClimateAcquisition,
        use_climate_parameter_instead_of_management_factor: bool = (
            Defaults.UseClimateParameterInsteadOfManagementFactor
        ),
        enable_carbon_modelling: bool = Defaults.EnableCarbonModelling,
    ):
        """
        ParamsFarmSettings assembles all the necessary parameters to generate a Holos-compatible Farm.settings file
        used for carbon and GHG modeling at the farm level.

        This class organizes parameters into thematic blocks (General, Crop-specific, Climate, Soil, etc.) and
        automatically distributes them to the corresponding section classes via `**kwargs`. It supports flexible
        configuration while preserving the expected structure and order of the output file.

        Args:
            year (int): Year of soil observation.
            latitude (float): Latitude of the farm centroid (decimal degrees).
            longitude (float): Longitude of the farm centroid (decimal degrees).
            monthly_precipitation (list): Monthly precipitation values (mm) for each month of the year.
            monthly_potential_evapotranspiration (list): Monthly potential evapotranspiration values (mm).
            monthly_temperature (list): Monthly average air temperature values (°C).

            yield_assignment_method (YieldAssignmentMethod): Method used to assign crop yield.
            path_to_custom_yield_input_file (str): Path to a custom yield input file, if applicable.
            use_custom_starting_soil_organic_carbon_value (bool): Whether to use a custom starting SOC value.
            starting_soc_value (float): Initial soil organic carbon value.
            residue_input_calculation_method (ResidueInputCalculationMethod): Method for calculating crop residue input.
            soil_data_acquisition_method (SoilDataAcquisitionMethod): Method for acquiring soil data.

            carbon_concentration (float): Soil carbon concentration (kg/kg).
            emergence_day (int): Julian day of crop emergence.
            ripening_day (int): Julian day of crop ripening.
            variance (float): Width of the crop growth distribution function.
            alfa (float): Minimum water storage fraction at wilting point.
            decomposition_minimum_temperature (float): Minimum temperature for decomposition (°C).
            decomposition_maximum_temperature (float): Maximum temperature for decomposition (°C).
            moisture_response_function_at_saturation (float): Moisture response at saturation.
            moisture_response_function_at_wilting_point (float): Moisture response at wilting point.

            percentage_of_product_returned_to_soil_for_annuals (float):
                Percentage of annual crop product returned to soil.
            percentage_of_straw_returned_to_soil_for_annuals (float): Percentage of annual crop straw returned to soil.
            percentage_of_roots_returned_to_soil_for_annuals (float): Percentage of annual crop roots returned to soil.

            percentage_of_product_yield_returned_to_soil_for_silage_crops (float):
                Percentage of silage crop product returned to soil.
            percentage_of_roots_returned_to_soil_for_silage_crops (float):
                Percentage of silage crop roots returned to soil.

            percentage_of_product_yield_returned_to_soil_for_cover_crops (float):
                Percentage of cover crop product returned to soil.
            percentage_of_product_yield_returned_to_soil_for_cover_crops_forage (float):
                Percentage of forage cover crop product returned to soil.
            percentage_of_product_yield_returned_to_soil_for_cover_crops_produce (float):
                Percentage of produce cover crop product returned to soil.
            percentage_of_straw_returned_to_soil_for_cover_crops (float):
                Percentage of cover crop straw returned to soil.
            percentage_of_roots_returned_to_soil_for_cover_crops (float):
                Percentage of cover crop roots returned to soil.

            percentage_of_product_returned_to_soil_for_root_crops (float):
                Percentage of root crop product returned to soil.
            percentage_of_straw_returned_to_soil_for_root_crops (float): Percentage of root crop straw returned to soil.

            percentage_of_product_returned_to_soil_for_perennials (float):
                Percentage of perennial crop product returned to soil.
            percentage_of_roots_returned_to_soil_for_perennials (float): Percentage of perennial

            percentage_of_product_returned_to_soil_for_rangeland_due_to_harvest_loss (float):
                Percentage of rangeland product returned to soil due to harvest loss.
            percentage_of_roots_returned_to_soil_for_rangeland (float): Percentage of rangeland roots returned to soil.

            percentage_of_product_returned_to_soil_for_fodder_corn (float):
                Percentage of fodder corn product returned to soil.
            percentage_of_roots_returned_to_soil_for_fodder_corn (float):
                Percentage of fodder corn roots returned to soil.
            decomposition_rate_constant_young_pool (float): Decomposition rate constant for the young carbon pool.
            decomposition_rate_constant_old_pool (float): Decomposition rate constant for the old carbon pool.
            old_pool_carbon_n (float): Carbon content of the old carbon pool.
            no_ratio (float): Nitrogen content of the old carbon pool.
            emission_factor_for_leaching_and_runoff (float): Emission factor for leaching and runoff.
            emission_factor_for_volatilization (float): Emission factor for volatilization.
            fraction_of_n_lost_by_volatilization (float): Fraction of N lost by volatilization.
            microbe_death (float): Microbe death rate.
            denitrification (float): Denitrification rate.
            carbon_modelling_strategy (CarbonModellingStrategies):
                Strategy used for carbon modeling (e.g., ICBM or IPCCTier2).
            run_in_period_years (int): Number of simulation years for carbon modeling.

            humification_coefficient_above_ground (float): Humification coefficient for above-ground biomass.
            humification_coefficient_below_ground (float): Humification coefficient for below-ground biomass.
            humification_coefficient_manure (float): Humification coefficient for manure.
            climate_filename (str): Filename of the climate data CSV.
            climate_data_acquisition (ChosenClimateAcquisition): Source of climate data (e.g., NASA, custom).
            use_climate_parameter_instead_of_management_factor (bool):
                Whether to use climate parameters instead of management factors.
            enable_carbon_modelling (bool): Whether to enable carbon modeling.

        Notes:
            - Parameters are automatically passed to section classes using `**kwargs`.
            - The order of sections in the output file is controlled by the order in which the attributes are defined
              in this class.
            - Default values are centralized in the `Defaults` and `DefaultEnums` modules for maintainability.
        """

        kwargs = {k: v for k, v in locals().items() if all([not k.startswith(('_', '__', 'self')), not callable(k)])}

        soil_properties = set_soil_properties(
            latitude=latitude,
            longitude=longitude)

        self.params_general = ParamsGeneral(
            polygon_id=soil_properties.pop('id_polygon'),
            **kwargs)

        # Annual Crops
        self.params_annual_crops = ParamsAnnualCrops(**kwargs)

        # Silage Crops
        self.params_silage_crops = ParamsSilageCrops(**kwargs)

        # Cover Crops
        self.params_cover_crops = ParamsCoverCrops(**kwargs)

        # Root crops
        self.params_root_crops = ParamsRootCrops(**kwargs)

        # Perennial Crops
        self.params_perennial_crops = ParamsPerennialCrops(**kwargs)

        # Rangeland
        self.params_rangeland = ParamsRangeland(**kwargs)

        # Fodder Corn
        self.params_fodder_corn = ParamsFodderCorn(**kwargs)

        # ICBM/Climate
        self.params_icbm = ParamsIcbm(**kwargs)

        # Precipitation Data (mm)
        self.params_weather_precipitation = MonthlyWeather(
            title="Precipitation Data (mm)",
            variable_name="Precipitation",
            variable_monthly_values=[int(round(v, 0)) for v in monthly_precipitation])

        # Precipitation Data (mm)
        self.params_weather_potential_evapotranspiration = MonthlyWeather(
            title="Evapotranspiration Data (mm year^-1)",
            variable_name="Potential Evapotranspiration",
            variable_monthly_values=[int(round(v, 0)) for v in monthly_potential_evapotranspiration])

        # Temperature Data (°C)
        self.params_weather_temperature = MonthlyWeather(
            title="Temperature Data (°C)",
            variable_name="Mean Temperature",
            variable_monthly_values=[round(v, 2) for v in monthly_temperature])

        # Soil Data
        self.params_soil = ParamsSoil(
            year=year,
            **soil_properties)

        self._file_name = "Farm.settings"

    def get_params(self) -> list[ParamGeneric]:
        return [getattr(self, v) for v in self.__dict__ if all([not v.startswith(('_', '__')), not callable(v)])]

    def _get_data(self) -> list[str]:
        sections = self.get_params()
        return [x for y in [v.to_list() + [''] for v in sections[:-1]] for x in y] + sections[-1].to_list()

    def write(self, path_dir_farm: Path):
        res = self._get_data()
        with (path_dir_farm / self._file_name).open(mode='w', encoding='utf-8') as f:
            f.writelines('\n'.join(res))
        pass

    def export_to_dict(self) -> dict[str, list[str]]:
        return {self._file_name: self._get_data()}
