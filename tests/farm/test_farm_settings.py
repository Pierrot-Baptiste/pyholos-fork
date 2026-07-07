import unittest
from pathlib import Path

from pyholos.farm import farm_settings


class TestFarmSettingsVar(unittest.TestCase):
    def test_farm_settings_variable_works_accepts_any_type_for_values(self):
        for v in (1, 1.0, 'str', Path):
            self.assertEqual(v, farm_settings.FarmSettingsVar(name='test_variable', value=v).value)


class TestParamGeneric(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.param_generic = farm_settings.ParamGeneric(title='test')

    def test_param_generic_has_expected_title(self):
        self.assertEqual('# test', self.param_generic.title)

    def test_param_generic_method_returns_expected_list(self):
        self.assertEqual(['# test'], self.param_generic.to_list())


class TestParamsFarmSettings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.params_farm_settings = farm_settings.ParamsFarmSettings(
            year=1,
            latitude=50,
            longitude=-98,
            monthly_precipitation=list(range(12)),
            monthly_potential_evapotranspiration=list(range(10, 22)),
            monthly_temperature=list(range(-5, 7)),
            run_in_period_years=15)
        _path_sources: Path = Path(__file__).parents[1] / 'sources'
        cls.path_farm_settings = _path_sources / 'Farm.settings'
        with (_path_sources / 'holos/non_regression_farm_settings.txt').open(mode='r', encoding='utf-8') as f:
            cls.expected_output = f.readlines()

    @classmethod
    def tearDownClass(cls):
        if cls.path_farm_settings.exists():
            cls.path_farm_settings.unlink()

    def test_params_farm_settings_output_is_written_to_file(self):
        self.params_farm_settings.write(self.path_farm_settings.parent)
        self.assertTrue(self.path_farm_settings.exists())

        with self.path_farm_settings.open(mode='r', encoding='utf-8') as f:
            output = f.readlines()
        self.assertEqual(self.expected_output, output)
        pass

    def test_params_farm_settings_output_is_passed_to_dict(self):
        for v_expected, v_output in zip(
                self.expected_output,
                self.params_farm_settings.export_to_dict()['Farm.settings']
        ):
            self.assertEqual(v_expected.replace('\n', ''), v_output)
        pass


if __name__ == '__main__':
    unittest.main()
