from enum import Enum
from pathlib import Path

from geojson import FeatureCollection, load
from pandas import DataFrame, read_csv
from shapely.geometry import Point, shape


class MapNamesGeneric(Enum):
    @classmethod
    def _get_name(cls, abbreviation: str) -> str | None:
        for member in cls:
            if member.value.abbreviation == abbreviation:
                return member.value.name

    @classmethod
    def get_name(cls, abbreviation: str) -> str:
        res = cls._get_name(abbreviation=abbreviation)
        return res if res is not None else "NotApplicable"


class NameSlc:
    def __init__(
            self,
            name: str,
            abbreviation: str
    ):
        self.name = name
        self.abbreviation = abbreviation


class CanadianProvince(MapNamesGeneric):
    Alberta = NameSlc(name='Alberta', abbreviation='AB')
    BritishColumbia = NameSlc(name='British Columbia', abbreviation="BC")
    Manitoba = NameSlc(name='Manitoba', abbreviation="MB")
    NewBrunswick = NameSlc(name='New Brunswick', abbreviation="NB")
    NewfoundlandAndLabrador = NameSlc(name='Newfoundland and Labrador', abbreviation="NL")
    NorthwestTerritories = NameSlc(name='Northwest Territories', abbreviation="NT")
    NovaScotia = NameSlc(name='Nova Scotia', abbreviation="NS")
    Nunavut = NameSlc(name='Nunavut', abbreviation="NU")
    Ontario = NameSlc(name='Ontario', abbreviation="ON")
    PrinceEdwardIsland = NameSlc(name='Prince Edward Island', abbreviation="PE")
    Quebec = NameSlc(name='Quebec', abbreviation="QC")
    Saskatchewan = NameSlc(name='Saskatchewan', abbreviation="SK")
    Yukon = NameSlc(name='Yukon', abbreviation="YT")


class SoilGreatGroupNamesSlc(MapNamesGeneric):
    MelanicBrunisol = NameSlc(name='Melanic Brunisol', abbreviation="MB")
    EutricBrunisol = NameSlc(name='Eutric Brunisol', abbreviation="EB")
    SombricBrunisol = NameSlc(name='Sombric Brunisol', abbreviation="SB")
    DystricBrunisol = NameSlc(name='Dystric Brunisol', abbreviation="DYB")
    BrownChernozem = NameSlc(name='Brown Chernozem', abbreviation="BC")
    DarkBrownChernozem = NameSlc(name='Dark Brown Chernozem', abbreviation="DBC")
    BlackChernozem = NameSlc(name='Black Chernozem', abbreviation="BLC")
    DarkGrayChernozem = NameSlc(name='Dark Gray Chernozem', abbreviation="DGC")
    TurbicCryosol = NameSlc(name='Turbic Cryosol', abbreviation="TC")
    StaticCryosol = NameSlc(name='Static Cryosol', abbreviation="SC")
    OrganicCryosol = NameSlc(name='Organic Cryosol', abbreviation="OC")
    HumicGleysol = NameSlc(name='Humic Gleysol', abbreviation="HG")
    Gleysol = NameSlc(name='Gleysol', abbreviation="G")
    LuvicGleysol = NameSlc(name='Luvic Gleysol', abbreviation="LG")
    GrayBrownLuvisol = NameSlc(name='Gray Brown Luvisol', abbreviation="GBL")
    GrayLuvisol = NameSlc(name='Gray Luvisol', abbreviation="GL")
    Fibrisol = NameSlc(name='Fibrisol', abbreviation="F")
    Mesisol = NameSlc(name='Mesisol', abbreviation="M")
    Humisol = NameSlc(name='Humisol', abbreviation="H")
    Folisol = NameSlc(name='Folisol', abbreviation="FO")
    HumicPodzol = NameSlc(name='Humic Podzol', abbreviation="HP")
    FerroHumicPodzol = NameSlc(name='Ferro-Humic Podzol', abbreviation="FHP")
    HumoFerricPodzol = NameSlc(name='Humo-Ferric Podzol', abbreviation="HFP")
    Regosol = NameSlc(name='Regosol', abbreviation="R")
    HumicRegosol = NameSlc(name='Humic Regosol', abbreviation="HR")
    Solonetz = NameSlc(name='Solonetz', abbreviation="SZ")
    SolodizedSolonetz = NameSlc(name='Solodized Solonetz', abbreviation="SS")
    Solod = NameSlc(name='Solod', abbreviation="SO")
    VerticSolonetz = NameSlc(name='Vertic Solonetz', abbreviation="VSZ")
    Vertisol = NameSlc(name='Vertisol', abbreviation="V")
    HumicVertisol = NameSlc(name='Humic Vertisol', abbreviation="HV")

    NotApplicable = NameSlc(name="NotApplicable", abbreviation='NA')
    Unknown = NameSlc(name="NotApplicable", abbreviation='NA')


class ParentMaterialTextureNamesSlc(MapNamesGeneric):
    VeryCoarse = NameSlc(name='Very Coarse', abbreviation="VC")
    Coarse = NameSlc(name='Coarse', abbreviation="C")
    ModeratelyCoarse = NameSlc(name='Moderately Coarse', abbreviation="MC")
    Medium = NameSlc(name='Medium', abbreviation="M")
    ModeratelyFine = NameSlc(name='Moderately Fine', abbreviation="MF")
    Fine = NameSlc(name='Fine', abbreviation="F")
    VeryFine = NameSlc(name='Very Fine', abbreviation="VF")
    CoarseSkeletal = NameSlc(name='Coarse Skeletal', abbreviation="CS")
    MediumSkeletal = NameSlc(name='Medium Skeletal', abbreviation="MS")
    FineSkeletal = NameSlc(name='Fine Skeletal', abbreviation="FS")
    Fragmental = NameSlc(name='Fragmental', abbreviation="FR")
    StratifiedMineral = NameSlc(name='Stratified (Mineral)', abbreviation="SM")
    StratifiedMineralAndOrganic = NameSlc(name='Stratified (Mineral and Organic)', abbreviation="SU")
    Fibric = NameSlc(name='Fibric', abbreviation="FI")
    Mesic = NameSlc(name='Mesic', abbreviation="ME")
    Humic = NameSlc(name='Humic', abbreviation="HU")
    Undifferentiated = NameSlc(name='Undifferentiated', abbreviation="UD")


def read_slc_csv(
        path_file: Path,
        **kwargs
) -> DataFrame:
    return read_csv(path_file, sep=',', decimal='.', **kwargs)


def load_slc_data(path_slc_geojson_file: Path) -> FeatureCollection:
    with path_slc_geojson_file.open(mode='r') as f:
        return load(f)


def get_slc_polygon_properties(
        latitude: float,
        longitude: float,
        geojson_data: FeatureCollection
) -> dict:
    point = Point(longitude, latitude)

    for feature in geojson_data['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']

    raise ValueError(f"No polygon found containing the point with {latitude=} and {longitude=}.")


def get_dominant_component_properties(
        id_polygon: str,
        slc_components_table: DataFrame
) -> dict[str, str]:
    return slc_components_table[slc_components_table['POLY_ID'] == id_polygon].sort_values(
        by='PERCENT_', ascending=False).iloc[0].astype(str).to_dict()


def get_soil_layer_table(
        id_soil: str,
        slc_soil_layer_table: DataFrame
) -> DataFrame:
    return slc_soil_layer_table[slc_soil_layer_table['SOIL_ID'] == id_soil].sort_values(by='UDEPTH', ascending=True)


def get_first_non_litter_layer(
        soil_layer_table: DataFrame
) -> dict:
    return soil_layer_table[soil_layer_table['UDEPTH'] >= 0].iloc[0].to_dict()


def get_soil_name_table(
        soil_name_table: DataFrame,
        id_soil: str
) -> dict:
    return soil_name_table.set_index('SOIL_ID').loc[id_soil].to_dict()
