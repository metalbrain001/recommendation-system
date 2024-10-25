"""
sample Test case
"""


from django.test import SimpleTestCase
from app import calc


class TestCalc(SimpleTestCase):
    """
    Test cases for calc.py
    """

    def test_add(self):
        """
        test add function
        """

        res = calc.add(3, 8)
        self.assertEqual(res, 11)

    def test_sub(self):
        """
        test sub function
        """

        res = calc.sub(8, 3)
        self.assertEqual(res, 5)
