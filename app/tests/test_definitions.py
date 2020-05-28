import unittest
from startup_nation.app import base

class TestDefinitions(unittest.TestCase):
    def setUp(self):
        self.questions = base.questions('social_media')

    def test_can_get_questions(self):
        self.assertIsInstance(self.questions, list)
        self.assertIsInstance(self.questions[0], dict)

    def test_randomizer(self):
        """Tests the randomizer decorator"""
        rand = base.randomizer(base.questions)
        questions = rand('social_media')
        self.assertIsInstance(questions, list)

    def test_population(self):
        # The decorator accepts a function that
        # opens a given file and returns its
        # JSON data for the random.sample function
        pop = base.population(base.questions)
        questions = pop(1, ['social_media'])
        self.assertIsInstance(questions, list)
        self.assertEqual(len(questions), 1)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestDefinitions('test_can_get_questions'))
    suite.addTest(TestDefinitions('test_randomizer'))
    suite.addTest(TestDefinitions('test_population'))
    unittest.TextTestRunner().run(suite)

    # suite = unittest.TestLoader().loadTestsFromTestCase(TestDefinitions)
    # unittest.TextTestRunner().run(suite)

    # unittest.main()