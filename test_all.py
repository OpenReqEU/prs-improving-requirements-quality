#### CURRENTLY NOT IN USE, ALTHOUGH READY FOR MORE TO BE ADDED ####

# Import testing framework
import unittest
# Import each set of unit tests
from tests.test_basic import TestBasic
from tests.test_check_lexical import TestCheckLexical
from tests.test_check_regexs import TestCheckRegexs
from tests.test_check_pos_regexs import TestCheckPOSRegexs
from tests.test_check_compound_nouns import TestCheckCompoundNouns
from tests.test_check_nominalizations import TestCheckNominalizations

if __name__ == '__main__':
    # Load and run each test suite, in a specific order
    test_classes = [
        TestBasic,
        TestCheckLexical,
        TestCheckRegexs,
        TestCheckPOSRegexs,
        TestCheckCompoundNouns,
        TestCheckNominalizations
    ]

    # Necessary functions
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)

    # Create a large test suite
    for test_class in test_classes:
        # Let the user know which test suite is running
        # print('\n\n------------------------------------------\n\n'
        #       'Running Test Suite: {0}'
        #       '\n\n------------------------------------------\n\n'.format(test_class.__name__))
        # Load the class into a suite
        test_suite = loader.loadTestsFromTestCase(test_class)
        # Run the test suite
        results = runner.run(test_suite)
