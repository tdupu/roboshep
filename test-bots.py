#!/usr/bin/env python3
#navigate to local directory and run "python3 test-bots.py helloworld"

from os.path import dirname, basename

import os
import sys
import argparse
import glob
import unittest
import pytest

def parse_args():
    description = """
Script to run test_<bot_name>.py files in the
zulip_bot/zulip_bots/bots/<bot_name> directories.
Running all tests:
./test-bots
Running tests for specific bots:
./test-bots define xkcd
Running all tests excluding certain bots (the
following command would run tests for all bots except
the tests for xkcd and wikipedia bots):
./test-bots --exclude xkcd wikipedia
"""
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('bots_to_test',
                        metavar='bot',
                        nargs='*',
                        default=[],
                        help='specific bots to test (default is all)')
    parser.add_argument('--coverage',
                        nargs='?',
                        const=True,
                        default=False,
                        help='compute test coverage (--coverage combine to combine with previous reports)')
    parser.add_argument('--exclude',
                        metavar='bot',
                        nargs='*',
                        default=[],
                        help='bot(s) to exclude')
    parser.add_argument('--error-on-no-init',
                        default=False,
                        action="store_true",
                        help="whether to exit if a bot has tests which won't run due to no __init__.py")
    parser.add_argument('--pytest', '-p',
                        default=False,
                        action='store_true',
                        help="run tests with pytest")
    parser.add_argument('--verbose', '-v',
                        default=False,
                        action='store_true',
                        help='show verbose output (with pytest)')
    return parser.parse_args()


def main():
    TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(TOOLS_DIR))
    sys.path.insert(0, TOOLS_DIR)
    #bots_dir = os.path.join(TOOLS_DIR, '..', 'zulip_bots/zulip_bots/bots')
    bots_dir = os.path.join(TOOLS_DIR, '..', '/Library/Python/3.7/site-packages/zulip_bots/bots') #added this manually
    glob_pattern = bots_dir + '/*/test_*.py'
    test_modules = glob.glob(glob_pattern)

    # get only the names of bots that have tests
    available_bots = map(lambda path: basename(dirname(path)), test_modules)

    options = parse_args()

    if options.coverage:
        import coverage
        #cov = coverage.Coverage(config_file="tools/.coveragerc") #this is not included
        cov = coverage.Coverage(config_file="/Library/Python/3.7/site-packages/zulip_bots/coveragerc") #this is not included
        if options.coverage == 'combine':
            cov.load()
        cov.start()

    if options.bots_to_test:
        specified_bots = options.bots_to_test
    else:
        specified_bots = available_bots

    # Use of a set ensures we don't end up with duplicate tests with unittest
    # (from globbing multiple test_*.py files, or multiple on the command line)
    bots_to_test = {bot for bot in specified_bots if bot not in options.exclude}

    if options.pytest:
        excluded_bots = ['merels']
        pytest_bots_to_test = sorted([bot for bot in bots_to_test if bot not in excluded_bots])
        pytest_options = [
            '-s',    # show output from tests; this hides the progress bar though
            '-x',    # stop on first test failure
            '--ff',  # runs last failure first
        ]
        pytest_options += (['-v'] if options.verbose else [])
        os.chdir(bots_dir)
        result = pytest.main(pytest_bots_to_test + pytest_options)
        if result != 0:
            sys.exit(1)
        failures = False
    else:
        # Codecov seems to work only when using loader.discover. It failed to
        # capture line executions for functions like loader.loadTestFromModule
        # or loader.loadTestFromNames.
        #top_level = "zulip_bots/zulip_bots/bots/"
        top_level = "/Library/Python/3.7/site-packages/zulip_bots/bots/"
        loader = unittest.defaultTestLoader
        test_suites = []
        for name in bots_to_test:
            try:
                test_suites.append(loader.discover(top_level + name, top_level_dir=top_level))
            except ImportError as exception:
                print(exception)
                print("This likely indicates that you need a '__init__.py' file in your bot directory.")
                if options.error_on_no_init:
                    sys.exit(1)

        suite = unittest.TestSuite(test_suites)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        failures = result.failures
        if failures or result.errors:
            sys.exit(1)

    if not failures and options.coverage:
        cov.stop()
        cov.data_suffix = False  # Disable suffix so that filename is .coverage
        cov.save()
        cov.html_report()
        print("HTML report saved under directory 'htmlcov'.")

if __name__ == '__main__':
    main()
