from datetime import date
from abc import ABC
from typing import Any, ClassVar, Literal, Mapping, TypeAliasType
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

type FloatOrNA = float | Literal["N/A"]

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
    dairy_bulls = GroupNameInfo(group_type=AnimalType.dairy_bulls)


# Constant that contains every columns the final CSVs need to have for this component.
# Might be interresting to regroup columns that are shared between all animals components.
DAIRY_COMPONENT_HOLOS_VAR: tuple[tuple[str, str, type | TypeAliasType, Any], ...] = (
    # (attribute_name, holos_name, type, value)   value can be a callable here
    ("name", "Name", str, "Dairy cattle"),
    ("component_type", "Component Type", str, "H.Core.Models.Animals.Dairy.DairyComponent"),
    ("group_name", "Group Name", str, None),
    ("group_type", "Group Type", AnimalType, None),
    ("management_period_name", "Management Period Name", str, None),
    ("management_period_start_date", "Management Period Start Date", date, None),
    ("management_period_days", "Management Period Days", int, None),
    ("number_of_animals", "Number Of Animals", float, None),
    ("production_stage", "Production Stage", ProductionStage, None),
    ("number_of_young_animals", "Number Of Young Animals", int, None),
    ("group_pairing_number", "Group Pairing Number", int, None),
    ("start_weight", "Start Weight", float, None),
    ("end_weight", "End Weight", float, None),
    ("average_daily_gain", "Average Daily Gain", float, None),
    ("milk_production", "Milk Production", float, None),
    ("milk_fat_content", "Milk Fat Content", float, None),
    ("milk_protein_content_as_percentage", "Milk Protein Content As Percentage", float, None),
    ("diet_additive_type", "Diet Additive Type", DietAdditiveType,None),
    ("methane_conversion_factor_of_diet", "Methane Conversion Factor Of Diet", float, None),
    ("methane_conversion_factor_adjusted", "Methane Conversion Factor Adjusted", float, 0),  # Deprecated
    ("feed_intake", "Feed Intake", float, 0),
    ("crude_protein", "Crude Protein", float, None),
    ("ash_content_of_diet", "Ash Content Of Diet", float, None),
    ("forage", "Forage", float, None),
    ("tdn", "TDN", float, None),
    ("starch", "Starch", float, None),
    ("fat", "Fat", float, None),
    ("me", "ME", float, None),
    ("ndf", "NDF", float, None),
    ("volatile_solid_adjusted", "Volatile Solid Adjusted", float, 1),  # Deprecated
    ("nitrogen_excretion_adjusted", "Nitrogen Excretion Adjusted", float, 1),
    ("dietary_net_energy_concentration", "Dietary Net Energy Concentration", float, None),
    ("gain_coefficient", "Gain Coefficient", float, None),
    ("gain_coefficient_a", "Gain Coefficient A", float, 0),
    ("gain_coefficient_b", "Gain Coefficient B", float, 0),
    ("housing_type", "Housing Type", HousingType, None),
    ("activity_coefficient_of_feeding_situation", "Activity Coefficient Of Feeding Situation", float, None),
    ("maintenance_coefficient", "Maintenance Coefficient", float, None),
    ("user_defined_bedding_rate", "User Defined Bedding Rate", float, None),
    ("total_carbon_kilograms_dry_matter_for_bedding", "Total Carbon Kilograms Dry Matter For Bedding", float, None),
    ("total_nitrogen_kilograms_dry_matter_for_bedding", "Total Nitrogen Kilograms Dry Matter For Bedding", float, None),
    ("moisture_content_of_bedding_material", "Moisture Content Of Bedding Material", float, None),
    ("indoor_barn_temperature", "Indoor Barn Temperature", FloatOrNA, "N/A"),
    ("methane_conversion_factor_of_manure", "Methane Conversion Factor Of Manure", float, None),
    ("n2o_direct_emission_factor", "N2O Direct Emission Factor", float, None),
    ("emission_factor_volatilization", "Emission Factor Volatilization", float, None),
    ("volatilization_fraction", "Volatilization Fraction", float, None),
    ("emission_factor_leaching", "Emission Factor Leaching", float, None),
    ("fraction_leaching", "Fraction Leaching", float, None),
    ("ash_content", "Ash Content", float, 8.0),  # Deprecated
    ("methane_producing_capacity_of_manure", "Methane Producing Capacity Of Manure", float, None),
    ("fraction_of_organic_nitrogen_immobilized", "Fraction Of Organic Nitrogen Immobilized", float, None),
    ("fraction_of_organic_nitrogen_nitrified", "Fraction Of Organic Nitrogen Nitrified", float, None),
    ("fraction_of_organic_nitrogen_mineralized", "Fraction Of Organic Nitrogen Mineralized", float, None),
    ("manure_state_type", "Manure State Type", ManureStateType, None),
    ("ammonia_emission_factor_for_manure_storage", "Ammonia Emission Factor For Manure Storage", float, None),
    ("use_custom_indoor_housing_temperature", "Use Custom Indoor Housing Temperature", bool, False),
)

class DairyBase(AnimalComponent):
    ANIMAL_COMPONENT_HOLOS_VAR: ClassVar[tuple[tuple[str, str, type | TypeAliasType, Any], ...]] = DAIRY_COMPONENT_HOLOS_VAR


@dataclass
class Dairy(DairyBase, ABC):
    """
    Base class for dairy animals. This class is not meant to be used directly.
    Required inputs are passed to the constructor, and the post_init method is used
    to generate the remaining attributes.

    Note: I believe this class should not be abstract anymore and become the only class.
        the restriction to predefined animal types is arbitrary and should be removed.
        Or not, the animal types seem to be used in lookup tables.

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
    bedding_material_type: BeddingMaterialType

    holos_overrides: Mapping[str, Any] = field(default_factory=dict)

    group_type: AnimalType = field(init=False)
    start_weight: float = field(init=False)
    end_weight: float = field(init=False)
    indoor_barn_temperature: FloatOrNA = field(init=False)

    def update_holos_var(self, var_name: str, value: Any) -> None:
        """Method to set an attribute to its default value in this class, but checks if holos_overides
        offers an override for the variable first

        Args:
            var_name (str): _description_
            value (Any): _description_
        """
        if var_name not in self.holos_var_names:
            raise KeyError(f"{var_name} is not a valid Holos variable.")
        if var_name in self.holos_overrides:
            value = self.holos_overrides[var_name]
        setattr(self, var_name, value)

    def __post_init__(self):
        super().__init__()
        self.update_holos_var("group_name", self.animal_group.group_name)
        self.update_holos_var("group_type", self.animal_group.group_type)

        """Retreives Table 16 livestock coefficients for beef cattle and dairy cattle."""
        self._animal_coefficient_data = get_beef_and_dairy_cattle_coefficient_data(
            animal_type=self.group_type
        )

        # --- Animal Coefficients ---
        self.update_holos_var("maintenance_coefficient", self._animal_coefficient_data.baseline_maintenance_coefficient)
        self.update_holos_var("gain_coefficient", self._animal_coefficient_data.gain_coefficient)

        # --- Animal Weights & Growth ---
        self.update_holos_var("start_weight", self._animal_coefficient_data.default_initial_weight)
        self.update_holos_var("end_weight", self._animal_coefficient_data.default_final_weight)
        self.update_holos_var("average_daily_gain", (self.end_weight - self.start_weight) / self.management_period_days)

        # --- Milk Production ---
        self.update_holos_var("milk_production", self.milk_data.production)
        self.update_holos_var("milk_fat_content", self.milk_data.fat_content)
        self.update_holos_var("milk_protein_content_as_percentage", self.milk_data.protein_content_as_percentage)

        # --- Diet ---
        self.update_holos_var("crude_protein", self.diet.crude_protein_percentage)
        self.update_holos_var("forage", self.diet.forage_percentage)
        self.update_holos_var("tdn", self.diet.total_digestible_nutrient_percentage)
        self.update_holos_var("ash_content_of_diet", self.diet.ash_percentage)
        self.update_holos_var("starch", self.diet.starch_percentage)
        self.update_holos_var("fat", self.diet.fat_percentage)
        self.update_holos_var("me", self.diet.metabolizable_energy)
        self.update_holos_var("ndf", self.diet.neutral_detergent_fiber_percentage)

        self.update_holos_var(
            "dietary_net_energy_concentration",
            self.diet.calc_dietary_net_energy_concentration_for_beef()
        )
        self.update_holos_var(
            "methane_conversion_factor_of_diet",
            self.diet.calc_methane_conversion_factor(animal_type=self.group_type)
        )

        # --- Bedding ---
        bedding = Bedding(
            housing_type=self.housing_type,
            bedding_material_type=self.bedding_material_type,
            animal_type=self.group_type
        )

        self.update_holos_var("user_defined_bedding_rate", bedding.user_defined_bedding_rate.value)
        self.update_holos_var(
            "total_carbon_kilograms_dry_matter_for_bedding",
            bedding.total_carbon_kilograms_dry_matter_for_bedding.value
        )
        self.update_holos_var(
            "total_nitrogen_kilograms_dry_matter_for_bedding",
            bedding.total_nitrogen_kilograms_dry_matter_for_bedding.value
        )
        self.update_holos_var(
            "moisture_content_of_bedding_material",
            bedding.moisture_content_of_bedding_material.value
        )

        # --- Feeding Activity ---
        """Retreives coefficient related to feeding activity."""
        self.update_holos_var(
            "activity_coefficient_of_feeding_situation",
            get_beef_and_dairy_cattle_feeding_activity_coefficient(housing_type=self.housing_type)
        )

        # --- Manure ---
        self.update_holos_var(
            "methane_producing_capacity_of_manure",
            get_default_methane_producing_capacity_of_manure(
                is_pasture=self.housing_type.is_pasture(),
                animal_type=self.group_type
            )
        )
        fraction_of_organic_nitrogen_mineralized_data = get_fraction_of_organic_nitrogen_mineralized_data(
            state_type=self.manure_handling_system,
            animal_type=self.group_type
        )

        self.update_holos_var("manure_state_type", self.manure_handling_system)
        self.update_holos_var(
            "fraction_of_organic_nitrogen_immobilized",
            fraction_of_organic_nitrogen_mineralized_data.fraction_immobilized
        )
        self.update_holos_var(
            "fraction_of_organic_nitrogen_nitrified",
            fraction_of_organic_nitrogen_mineralized_data.fraction_nitrified
        )
        self.update_holos_var(
            "fraction_of_organic_nitrogen_mineralized",
            fraction_of_organic_nitrogen_mineralized_data.fraction_mineralized
        )
        self.update_holos_var(
            "ammonia_emission_factor_for_manure_storage",
            get_ammonia_emission_factor_for_storage_of_beef_and_dairy_cattle_manure(
                storage_type=self.manure_handling_system
            )
        )

        self.update_holos_var("indoor_barn_temperature", "N/A")
        self.update_holos_var("use_custom_indoor_housing_temperature", False if self.indoor_barn_temperature == "N/A" else True)

        self.update_holos_var("methane_conversion_factor_of_manure", self.manure_emission_factors.MethaneConversionFactor)
        self.update_holos_var("n2o_direct_emission_factor", self.manure_emission_factors.N2ODirectEmissionFactor)
        self.update_holos_var("volatilization_fraction", self.manure_emission_factors.VolatilizationFraction)
        self.update_holos_var("emission_factor_volatilization", self.manure_emission_factors.EmissionFactorVolatilization)
        self.update_holos_var("fraction_leaching", self.manure_emission_factors.LeachingFraction)
        self.update_holos_var("emission_factor_leaching", self.manure_emission_factors.EmissionFactorLeach)

        self.update_holos_var("volatile_solid_adjusted", 1)
        self.update_holos_var("nitrogen_excretion_adjusted", 1)
        self.update_holos_var("gain_coefficient_a", 0)
        self.update_holos_var("gain_coefficient_b", 0)
        for var_name, value in self.holos_overrides.items():
            setattr(self, var_name, value)
        self._fix_holos_vars()


class DairyHeifers(Dairy):
    animal_group = GroupNameType.dairy_heifers.value


class DairyLactatingCow(Dairy):
    animal_group = GroupNameType.dairy_lactating_cow.value


class DairyCalves(Dairy):
    animal_group = GroupNameType.dairy_calves.value


class DairyDryCow(Dairy):
    animal_group = GroupNameType.dairy_dry_cow.value


class DairyBulls(Dairy):
    animal_group = GroupNameType.dairy_bulls.value
