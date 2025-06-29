#!/usr/bin/env python3
"""
Test runner script for Flask application tests.
"""

import sys
import unittest
from tests import FlaskAppTestCase, FlaskAppIntegrationTestCase


def run_tests(verbosity=2, pattern=None):
    """Run the test suite with specified verbosity and pattern."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(FlaskAppTestCase))
    test_suite.addTest(unittest.makeSuite(FlaskAppIntegrationTestCase))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Parse command line arguments
    verbosity = 2
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-v', '--verbose']:
            verbosity = 3
        elif sys.argv[1] in ['-q', '--quiet']:
            verbosity = 1
    
    # Run tests
    success = run_tests(verbosity=verbosity)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 