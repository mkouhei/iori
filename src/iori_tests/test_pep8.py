# -*- coding: utf-8 -*-
import sys
import os
import pep8
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)


def test_pep8():
    if pep8.__version__ >= '1.3':
        arglist = [['statistics', True],
                   ['show-source', True],
                   ['repeat', True],
                   ['exclude', []],
                   ['paths', [BASE_DIR]]]

        pep8style = pep8.StyleGuide(arglist,
                                    parse_argv=False,
                                    config_file=True)
        options = pep8style.options
        if options.doctest:
            import doctest
            fail_d, done_d = doctest.testmod(report=False,
                                             verbose=options.verbose)
            fail_s, done_s = selftest(options)
            count_failed = fail_s + fail_d
            if not options.quiet:
                count_passed = done_d + done_s - count_failed
                print("%d passed and %d failed." % (count_passed,
                                                    count_failed))
                print("Test failed." if count_failed else "Test passed.")
            if count_failed:
                sys.exit(1)
        if options.testsuite:
            init_tests(pep8style)
        report = pep8style.check_files()
        if options.statistics:
            report.print_statistics()
        if options.benchmark:
            report.print_benchmark()
        if options.testsuite and not options.quiet:
            report.print_results()
        if report.total_errors:
            if options.count:
                sys.stderr.write(str(report.total_errors) + '\n')
            sys.exit(1)
        # reporting errors (additional summary)
        errors = report.get_count('E')
        warnings = report.get_count('W')
        message = 'pep8: %d errors / %d warnings' % (errors, warnings)
        print(message)
        assert report.total_errors == 0, message
    else:
        # under pep8 1.3
        arglist = [
            '--statistics',
            '--filename=*.py',
            '--show-source',
            '--benchmark',
            '--repeat',
            '--show-pep8',
            #'--qq',
            #'-v',
            BASE_DIR, ]

        options, args = pep8.process_options(arglist)
        runner = pep8.input_file

        for path in args:
            if os.path.isdir(path):
                pep8.input_dir(path, runner=runner)
            elif not pep8.excluded(path):
                options.counters['files'] += 1
                runner(path)

        pep8.print_statistics()
        errors = pep8.get_count('E')
        warnings = pep8.get_count('W')
        message = 'pep8: %d errors / %d warnings' % (errors, warnings)
        print(message)
        assert errors + warnings == 0, message
