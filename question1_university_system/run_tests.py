"""
Test Runner for University Management System

This script runs all unit tests and provides a comprehensive test report.
It can be used to verify that all components of the system work correctly
after making changes to the codebase.

All test files are now organized in the test_code directory for better project structure.
"""

import unittest
import sys
import os


def discover_and_run_tests():
    """
    Discover and run all tests in the test_code directory.

    Returns:
        bool: True if all tests passed, False if any failed
    """
    # Set up test loader
    loader = unittest.TestLoader()

    # Discover all test files (test_*.py) in the test_code directory
    test_code_dir = os.path.join(os.path.dirname(__file__), 'test_code')

    if not os.path.exists(test_code_dir):
        print(f"❌ Test directory not found: {test_code_dir}")
        return False

    test_suite = loader.discover(test_code_dir, pattern='test_*.py')

    # Create test runner with verbose output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )

    # Run the tests
    print("=" * 70)
    print("UNIVERSITY MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 70)
    print(f"Running tests from: {test_code_dir}")
    print("=" * 70)

    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED!")

        # Print failure details
        if result.failures:
            print("\nFAILURES:")
            for test, traceback in result.failures:
                print(f"- {test}")
                print(f"  {traceback}\n")

        if result.errors:
            print("\nERRORS:")
            for test, traceback in result.errors:
                print(f"- {test}")
                print(f"  {traceback}\n")

        return False


def run_specific_test_module(module_name):
    """
    Run tests for a specific module in the test_code directory.

    Args:
        module_name (str): Name of the test module (e.g., 'test_student' or 'student')
    """
    # Ensure module name starts with 'test_'
    if not module_name.startswith('test_'):
        module_name = f'test_{module_name}'

    # Add test_code directory to Python path
    test_code_dir = os.path.join(os.path.dirname(__file__), 'test_code')
    if test_code_dir not in sys.path:
        sys.path.insert(0, test_code_dir)

    try:
        # Import the test module from test_code directory
        test_module = __import__(module_name)

        # Create test suite
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_module)

        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        print("=" * 70)
        print(f"RUNNING TESTS FOR MODULE: {module_name}")
        print("=" * 70)

        result = runner.run(suite)

        return result.wasSuccessful()

    except ImportError as e:
        print(f"❌ Could not import test module '{module_name}' from test_code directory")
        print(f"   Error: {e}")
        print(f"   Make sure the file 'test_code/{module_name}.py' exists")
        return False


def list_available_tests():
    """List all available test modules in the test_code directory."""
    test_code_dir = os.path.join(os.path.dirname(__file__), 'test_code')

    if not os.path.exists(test_code_dir):
        print(f"❌ Test directory not found: {test_code_dir}")
        return

    print("Available test modules:")
    test_files = [f for f in os.listdir(test_code_dir) if f.startswith('test_') and f.endswith('.py')]

    if not test_files:
        print("  No test files found in test_code directory")
        return

    for test_file in sorted(test_files):
        module_name = test_file[:-3]  # Remove .py extension
        short_name = module_name[5:]  # Remove 'test_' prefix
        print(f"  - {module_name} (run with: python run_tests.py {short_name})")


def main():
    """Main function to handle command line arguments and run tests."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg in ['help', '--help', '-h']:
            print("University Management System - Test Runner")
            print("\nUsage:")
            print("  python run_tests.py           # Run all tests")
            print("  python run_tests.py <module>  # Run specific test module")
            print("  python run_tests.py list      # List available test modules")
            print("  python run_tests.py help      # Show this help message")
            print("\nExamples:")
            print("  python run_tests.py person    # Run test_person.py")
            print("  python run_tests.py student   # Run test_student.py")
            return

        elif arg == 'list':
            list_available_tests()
            return

        else:
            # Run specific test module
            print(f"Running tests for module: {arg}")
            success = run_specific_test_module(arg)
    else:
        # Run all tests
        success = discover_and_run_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
