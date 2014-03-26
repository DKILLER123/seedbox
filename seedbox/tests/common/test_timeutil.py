from __future__ import absolute_import
import datetime
import logging
import time

from seedbox.tests import test
# now include what we need to test
from seedbox.common import timeutil

LOG = logging.getLogger('test_timeutil')


class TimeutilTest(test.BaseTestCase):

    def test_nvl_date_default_none(self):
        now = datetime.datetime.utcnow()
        # pass datetime in, get same datetime back
        self.assertIsInstance(timeutil.nvl_date(now), datetime.datetime)
        self.assertEqual(timeutil.nvl_date(now), now)
        # pass None in, get default datetime back
        self.assertIsInstance(timeutil.nvl_date(None), datetime.datetime)
        self.assertIsNotNone(timeutil.nvl_date(None))

    def test_nvl_date_default_provided(self):
        now = datetime.datetime.utcnow()
        # pass datetime in, get same datetime back
        self.assertIsInstance(timeutil.nvl_date(now,
                                                now + datetime.timedelta(1)),
                              datetime.datetime)
        self.assertEqual(timeutil.nvl_date(now,
                                           now + datetime.timedelta(1)), now)
        # pass None in, get default datetime back
        self.assertIsInstance(timeutil.nvl_date(None,
                                                now + datetime.timedelta(1)),
                              datetime.datetime)
        self.assertIsNotNone(timeutil.nvl_date(None,
                                               now + datetime.timedelta(1)))

    def test_timed_function_emit(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.DEBUG)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 flushLevel=logging.DEBUG,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG)
        def simple_func():
            print 'simple'

        simple_func()
        self.assertIsNotNone(CaptureOutput.OUTPUT)
        self.assertEqual(len(CaptureOutput.OUTPUT), 28)

    def test_timed_function_no_emit(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.INFO)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG)
        def simple_func():
            print 'simple'

        simple_func()
        self.assertIsNone(CaptureOutput.OUTPUT)

    def test_timed_function_emit_wlevel(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.INFO)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 flushLevel=logging.DEBUG,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG, loglvl=logging.INFO)
        def simple_func():
            print 'simple'

        simple_func()
        self.assertIsNotNone(CaptureOutput.OUTPUT)
        self.assertEqual(len(CaptureOutput.OUTPUT), 28)

    def test_timed_function_no_emit_wlevel(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.INFO)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG, loglvl=logging.INFO)
        def simple_func():
            print 'simple'

        simple_func()
        self.assertIsNone(CaptureOutput.OUTPUT)

    def test_timed_function_emit_func_args(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.DEBUG)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 flushLevel=logging.DEBUG,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG)
        def simple_func(arg1, arg2):
            print 'simple', arg1, arg2

        simple_func(2, 3)
        self.assertIsNotNone(CaptureOutput.OUTPUT)
        self.assertEqual(len(CaptureOutput.OUTPUT), 28)

    def test_timed_function_no_emit_func_args(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.INFO)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG)
        def simple_func(arg1, arg2):
            print 'simple', arg1, arg2

        simple_func(2, 3)
        self.assertIsNone(CaptureOutput.OUTPUT)

    def test_timed_function_emit_func_args_retval(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.DEBUG)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 flushLevel=logging.DEBUG,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG)
        def simple_func(arg1, arg2):
            print 'simple', arg1, arg2
            return arg1 * arg2

        retval = simple_func(2, 3)
        self.assertEqual(retval, 6)
        self.assertIsNotNone(CaptureOutput.OUTPUT)
        self.assertEqual(len(CaptureOutput.OUTPUT), 28)

    def test_timed_function_no_emit_func_args_retval(self):

        class CaptureOutput(logging.Handler):

            OUTPUT = None

            def handle(self, record):
                CaptureOutput.OUTPUT = self.format(record)


        LOG.setLevel(logging.INFO)
        handler = logging.handlers.MemoryHandler(capacity=100,
                                                 target=CaptureOutput())
        handler.setFormatter(logging.Formatter('%(message)s'))
        LOG.addHandler(handler)

        @timeutil.timed(logger=LOG)
        def simple_func(arg1, arg2):
            print 'simple', arg1, arg2
            return arg1 * arg2

        retval = simple_func(2, 3)
        self.assertEqual(retval, 6)
        self.assertIsNone(CaptureOutput.OUTPUT)

    def test_after_delta(self):

        class ShortDelta(timeutil.AfterDelta):

            def get_delta(self):
                return .5


        @ShortDelta
        def do_something():
            print 'do_something'
            return True

        execs = 0
        counter = 0
        while counter < 11:
            print 'working....', counter
            if do_something():
                execs +=1
            print execs
            time.sleep(.1)
            counter += 1

        self.assertEqual(counter, 11)
        self.assertEqual(execs, 2)
