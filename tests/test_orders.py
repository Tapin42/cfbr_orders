import unittest

from orders import Orders
from cfbr_db import Db

class TestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Db.get_db("files/testdb.db")

    @classmethod
    def tearDownClass(cls):
        Db.close_connection()

    def setUp(self):
        pass

    def test_get_next_offers(self):
        pass

    def test_get_orders(self):
        # No plans loaded for a day
        orders = Orders.get_orders(1, 1)
        self.assertEqual(orders, [])

        # No orders accepted for a day -- all pct_completes need to be zero, and all territories present
        orders = Orders.get_orders(2, 1)
        self.assertEqual(len(orders), 5)
        for o in orders:
            self.assertEqual(o['pct_complete'], 0)
            self.assertIn(o['territory'], ["Ann Arbor", "Columbus", "Wisconsin", "College Station", "Cote Nord"])

        # Plans and orders both present -- validate all the things
        orders = Orders.get_orders(3, 1)
        self.assertEqual(len(orders), 5)

        terrs = [x['territory'] for x in orders]
        tiers = [x['tier'] for x in orders]
        quotas = [x['quota'] for x in orders]
        assignments = [x['assigned'] for x in orders]
        pcts = [x['pct_complete'] for x in orders]

        self.assertEqual(terrs, ['Ann Arbor', 'Columbus', 'Wisconsin', 'College Station', 'Cote Nord'])
        self.assertEqual(tiers, [1, 1, 1, 2, 2])
        self.assertEqual(quotas, [5, 10, 10, 3, 2])
        self.assertEqual(assignments, [1, 2, 3, 0, 0])
        self.assertEqual(pcts, [0.2, 0.2, 0.3, 0, 0])

    def test_get_assigned_orders(self):
        pass

    def test_user_already_moved(self):
        pass

    def test_user_already_offered(self):
        pass

    def test_get_foreign_order(self):
        pass

    def test_write_offer(self):
        pass

    def test_confirm_offer(self):
        pass

    def test_get_day_and_tier_totals(self):
        pass

    def test_get_tier_territory_summary(self):
        pass

    def test_get_day_totals(self):
        # No plans loaded for a day
        rv = Orders.get_day_totals(1, 1)
        self.assertEqual(rv, (0,0))

        # No orders accepted for a day
        rv = Orders.get_day_totals(2, 1)
        self.assertEqual(rv, (30,0))

        # Plans and orders both present
        rv = Orders.get_day_totals(3, 1)
        self.assertEqual(rv, (30,6))