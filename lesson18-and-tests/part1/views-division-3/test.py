import app
import sys
import unittest
from pathlib import Path
import os


project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402
from ttools.skyprotests.tests_mixins import ResponseTestsMixin  # noqa: E402


class ArchitectureTestCase(SkyproTestCase):
    def setUp(self):
        self.checkpath = basepath.joinpath('part1', 'views-division-3')

    def test_folder_with_views_is_created(self):
        folder = 'views'
        self.assertTrue(os.path.exists(self.checkpath.joinpath(folder)),
        f"%@ Проверьте что создали папку {folder}")

    def test_views_files_is_created(self):
        folder = 'views'
        files = ['books.py', 'authors.py']
        for file in files:
            self.assertTrue(os.path.exists(self.checkpath.joinpath(folder, file)),
            f"%@ Проверьте что создали файл {file} в папке {folder}")


    def test_views_files_has_namespace_vars(self):
        from views import books
        from views import authors
        namespaces_vars = ['book_ns', 'author_ns']
        for var, module in zip (namespaces_vars, [books, authors]):   
            self.assertTrue(
                hasattr(module, var), 
                f'%@ Проверте что перенесли переменную {var} в модуль {module}'
            )

    def test_book_ns_has_correct_resources(self):
        from views import books
        ns_var = books.book_ns
        namespace = ns_var.name
        resources_list = [res.urls[0] for res in ns_var.resources]
        expected_resources = ['/', '/<int:bid>']
        for expected in expected_resources:
            self.assertIn(expected, resources_list,
            '%@ Проверьте что фаил books содержит view-функцию для '
            f' адреса /"{namespace}{expected}"')

    def test_book_ns_has_correct_resources(self):
        from views import authors
        ns_var = authors.author_ns
        namespace = ns_var.name
        resources_list = [res.urls[0] for res in ns_var.resources]
        expected_resources = ['/', '/<int:aid>']
        for expected in expected_resources:
            self.assertIn(expected, resources_list,
            '%@ Проверьте что фаил books содержит view-функцию для '
            f' адреса /"{namespace}{expected}"')


class ApplicationTestCase(SkyproTestCase,
                          ResponseTestsMixin):

    def setUp(self):
        self.student_app = app.app.test_client()


    def test_view_books_get_is_available_and_works_correct(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": list
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_books_post_is_available_and_works_correct(self):
        url = '/books/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [201],
            "student_response": self.student_app.post(
                url, json={}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_books_id_get_is_available_and_works_correct(self):
        url = '/books/1'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": dict
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_authors_get_is_available_and_works_correct(self):
        url = '/authors/'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": list
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_author_post_is_available_and_works_correct(self):
        url = '/authors/'
        test_options = {
            "url": url,
            "method": 'POST',
            "code": [201],
            "student_response": self.student_app.post(
                url, json={}),
        }
        self.check_status_code_jsonify_and_expected(**test_options)

    def test_view_authors_id_get_is_available_and_works_correct(self):
        url = '/authors/1'
        test_options = {
            "url": url,
            "method": 'GET',
            "code": [200],
            "student_response": self.student_app.get(
                url, json=""),
            "expected": dict
        }
        self.check_status_code_jsonify_and_expected(**test_options)

if __name__ == "__main__":
    unittest.main()
