import unittest
from copy import deepcopy
from datetime import date
from pathlib import Path

from pyholos.common2 import CanadianProvince
from pyholos.components.animals import common, dairy
from pyholos.common import HolosVar
from pyholos.soil import SoilTexture
from pyholos.utils import read_holos_resource_table


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.non_regression_data = read_holos_resource_table(
            path_file=Path(__file__).parents[2] / 'sources/holos/non_regression_dairy.csv',
            keep_default_na=False)
        cls.non_regression_data.set_index("Group Name", inplace=True)

        cls.province = CanadianProvince.Manitoba
        cls.manure_emission_kwargs = dict(
            mean_annual_precipitation=541.5,
            mean_annual_temperature=3.6,
            mean_annual_evapotranspiration=625.7,
            growing_season_precipitation=383,
            growing_season_evapotranspiration=568,
            province=cls.province,
            soil_texture=SoilTexture.Fine)

        cls.housing_type = common.HousingType.free_stall_barn_solid_litter
        cls.bedding_material_type = common.BeddingMaterialType.sand

        cls.diet = common.Diet(
            crude_protein_percentage=16.146,
            forage_percentage=77.8,
            total_digestible_nutrient_percentage=69.516,
            ash_percentage=6.323,
            starch_percentage=0,
            fat_percentage=0,
            neutral_detergent_fiber_percentage=35.289,
            metabolizable_energy=2.4459)

    def run_test(
            self,
            group_name: str,
            res: dict
    ):
        for k, v in self.non_regression_data.loc[group_name].to_dict().items():
            self.assertAlmostEqual(
                v,
                res[k],
                places=3)

    def test_dairy_heifers(self):
        manure_state_type = common.ManureStateType.daily_spread

        dairy_heifers = dairy.DairyHeifers(
            management_period_name='Management period 1',
            group_pairing_number=0,
            management_period_start_date=date(2025, 1, 1),
            management_period_days=30,
            number_of_animals=20,
            production_stage=common.ProductionStage.gestating,
            number_of_young_animals=0,
            milk_data=common.Milk(),
            diet=self.diet,
            housing_type=self.housing_type,
            manure_handling_system=manure_state_type,
            manure_emission_factors=common.get_manure_emission_factors(
                animal_type=common.AnimalType.dairy_heifers,
                year=2025,
                manure_state_type=manure_state_type,
                **self.manure_emission_kwargs),
            bedding_material_type=self.bedding_material_type
        )

        self.run_test(
            group_name=dairy_heifers.group_name.value,
            res=dairy_heifers.to_dict()
        )

    def test_dairy_lactating_cow(self):
        manure_state_type = common.ManureStateType.pasture

        dairy_lactating_cow = dairy.DairyLactatingCow(
            management_period_name='Early lactation',
            group_pairing_number=1,
            management_period_start_date=date(2024, 1, 1),
            management_period_days=150,
            number_of_animals=20,
            production_stage=common.ProductionStage.gestating,
            number_of_young_animals=0,
            milk_data=common.Milk(
                production=common.get_average_milk_production_for_dairy_cows_value(
                    year=2025,
                    province=self.province),
                fat_content=3.71,
            ),
            diet=self.diet,
            housing_type=self.housing_type,
            manure_handling_system=manure_state_type,
            manure_emission_factors=common.get_manure_emission_factors(
                animal_type=common.AnimalType.dairy_lactating_cow,
                year=2025,
                manure_state_type=manure_state_type,
                **self.manure_emission_kwargs),
            bedding_material_type=self.bedding_material_type
        )

        self.run_test(
            group_name=dairy_lactating_cow.group_name.value,
            res=dairy_lactating_cow.to_dict()
        )

    def test_dairy_calves(self):
        manure_state_type = common.ManureStateType.solid_storage

        dairy_calves = dairy.DairyCalves(
            management_period_name='Milk-fed dairy calves. A period of no enteric methane emissions',
            group_pairing_number=1,
            management_period_start_date=date(2024, 1, 1),
            management_period_days=30,
            number_of_animals=20,
            production_stage=common.ProductionStage.weaning,
            number_of_young_animals=0,
            milk_data=common.Milk(),
            diet=self.diet,
            housing_type=self.housing_type,
            manure_handling_system=manure_state_type,
            manure_emission_factors=common.get_manure_emission_factors(
                animal_type=common.AnimalType.dairy_calves,
                year=2025,
                manure_state_type=manure_state_type,
                **self.manure_emission_kwargs),
            bedding_material_type=self.bedding_material_type
        )

        self.run_test(
            group_name=dairy_calves.group_name.value,
            res=dairy_calves.to_dict()
        )

    def test_dairy_dry_cow(self):
        manure_state_type = common.ManureStateType.solid_storage

        dairy_dry_cow = dairy.DairyDryCow(
            management_period_name='Dry period',
            group_pairing_number=0,
            management_period_start_date=date(2024, 11, 5),
            management_period_days=60,
            number_of_animals=20,
            production_stage=common.ProductionStage.gestating,
            number_of_young_animals=0,
            milk_data=common.Milk(),
            diet=self.diet,
            housing_type=self.housing_type,
            manure_handling_system=manure_state_type,
            manure_emission_factors=common.get_manure_emission_factors(
                animal_type=common.AnimalType.dairy_dry_cow,
                year=2025,
                manure_state_type=manure_state_type,
                **self.manure_emission_kwargs),
            bedding_material_type=self.bedding_material_type
        )

        self.run_test(
            group_name=dairy_dry_cow.group_name.value,
            res=dairy_dry_cow.to_dict()
        )


class TestDairyRefactorUnit(unittest.TestCase):
    """Unit tests focusing on refactor invariants rather than full E2E behavior."""

    def make_heifers(self, **overrides):
        """Helper: produce a valid DairyHeifers with minimal boilerplate."""
        province = common.CanadianProvince.Manitoba
        manure_state_type = common.ManureStateType.daily_spread
        diet = common.Diet(
            crude_protein_percentage=16.146,
            forage_percentage=77.8,
            total_digestible_nutrient_percentage=69.516,
            ash_percentage=6.323,
            starch_percentage=0,
            fat_percentage=0,
            neutral_detergent_fiber_percentage=35.289,
            metabolizable_energy=2.4459,
        )
        base_kwargs = dict(
            management_period_name="MP-1",
            group_pairing_number=0,
            management_period_start_date=date(2025, 1, 1),
            management_period_days=30,
            number_of_animals=20.0,
            production_stage=common.ProductionStage.gestating,
            number_of_young_animals=0,
            milk_data=common.Milk(),
            diet=diet,
            housing_type=common.HousingType.free_stall_barn_solid_litter,
            manure_handling_system=manure_state_type,
            manure_emission_factors=common.get_manure_emission_factors(
                animal_type=common.AnimalType.dairy_heifers,
                year=2025,
                manure_state_type=manure_state_type,
                mean_annual_precipitation=541.5,
                mean_annual_temperature=3.6,
                mean_annual_evapotranspiration=625.7,
                growing_season_precipitation=383,
                growing_season_evapotranspiration=568,
                province=province,
                soil_texture=common.SoilTexture.Fine,
            ),
            bedding_material_type=common.BeddingMaterialType.sand,
        )
        base_kwargs.update(overrides)
        return dairy.DairyHeifers(**base_kwargs)

    # ---------------------------------------------------------------------
    # 1) Idempotence de _fix_holos_vars() et stabilité de to_dict()
    # ---------------------------------------------------------------------
    def test_fix_holos_vars_idempotent_and_stable(self):
        obj = self.make_heifers()
        d1 = obj.to_dict()
        d2 = obj.to_dict()
        self.assertEqual(d1, d2, "to_dict() should be stable across multiple calls")

        # Option: vérifier que les objets HolosVar ne sont pas recréés
        # (nécessite que _fix_holos_vars mette à jour in-place si HolosVar déjà là)
        before = {attr: getattr(obj, attr) for (attr, _, _) in dairy.DAIRY_COMPONENT_HOLOS_VAR}
        obj._fix_holos_vars()
        after = {attr: getattr(obj, attr) for (attr, _, _) in dairy.DAIRY_COMPONENT_HOLOS_VAR}
        for attr in before:
            self.assertIs(before[attr], after[attr], f"HolosVar for '{attr}' should be updated in-place, not recreated")

    # ---------------------------------------------------------------------
    # 2) Conversion date → str (DATE_FMT) et Enum → .value
    # ---------------------------------------------------------------------
    def test_date_and_enum_are_serialized(self):
        obj = self.make_heifers(
            management_period_start_date=date(2030, 12, 31),
            # Force a specific enum we can check easily
            production_stage=common.ProductionStage.weaning,
        )
        out = obj.to_dict()

        # Date is formatted to string
        self.assertIsInstance(out["Management Period Start Date"], str)
        self.assertEqual(out["Management Period Start Date"], "2030-12-31")  # DATE_FMT attendu

        # Enums are serialized to their .value (strings)
        self.assertIsInstance(out["Group Type"], str)
        self.assertEqual(out["Group Type"], obj.group_type.value)

        self.assertIsInstance(out["Production Stage"], str)
        self.assertEqual(out["Production Stage"], obj.production_stage.value)

    # ---------------------------------------------------------------------
    # 3) ADG: calculé si None, sinon conservé
    # ---------------------------------------------------------------------
    def test_average_daily_gain_logic(self):
        # Cas calculé
        obj_calc = self.make_heifers(start_weight=500.0, end_weight=560.0, average_daily_gain=None)
        out_calc = obj_calc.to_dict()
        self.assertAlmostEqual(out_calc["Average Daily Gain"], (560.0 - 500.0) / 30, places=10)

        # Cas fourni
        obj_given = self.make_heifers(start_weight=500.0, end_weight=560.0, average_daily_gain=1.2345)
        out_given = obj_given.to_dict()
        self.assertAlmostEqual(out_given["Average Daily Gain"], 1.2345, places=10)

    # ---------------------------------------------------------------------
    # 4) Présence de toutes les colonnes de la spec dans la sortie
    # ---------------------------------------------------------------------
    def test_all_schema_columns_present(self):
        obj = self.make_heifers()
        out = obj.to_dict()
        expected_columns = [csv_name for (_, csv_name, _) in dairy.DAIRY_COMPONENT_HOLOS_VAR]
        for col in expected_columns:
            self.assertIn(col, out, f"Column '{col}' declared in schema should be present in to_dict()")

    # ---------------------------------------------------------------------
    # 5) Mise à jour in-place quand l'attribut est déjà un HolosVar
    # ---------------------------------------------------------------------
    def test_inplace_update_when_already_holosvar(self):
        obj = self.make_heifers()

        # Force un HolosVar existant sur un champ
        hv = HolosVar(name="Crude Protein", value=42)
        setattr(obj, "crude_protein", hv)

        # Appel de matérialisation: doit mettre à jour in-place
        obj._fix_holos_vars()

        self.assertIs(getattr(obj, "crude_protein"), hv, "Existing HolosVar should not be replaced")
        d = obj.to_dict()
        self.assertEqual(d["Crude Protein"], 42)

    # ---------------------------------------------------------------------
    # 6) Defaults dynamiques (callable) dans la spec
    # ---------------------------------------------------------------------
    def test_callable_default_in_schema(self):
        # On insère temporairement un champ de spec avec default callable
        # qui dépend de l'instance (ex: renvoyer group_name sous une autre clé)
        tmp_schema = list(deepcopy(dairy.DAIRY_COMPONENT_HOLOS_VAR))
        tmp_schema.append(("synthetic_field", "Synthetic Field", lambda self: f"{self.group_name}-X"))

        try:
            obj = self.make_heifers()
            obj.ANIMAL_COMPONENT_HOLOS_VAR = tuple(tmp_schema)  # ClassVar modified to check its behavior
            # On appelle _fix_holos_vars avec la spec étendue
            obj._fix_holos_vars()
            out = obj.to_dict()  # to_dict() va rematérialiser, mais doit conserver la valeur
            self.assertIn("Synthetic Field", out)
            self.assertEqual(out["Synthetic Field"], f"{obj.group_name}-X")
        finally:
            # Rien à restaurer sur le module, on a passé la spec étendue par paramètre
            pass

    # ---------------------------------------------------------------------
    # 7) (Optionnel) Ordre des colonnes = ordre du header CSV de non-régression
    #     → utile si tu veux verrouiller l'ordre pour toujours.
    # ---------------------------------------------------------------------
    def test_optional_column_order_matches_csv_header(self):
        # On lit juste la première ligne (header) du CSV fourni pour la non-régression
        csv_path = Path(__file__).parents[2] / "sources/holos/non_regression_dairy.csv"
        with csv_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        # Saute les lignes de commentaires '#' et récupère le premier header
        header_line = next(line for line in lines if not line.startswith("#"))
        header = [h.strip() for h in header_line.split(",")]

        obj = self.make_heifers()
        out = obj.to_dict()
        observed = list(out.keys())

        # On ne force pas l'égalité stricte pour laisser une marge d'évolution,
        # mais on vérifie que l'ordre actuel correspond au header connu.
        self.assertEqual(
            observed,
            header,
            "Observed to_dict() order differs from CSV header used in non-regression.",
        )


if __name__ == '__main__':
    unittest.main()
