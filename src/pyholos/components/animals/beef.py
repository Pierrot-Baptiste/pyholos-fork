from datetime import date
from dataclasses import dataclass, field
from typing import Any, ClassVar

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
    get_ammonia_emission_factor_for_storage_of_beef_and_dairy_cattle_manure,
    get_beef_and_dairy_cattle_coefficient_data,
    get_beef_and_dairy_cattle_feeding_activity_coefficient,
    get_default_methane_producing_capacity_of_manure,
    get_fraction_of_organic_nitrogen_mineralized_data
)
from pyholos.components.common import ComponentType

COMPONENT_TYPE_ROOT = "H.Core.Models.Animals.Beef"


@dataclass
class GroupNameInfo:
    name: str
    component_type: ComponentType
    group_type: AnimalType
    group_name: str


class GroupNameType(EnumGeneric):
    BULLS = GroupNameInfo(
        name="Cow-Calf",
        component_type=ComponentType.cow_calf,
        group_type=AnimalType.beef_bulls,
        group_name="Bulls"
    )
    REPLACEMENT_HEIFERS = GroupNameInfo(
        name="Cow-Calf",
        component_type=ComponentType.cow_calf,
        group_type=AnimalType.beef_replacement_heifers,
        group_name="Replacement heifers"
    )
    COWS = GroupNameInfo(
        name="Cow-Calf",
        component_type=ComponentType.cow_calf,
        group_type=AnimalType.beef_cow_lactating,
        group_name="Cows"
    )
    CALVES = GroupNameInfo(
        name="Cow-Calf",
        component_type=ComponentType.cow_calf,
        group_type=AnimalType.beef_calf,
        group_name="Calves"
    )
    FINISHING_HEIFERS = GroupNameInfo(
        name="Finisher",
        component_type=ComponentType.finishing,
        group_type=AnimalType.beef_finishing_heifer,
        group_name="Heifers"
    )
    FINISHING_STEERS = GroupNameInfo(
        name="Finisher",
        component_type=ComponentType.finishing,
        group_type=AnimalType.beef_finishing_steer,
        group_name="Steers"
    )
    BACKGROUND_HEIFER = GroupNameInfo(
        name="Stockers & Backgrounders",
        component_type=ComponentType.backgrounding,
        group_type=AnimalType.beef_backgrounder_heifer,
        group_name="Heifers"
    )
    BACKGROUND_STEER = GroupNameInfo(
        name="Stockers & Backgrounders",
        component_type=ComponentType.backgrounding,
        group_type=AnimalType.beef_backgrounder_steer,
        group_name="Steers"
    )


BEEF_COMPONENT_HOLOS_VAR: tuple[tuple[str, str, Any], ...] = (
    # (attr_name, holos_name, default)
    ("name", "Name", "Beef"),
    ("component_type", "Component Type", COMPONENT_TYPE_ROOT),
    ("group_name", "Group Name", None),
    ("group_type", "Group Type", None),
    ("management_period_name", "Management Period Name", None),
    ("group_pairing_number", "Group Pairing Number", None),
    ("management_period_start_date", "Management Period Start Date", None),
    ("management_period_days", "Management Period Days", None),
    ("number_of_animals", "Number Of Animals", None),
    ("production_stage", "Production Stage", None),
    ("number_of_young_animals", "Number Of Young Animals", None),
    ("animals_are_milk_fed_only", "Animals Are Milk Fed Only", None),
    ("start_weight", "Start Weight", None),
    ("end_weight", "End Weight", None),
    ("average_daily_gain", "Average Daily Gain", None),
    ("milk_production", "Milk Production", None),
    ("milk_fat_content", "Milk Fat Content", None),
    ("milk_protein_content_as_percentage", "Milk Protein Content As Percentage", None),
    ("diet_additive_type", "Diet Additive Type", None),
    ("methane_conversion_factor_of_diet", "Methane Conversion Factor Of Diet", None),
    ("methane_conversion_factor_adjusted", "Methane Conversion Factor Adjusted", 0),  # deprecated
    ("feed_intake", "Feed Intake", None),
    ("crude_protein", "Crude Protein", None),
    ("forage", "Forage", None),
    ("tdn", "TDN", None),
    ("ash_content_of_diet", "Ash Content Of Diet", None),
    ("starch", "Starch", None),
    ("fat", "Fat", None),
    ("me", "ME", None),
    ("ndf", "NDF", None),
    ("dietary_net_energy_concentration", "Dietary Net Energy Concentration", None),
    ("housing_type", "Housing Type", None),
    ("gain_coefficient", "Gain Coefficient", None),
    ("user_defined_bedding_rate", "User Defined Bedding Rate", None),
    ("total_carbon_kilograms_dry_matter_for_bedding", "Total Carbon Kilograms Dry Matter For Bedding", None),
    ("total_nitrogen_kilograms_dry_matter_for_bedding", "Total Nitrogen Kilograms Dry Matter For Bedding", None),
    ("moisture_content_of_bedding_material", "Moisture Content Of Bedding Material", None),
    ("activity_coefficient_of_feeding_situation", "Activity Coefficient Of Feeding Situation", None),
    ("maintenance_coefficient", "Maintenance Coefficient", None),  # (MJ day⁻¹ kg⁻¹) C_f_adjusted
    ("methane_conversion_factor_of_manure", "Methane Conversion Factor Of Manure", None),
    ("n2o_direct_emission_factor", "N2O Direct Emission Factor", None),
    # (kg N2O-N (kg N)^-1) EF_volatilization
    ("emission_factor_volatilization", "Emission Factor Volatilization", None),
    ("volatilization_fraction", "Volatilization Fraction", None),
    ("emission_factor_leaching", "Emission Factor Leaching", None),
    ("fraction_leaching", "Fraction Leaching", None),
    ("ash_content", "Ash Content", 8.0),  # deprecated
    ("methane_producing_capacity_of_manure", "Methane Producing Capacity Of Manure", None),
    ("fraction_of_organic_nitrogen_immobilized", "Fraction Of Organic Nitrogen Immobilized", None),
    ("fraction_of_organic_nitrogen_nitrified", "Fraction Of Organic Nitrogen Nitrified", None),
    ("fraction_of_organic_nitrogen_mineralized", "Fraction Of Organic Nitrogen Mineralized", None),
    ("manure_state_type", "Manure State Type", None),
    ("ammonia_emission_factor_for_manure_storage", "Ammonia Emission Factor For Manure Storage", None),
)


class BeefBase(AnimalComponent):
    """Base class for beef components.  Only needs to define the ANIMAL_COMPONENT_HOLOS_VAR class variable."""
    ANIMAL_COMPONENT_HOLOS_VAR: ClassVar[tuple[tuple[str, str, Any], ...]] = BEEF_COMPONENT_HOLOS_VAR


@dataclass
class Beef(BeefBase):
    """
    Args:
        management_period_name: given name for the management period
        group_pairing_number: number of paired animals
        management_period_start_date: starting date for the management period
        management_period_days: number of days of the management period
        number_of_animals: number of animals
        production_stage: ProductionStage class instance
        number_of_young_animals: number of young animals
        is_milk_fed_only: used to indicate when animals are not consuming forage but only milk
            (distinction needed for calculate enteric methane for beef calves)
        milk_data: class object that contains all required milk production data
        diet: class object that contains all required diet data
        housing_type: HousingType class instance
        manure_handling_system: ManureStateType class instance
        manure_emission_factors: LivestockEmissionConversionFactorsData class instance
        diet_additive_type: type of the diet additive
        start_weight: (kg) animal weight at the beginning of the management period
        end_weight: (kg) animal weight at the end of the management period
        bedding_material_type: bedding material type
    """
    animal_group: ClassVar[GroupNameInfo]

    management_period_name: str
    group_pairing_number: int
    management_period_start_date: date
    management_period_days: int
    number_of_animals: int
    production_stage: ProductionStage
    number_of_young_animals: int
    is_milk_fed_only: bool
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
    name: str = field(init=False)
    group_name: str = field(init=False)
    group_type: AnimalType = field(init=False)
    component_type: str = field(init=False)
    animals_are_milk_fed_only: str = field(init=False)

    def get_animal_coefficient_data(self):
        self._animal_coefficient_data = get_beef_and_dairy_cattle_coefficient_data(animal_type=self.group_type)

    def set_feeding_activity_coefficient(
            self,
            housing_type: HousingType
    ):
        self.activity_coefficient_of_feeding_situation = get_beef_and_dairy_cattle_feeding_activity_coefficient(
            housing_type=housing_type)

    def __post_init__(self):
        # TODO: A lot of repetition with Dairy component here. Could centralise the logic of shared work
        super().__init__()
        # Handling of animal group info (defined at class level)
        self.name = f"Beef {self.animal_group.name.strip()}"
        self.group_name = self.animal_group.group_name
        self.group_type = self.animal_group.group_type
        self.component_type = f"{COMPONENT_TYPE_ROOT}.{self.animal_group.component_type.to_str()}"

        self.animals_are_milk_fed_only = str(self.is_milk_fed_only)

        self._animal_coefficient_data = get_beef_and_dairy_cattle_coefficient_data(
            animal_type=self.group_type
        )
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

        self.methane_conversion_factor_adjusted = 0
        self.feed_intake = 0

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

        self.set_feeding_activity_coefficient(housing_type=self.housing_type)

        self.methane_producing_capacity_of_manure = get_default_methane_producing_capacity_of_manure(
            is_pasture=self.housing_type.is_pasture(),
            animal_type=self.group_type)

        fraction_of_organic_nitrogen_mineralized_data = get_fraction_of_organic_nitrogen_mineralized_data(
            state_type=self.manure_handling_system,
            animal_type=self.group_type)

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
                storage_type=self.manure_handling_system))

        self.methane_conversion_factor_of_manure = self.manure_emission_factors.MethaneConversionFactor
        self.n2o_direct_emission_factor = self.manure_emission_factors.N2ODirectEmissionFactor
        self.volatilization_fraction = self.manure_emission_factors.VolatilizationFraction
        self.emission_factor_volatilization = self.manure_emission_factors.EmissionFactorVolatilization
        self.fraction_leaching = self.manure_emission_factors.LeachingFraction
        self.emission_factor_leaching = self.manure_emission_factors.EmissionFactorLeach

        self._fix_holos_vars()


class Bulls(Beef):
    animal_group = GroupNameType.BULLS.value


class ReplacementHeifers(Beef):
    animal_group = GroupNameType.REPLACEMENT_HEIFERS.value


class Cows(Beef):
    animal_group = GroupNameType.COWS.value


class Calves(Beef):
    animal_group = GroupNameType.CALVES.value


class FinishingHeifers(Beef):
    animal_group = GroupNameType.FINISHING_HEIFERS.value


class FinishingSteers(Beef):
    animal_group = GroupNameType.FINISHING_STEERS.value


class BackgrounderHeifer(Beef):
    animal_group = GroupNameType.BACKGROUND_HEIFER.value


class BackgrounderSteer(Beef):
    animal_group = GroupNameType.BACKGROUND_STEER.value
