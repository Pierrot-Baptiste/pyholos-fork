from datetime import date
from abc import ABC
from typing import Literal, Any, ClassVar
from dataclasses import dataclass, field

from pyholos.common import EnumGeneric
from pyholos.components.animals.common import (
    AnimalComponent,
    AnimalType,
    Bedding,
    BeddingMaterialType,
    Diet,
    DietAdditiveType,
    HousingType,
    LivestockEmissionConversionFactorsData,
    ManureStateType,
    Milk,
    ProductionStage,
    get_beef_and_dairy_cattle_coefficient_data,
    get_beef_and_dairy_cattle_feeding_activity_coefficient,
    get_default_methane_producing_capacity_of_manure,
    get_fraction_of_organic_nitrogen_mineralized_data,
    get_ammonia_emission_factor_for_storage_of_beef_and_dairy_cattle_manure
)
from pyholos.utils import convert_camel_case_to_space_delimited


@dataclass
class GroupNameInfo:
    """Group name info.  Used to generate group names from the animal type.
    Not super useful and we might want more control on group names."""
    group_type: AnimalType
    group_name: str = field(init=False)

    def __post_init__(self):
        self.group_name = convert_camel_case_to_space_delimited(
            s=self.group_type.value.replace('Cow', '')
        ).capitalize()


class GroupNameType(EnumGeneric):
    """Group name types.  Enum for different implemented groups.
    We might want to simply remove restriction on what group we can make as it is
    not a restriction in Holos."""
    dairy_heifers = GroupNameInfo(group_type=AnimalType.dairy_heifers)
    dairy_lactating_cow = GroupNameInfo(group_type=AnimalType.dairy_lactating_cow)
    dairy_calves = GroupNameInfo(group_type=AnimalType.dairy_calves)
    dairy_dry_cow = GroupNameInfo(group_type=AnimalType.dairy_dry_cow)


# Constant that contains every columns the final CSVs need to have for this component.
# Might be interresting to regroup columns that are shared between all animals components.
DAIRY_COMPONENT_HOLOS_VAR: tuple[tuple[str, str, Any], ...] = (
    # (attribute_name, holos_name, value)   value can be a callable here
    ("name", "Name", "Dairy cattle"),
    ("component_type", "Component Type", "H.Core.Models.Animals.Dairy.DairyComponent"),
    ("group_name", "Group Name", None),
    ("group_type", "Group Type", None),
    ("management_period_name", "Management Period Name", None),
    ("management_period_start_date", "Management Period Start Date", None),
    ("management_period_days", "Management Period Days", None),
    ("number_of_animals", "Number Of Animals", None),
    ("production_stage", "Production Stage", None),
    ("number_of_young_animals", "Number Of Young Animals", None),
    ("group_pairing_number", "Group Pairing Number", None),
    ("start_weight", "Start Weight", None),
    ("end_weight", "End Weight", None),
    ("average_daily_gain", "Average Daily Gain", None),
    ("milk_production", "Milk Production", None),
    ("milk_fat_content", "Milk Fat Content", None),
    ("milk_protein_content_as_percentage", "Milk Protein Content As Percentage", None),
    ("diet_additive_type", "Diet Additive Type", None),
    ("methane_conversion_factor_of_diet", "Methane Conversion Factor Of Diet", None),
    ("methane_conversion_factor_adjusted", "Methane Conversion Factor Adjusted", 0),
    ("feed_intake", "Feed Intake", 0),
    ("crude_protein", "Crude Protein", None),
    ("ash_content_of_diet", "Ash Content Of Diet", None),
    ("forage", "Forage", None),
    ("tdn", "TDN", None),
    ("starch", "Starch", None),
    ("fat", "Fat", None),
    ("me", "ME", None),
    ("ndf", "NDF", None),
    ("volatile_solid_adjusted", "Volatile Solid Adjusted", 1),
    ("nitrogen_excretion_adjusted", "Nitrogen Excretion Adjusted", 1),
    ("dietary_net_energy_concentration", "Dietary Net Energy Concentration", None),
    ("gain_coefficient", "Gain Coefficient", None),
    ("gain_coefficient_a", "Gain Coefficient A", 0),
    ("gain_coefficient_b", "Gain Coefficient B", 0),
    ("housing_type", "Housing Type", None),
    ("activity_coefficient_of_feeding_situation", "Activity Coefficient Of Feeding Situation", None),
    ("maintenance_coefficient", "Maintenance Coefficient", None),
    ("user_defined_bedding_rate", "User Defined Bedding Rate", None),
    ("total_carbon_kilograms_dry_matter_for_bedding", "Total Carbon Kilograms Dry Matter For Bedding", None),
    ("total_nitrogen_kilograms_dry_matter_for_bedding", "Total Nitrogen Kilograms Dry Matter For Bedding", None),
    ("moisture_content_of_bedding_material", "Moisture Content Of Bedding Material", None),
    ("indoor_barn_temperature", "Indoor Barn Temperature", None),
    ("methane_conversion_factor_of_manure", "Methane Conversion Factor Of Manure", None),
    ("n2o_direct_emission_factor", "N2O Direct Emission Factor", None),
    ("emission_factor_volatilization", "Emission Factor Volatilization", None),
    ("volatilization_fraction", "Volatilization Fraction", None),
    ("emission_factor_leaching", "Emission Factor Leaching", None),
    ("fraction_leaching", "Fraction Leaching", None),
    ("ash_content", "Ash Content", 8.0),
    ("methane_producing_capacity_of_manure", "Methane Producing Capacity Of Manure", None),
    ("fraction_of_organic_nitrogen_immobilized", "Fraction Of Organic Nitrogen Immobilized", None),
    ("fraction_of_organic_nitrogen_nitrified", "Fraction Of Organic Nitrogen Nitrified", None),
    ("fraction_of_organic_nitrogen_mineralized", "Fraction Of Organic Nitrogen Mineralized", None),
    ("manure_state_type", "Manure State Type", None),
    ("ammonia_emission_factor_for_manure_storage", "Ammonia Emission Factor For Manure Storage", None),
    ("use_custom_indoor_housing_temperature", "Use Custom Indoor Housing Temperature", False),
)


class DairyBase(AnimalComponent):
    ANIMAL_COMPONENT_HOLOS_VAR: ClassVar[tuple[tuple[str, str, Any], ...]] = DAIRY_COMPONENT_HOLOS_VAR


@dataclass
class Dairy(DairyBase, ABC):
    """
    Base class for dairy animals. This class is not meant to be used directly.
    Required inputs are passed to the constructor, and the post_init method is used
    to generate the remaining attributes.

    Note: I believe this class should not be abstract anymore and become the only class.
        the restriction to predefined animal types is arbitrary and should be removed.

    Args:
        management_period_name: given name for the management period
        group_pairing_number: number of paired animals
        management_period_start_date: starting date for the management period
        management_period_days: number of days of the management period
        number_of_animals: number of animals
        production_stage: ProductionStage class instance
        number_of_young_animals: number of young animals
        milk_data: class object that contains all required milk production data
        diet: class object that contains all required diet data
        housing_type: HousingType class instance
        manure_handling_system: ManureStateType class instance
        manure_emission_factors: LivestockEmissionConversionFactorsData class instance
        start_weight: (kg) animal weight at the beginning of the management period
        end_weight: (kg) animal weight at the end of the management period
        diet_additive_type: type of the diet additive
        bedding_material_type: bedding material type
    """

    animal_group: ClassVar[GroupNameInfo]

    management_period_name: str
    group_pairing_number: int
    management_period_start_date: date
    management_period_days: int
    number_of_animals: float
    production_stage: ProductionStage
    number_of_young_animals: int
    milk_data: Milk
    diet: Diet
    housing_type: HousingType
    manure_handling_system: ManureStateType
    manure_emission_factors: LivestockEmissionConversionFactorsData
    start_weight: float | None = None
    end_weight: float | None = None
    average_daily_gain: float | None = None
    diet_additive_type: DietAdditiveType = DietAdditiveType.NONE
    bedding_material_type: BeddingMaterialType = BeddingMaterialType.NONE
    indoor_barn_temperature: float | Literal["N/A"] = "N/A"

    def get_animal_coefficient_data(self):
        """Retreives Table 16 livestock coefficients for beef cattle and dairy cattle."""
        self._animal_coefficient_data = get_beef_and_dairy_cattle_coefficient_data(
            animal_type=self.group_type
        )

    def set_feeding_activity_coefficient(self):
        """Retreives coefficient related to feeding activity."""
        self.activity_coefficient_of_feeding_situation = get_beef_and_dairy_cattle_feeding_activity_coefficient(
            housing_type=self.housing_type
        )

    def __post_init__(self):
        super().__init__()
        self.group_name = self.animal_group.group_name
        self.group_type = self.animal_group.group_type

        self.get_animal_coefficient_data()

        self.maintenance_coefficient = self._animal_coefficient_data.baseline_maintenance_coefficient
        self.gain_coefficient = self._animal_coefficient_data.gain_coefficient

        if self.start_weight is None:
            self.start_weight = self._animal_coefficient_data.default_initial_weight

        if self.end_weight is None:
            self.end_weight = self._animal_coefficient_data.default_final_weight

        if self.average_daily_gain is None:
            self.average_daily_gain = (
                self.end_weight - self.start_weight
            ) / self.management_period_days

        self.milk_production = self.milk_data.production
        self.milk_fat_content = self.milk_data.fat_content
        self.milk_protein_content_as_percentage = self.milk_data.protein_content_as_percentage

        self.crude_protein = self.diet.crude_protein_percentage
        self.forage = self.diet.forage_percentage
        self.tdn = self.diet.total_digestible_nutrient_percentage
        self.ash_content_of_diet = self.diet.ash_percentage
        self.starch = self.diet.starch_percentage
        self.fat = self.diet.fat_percentage
        self.me = self.diet.metabolizable_energy
        self.ndf = self.diet.neutral_detergent_fiber_percentage

        self.dietary_net_energy_concentration = self.diet.calc_dietary_net_energy_concentration_for_beef()
        self.methane_conversion_factor_of_diet = self.diet.calc_methane_conversion_factor(
            animal_type=self.group_type
        )

        bedding = Bedding(
            housing_type=self.housing_type,
            bedding_material_type=self.bedding_material_type,
            animal_type=self.group_type
        )

        self.user_defined_bedding_rate = bedding.user_defined_bedding_rate.value
        self.total_carbon_kilograms_dry_matter_for_bedding = (
            bedding.total_carbon_kilograms_dry_matter_for_bedding.value
        )
        self.total_nitrogen_kilograms_dry_matter_for_bedding = (
            bedding.total_nitrogen_kilograms_dry_matter_for_bedding.value
        )
        self.moisture_content_of_bedding_material = bedding.moisture_content_of_bedding_material.value

        self.set_feeding_activity_coefficient()

        self.methane_producing_capacity_of_manure = get_default_methane_producing_capacity_of_manure(
            is_pasture=self.housing_type.is_pasture(),
            animal_type=self.group_type
        )
        fraction_of_organic_nitrogen_mineralized_data = get_fraction_of_organic_nitrogen_mineralized_data(
            state_type=self.manure_handling_system,
            animal_type=self.group_type
        )

        self.manure_state_type = self.manure_handling_system
        self.fraction_of_organic_nitrogen_immobilized = (
            fraction_of_organic_nitrogen_mineralized_data.fraction_immobilized
        )
        self.fraction_of_organic_nitrogen_nitrified = (
            fraction_of_organic_nitrogen_mineralized_data.fraction_nitrified
        )
        self.fraction_of_organic_nitrogen_mineralized = (
            fraction_of_organic_nitrogen_mineralized_data.fraction_mineralized
        )

        self.ammonia_emission_factor_for_manure_storage = (
            get_ammonia_emission_factor_for_storage_of_beef_and_dairy_cattle_manure(
                storage_type=self.manure_handling_system
            )
        )

        self.use_custom_indoor_housing_temperature = False if self.indoor_barn_temperature == "N/A" else True

        self.methane_conversion_factor_of_manure = self.manure_emission_factors.MethaneConversionFactor
        self.n2o_direct_emission_factor = self.manure_emission_factors.N2ODirectEmissionFactor
        self.volatilization_fraction = self.manure_emission_factors.VolatilizationFraction
        self.emission_factor_volatilization = self.manure_emission_factors.EmissionFactorVolatilization
        self.fraction_leaching = self.manure_emission_factors.LeachingFraction
        self.emission_factor_leaching = self.manure_emission_factors.EmissionFactorLeach

        self.volatile_solid_adjusted = 1
        self.nitrogen_excretion_adjusted = 1
        self.gain_coefficient_a = 0
        self.gain_coefficient_b = 0
        self._fix_holos_vars()


class DairyHeifers(Dairy):
    animal_group = GroupNameType.dairy_heifers.value


class DairyLactatingCow(Dairy):
    animal_group = GroupNameType.dairy_lactating_cow.value


class DairyCalves(Dairy):
    animal_group = GroupNameType.dairy_calves.value


class DairyDryCow(Dairy):
    animal_group = GroupNameType.dairy_dry_cow.value
