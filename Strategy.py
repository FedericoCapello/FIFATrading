#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Strategy for fut."""

from Trade import Trade
from random import randint
from time import sleep


class Strategy(object):
    """Strategy class"""

    def __init__(self):
        self.idle = 60 * 30

    def run(self):
        """Run strategy"""

        while True:
            print "Running Strategy: Contracts - 001"
            try:
                Trade(K=10).run()
            except Exception:
				print "Error"
				pass
            print "Done"
            sleep(self.idle)
            print "Running leanizer"
            try:
                Trade(K=10).leanize()
            except Exception:
				print "Error"
				pass
            print "Done"
            sleep(self.idle)


if __name__ == '__main__':
    Strategy().run()
