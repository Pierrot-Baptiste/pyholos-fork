from enum import StrEnum, auto, unique

from pyholos.common import EnumGeneric
from pyholos.common2 import CanadianProvince


@unique
class ComponentCategory(StrEnum):
    LandManagement = auto()
    BeefProduction = auto()
    Dairy = auto()
    Swine = auto()
    Poultry = auto()
    OtherLivestock = auto()
    Sheep = auto()
    Infrastructure = auto()


class ComponentType(str, EnumGeneric):
    """Holos component types

    References:
        Source code:
        https://github.com/holos-aafc/Holos/blob/396f1ab9bc7247e6d78766f9445c14d2eb7c0d9d/H.Core/Models/ComponentType.cs#L5

    """
    rotation = "Rotation"
    pasture = "Pasture"
    range = "Range"
    shelterbelt = "Shelterbelt"
    field = "Field"
    cow_calf = "CowCalf"
    backgrounding = "Backgrounding"
    finishing = "Finishing"
    grassland = "Grassland"
    dairy = "Dairy"
    dairy_lactating = "DairyLactating"
    dairy_heifer = "DairyHeifer"
    dairy_dry = "DairyDry"
    dairy_calf = "DairyCalf"
    dairy_bulls = "DairyBulls"
    swine = "Swine"
    boar = "Boar"
    swine_finishers = "SwineFinishers"
    swine_starters = "SwineStarters"
    swine_lactating_sows = "SwineLactatingSows"
    swine_dry_sows = "SwineDrySows"
    swine_growers = "SwineGrowers"
    poultry = "Poultry"
    poultry_layers_wet = "PoultryLayersWet"
    poultry_turkeys = "PoultryTurkeys"
    poultry_geese = "PoultryGeese"
    poultry_broilers = "PoultryBroilers"
    poultry_ducks = "PoultryDucks"
    poultry_layers_dry = "PoultryLayersDry"
    sheep = "Sheep"
    sheep_feedlot = "SheepFeedlot"
    rams = "Rams"
    lambs_and_ewes = "LambsAndEwes"
    ewes_and_lambs = "EwesAndLambs"  # added to the original code for convenience
    other_livestock = "OtherLivestock"
    alpaca = "Alpaca"
    elk = "Elk"
    goats = "Goats"
    deer = "Deer"
    horses = "Horses"
    mules = "Mules"
    bison = "Bison"
    llamas = "Llamas"
    farrow_to_wean = "FarrowToWean"
    iso_wean = "IsoWean"
    farrow_to_finish = "FarrowToFinish"
    chicken_pullet_farm = "ChickenPulletFarm"
    chicken_multiplier_breeder = "ChickenMultiplierBreeder"
    chicken_meat_production = "ChickenMeatProduction"
    turkey_multiplier_breeder = "TurkeyMultiplierBreeder"
    turkey_meat_production = "TurkeyMeatProduction"
    chicken_egg_production = "ChickenEggProduction"
    chicken_multiplier_hatchery = "ChickenMultiplierHatchery"
    anaerobic_digestion = "AnaerobicDigestion"

    def to_str(self):
        return f'{self.value}Component'


def calculate_fraction_of_nitrogen_lost_by_leaching_and_runoff(
        growing_season_precipitation: float,
        growing_season_evapotranspiration: float
) -> float:
    """Calculates the nitrogen loss due to leaching and runoff

    Args:
        growing_season_precipitation: Growing season precipitation, by ecodistrict (May – October)</param>
        growing_season_evapotranspiration: Growing season potential evapotranspiration, by ecodistrict (May – October)

    Returns:
        (kg N (kg N)^-1) fraction of N lost by leaching and runoff

    Holos Source Code:
        https://github.com/RamiALBASHA/Holos/blob/71638efd97c84c6ded45e342ce664477df6f803f/H.Core/Calculators/Nitrogen/NitrogenInputCalculatorBase.cs#L15

    """
    fraction_of_nitrogen_lost_by_leaching_and_runoff = 0.3247 * (
            growing_season_precipitation / growing_season_evapotranspiration) - 0.0247
    return min(0.3, max(0.05, fraction_of_nitrogen_lost_by_leaching_and_runoff))


def convert_province_name(name: str) -> CanadianProvince:
    """Returns a CanadianProvince instance based on the given name or abbreviation.

    Args:
        name: name of abbreviation of the canadian province

    Returns:
        CanadianProvince member

    Holos source code:
        https://github.com/holos-aafc/Holos/blob/b183dab99d211158d1fed9da5370ce599ac7c914/H.Core/Converters/ProvinceStringConverter.cs#L9

    Notes:
        The province name "Newfoundland" in the original holos source code was changed to
            "NewfoundlandAndLabrador" to that to agree with the official name of the Province

    """
    match name.lower():
        case "alberta" | "ab" | "alta" | "alb":
            return CanadianProvince.Alberta
        case "britishcolumbia" | "colombiebritannique" | "bc" | "cb":
            return CanadianProvince.BritishColumbia
        case "saskatchewan" | "sk" | "sask":
            return CanadianProvince.Saskatchewan
        case "manitoba" | "mb" | "man":
            return CanadianProvince.Manitoba
        case "ontario" | "on" | "ont":
            return CanadianProvince.Ontario
        case "quebec" | "québec" | "qc" | "que":
            return CanadianProvince.Quebec
        case "newbrunswick" | "nouveaubrunswick" | "nb":
            return CanadianProvince.NewBrunswick
        case "novascotia" | "nouvelleécosse" | "nouvelleecosse" | "ns" | "né" | "ne":
            return CanadianProvince.NovaScotia
        case (
            "princeedwardisland"
            | "îleduprinceédouard"
            | "îleduprinceedouard"
            | "ileduprinceédouard"
            | "ileduprinceedouard"
            | "pe"
            | "pei"
            | "ipe"
            | "ipé"
            | "îpe"
            | "îpé"
        ):
            return CanadianProvince.PrinceEdwardIsland
        case "newfoundlandandlabrador" | "terreneuveetlabrador" | "nl" | "nf" | "tnl" | "nfld" | "newfoundland":
            return CanadianProvince.NewfoundlandAndLabrador
        case "yukon" | "yt" | "yk" | "yuk" | "yn":
            return CanadianProvince.Yukon
        case "northwestterritories" | "territoiresdunordouest" | "nt" | "tno":
            return CanadianProvince.NorthwestTerritories
        case "nunavut" | "nu" | "nvt":
            return CanadianProvince.Nunavut
        case _:
            return CanadianProvince.Alberta


def calc_default_irrigation_amount(
        precipitation: float,
        evapotranspiration: float
) -> float:
    """Calculates the default irrigation amount as the gap between water offer and demand.

    Args:
        precipitation: (mm) precipitation amount
        evapotranspiration: (mm) evapotranspiration amount

    Returns:
        (mm) default irrigation amount

    """
    return max(0., evapotranspiration - precipitation)
