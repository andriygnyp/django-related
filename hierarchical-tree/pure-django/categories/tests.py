import json

from django.test import TestCase, Client

# Create your tests here.


class CategoryModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        with open('data.json') as f:
            self.data = json.load(f)
        self.expectation = (
            (2, {
                    "id": 2, "name": "Category 1.1",
                    "children": [
                        {"id": 4, "name": "Category 1.1.1"},
                        {"id": 5, "name": "Category 1.1.2"}
                    ],
                    "siblings": [
                        {"id": 3, "name": "Category 1.2"}
                    ],
                    "parents": [
                        {"id": 1, "name": "Category 1"}
                    ],
                }),
            (11, {
                    "id": 11, "name": "Category 1.1.2.1",
                    "parents": [
                        {"id": 5, "name": "Category 1.1.2"},
                        {"id": 2, "name": "Category 1.1"},
                        {"id": 1, "name": "Category 1"},
                    ],
                    "children": [],
                    "siblings": [
                        {"id": 12, "name": "Category 1.1.2.2"},
                        {"id": 13, "name": "Category 1.1.2.3"}
                    ]
                }),
            )

    def test_tree(self):
        """
            Creates tree and checks subtrees (branches)
        """
        resp = self.client.post('/categories/', json.dumps(self.data),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        self.assertDictEqual(resp.json(), {'count': 15})

        for (cid, data) in self.expectation:
            resp = self.client.get(f'/categories/{cid}',
                                   content_type="application/json")
            self.assertEqual(resp.status_code, 200)
            self.assertDictEqual(resp.json(), data)
