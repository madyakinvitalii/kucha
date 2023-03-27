import sys
from pathlib import Path
import os
import unittest
import app


project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402
from ttools.skyprotests.tests_mixins import ResponseTestsMixin  # noqa: E402


class ArchitectureTestCase(SkyproTestCase, ResponseTestsMixin):
    def setUp(self):
        self.checkpath = basepath.joinpath('part1', 'configs-division')
        self.student_app = app.app.test_client()
        self.obj_list = [
            {
                "name": "iphone 11",
                "brand": "apple",
                "price": 40000
            },
            {
                "name": "iphone 10",
                "brand": "apple",
                "price": 300000
            },
            {
                "name": "redmi 9A",
                "brand": "redmi",
                "price": 30000
            }
        ]
        
    def test_config_is_created(self):
        files = ['config.py']
        for file in files:
            self.assertTrue(os.path.exists(self.checkpath.joinpath(file)),
            f"%@ Проверьте что создали файл {file} в корне папки приложения")

    def test_config_file_has_correct_attributes(self):
        import config
        self.assertTrue(
            hasattr(config, 'Config'),
            '%@Проверьте что создали класс Config в файле config.py'
        )
        attributes = [
            'API_URL', 
            'SQLALCHEMY_DATABASE_URI', 
            'SQLALCHEMY_TRACK_MODIFICATIONS'
        ]
        for att in attributes:
            self.assertTrue(
                hasattr(config.Config, att),
                f"%@Проверьте что создали аттрибут {att} в классе Config"
            )

    def test_views_works_correct(self):
        url = '/import'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json="")
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        url = '/phones'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(url),
            "expected": list,
        }
        self.check_status_code_jsonify_and_expected(**test_options)
        data = self.student_app.get(url).json
        self.assertIsNotNone(data,
            "%@Проверьте что добавили ссылку на внешнее хранилище в "
            "view-функции 'import_data'")
        self.assertEqual(
            len(data), 3,
            "%@Проверьте, что вы добавили все объекты во внешнее хранилище")
        for index in range(3):
            for key in self.obj_list[index].keys():
                self.assertTrue(data[index][key]==self.obj_list[index][key],
                "%@Проверьте, что во внешнем хранилище сохранены корректные данные, "
                "а объекты расположены в таком же порядке как указано в задании."
                )

if __name__ == "__main__":
    unittest.main()