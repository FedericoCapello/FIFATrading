#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Trading Contracts for fut."""

import fut
from random import randint
from time import sleep
from datetime import datetime
import requests
import cPickle
import telepot


class Trade(object):

    def tgram(self, txt):
		self.bot.sendMessage(<Telegram Bot Chat>, txt)
		

    def __init__(self, K):
        self.K, self.bought = K, 0
        self.off_limits = []
        self.bot = telepot.Bot('<Telegram API Key>')
        self.f = fut.Core('<FUT Email>', '<FUT Password>', '<FUT secret answer>', platform='ps4')


    def is_pertinent(self, e):
        """Is the item good?"""

        if e['itemType'] == 'contract' and e['discardValue'] == 32 and e['currentBid'] == 0 and e['id'] not in self.off_limits:
            return e['tradeId']


    def pickle_load(self):
        """Load off limits list"""

        with open('list', 'rb') as f:
            self.off_limits = cPickle.load(f)


    def pickle_save(self):
        """Save file"""

        with open('list', 'wb') as f:
            cPickle.dump(self.off_limits, f)


    def buy_first(self):
        """Buy first in auction"""

        for e in self.f.searchAuctions('development', max_price=150):
            if self.is_pertinent(e):
                try:
                    return self.f.bid(e['tradeId'], 150)
                except fut.exceptions.PermissionDenied:
                    return False


    def search(self):
        """Search continuosuly for biddable items"""

        while len(self.f.watchlist()) < self.K:
            sleep(randint(1, 4))
            self.buy_first()


    @staticmethod
    def to_prune(e):
        """Do I have to prune the item?"""

        if e['tradeState'] == 'closed' and e['bidState'] != 'highest':
            return True
        return False


    def prune(self):
        """Prune lost items from the watchlist"""

        pruned = 0
        for e in self.f.watchlist():
            if self.to_prune(e):
                sleep(randint(1, 4))
                self.f.watchlistDelete(e['tradeId'])  # remove from watchlist
                pruned += 1
        return pruned


    def sell_all(self):
        """Sell all items for 150 BID / 200 NOW"""

        for e in self.f.watchlist():
            sleep(randint(1, 4))
            self.f.sendToTradepile(e['tradeId'], e['id'])
            sleep(randint(50, 60))
            try:
                self.f.sell(e['id'], 150, buy_now=200, duration=3600)
            except fut.exceptions.PermissionDenied:
                pass


    def is_consolidated(self):
        """Check if everything is static"""

        for e in self.f.watchlist():
            if e['tradeState'] != 'closed':
                return False

            self.off_limits.append(e['id'])

        return True


    @staticmethod
    def is_to_relist(e):
        """Check if item is to be relisted"""

        return e['tradeState'] == 'expired'


    @staticmethod
    def is_sold(e):
        """Check if item is sold"""

        return e['tradeState'] == 'closed'


    def relist(self):
        """Relist items if not sold and prune tradelist"""

        for e in self.f.tradepile():
            if self.is_to_relist(e):
                sleep(randint(55, 70))
                self.f.sell(e['id'], 150, buy_now=200, duration=3600)

            if self.is_sold(e):
                try:
                    self.off_limits.remove(e['id'])
                except ValueError:
                    pass
                self.f.tradepileDelete(e['tradeId'])


    def run(self):
        """Runs the Trading Strategy"""

        self.pickle_load()
        self.send_email(start=True)
        print "Relisting..."
        self.relist()
        if len(self.f.tradepile()) > 20:
			print "Skipping..."
			return
        sleep(3)
        print "Searching..."
        while True:
            while self.prune() != 0 or len(self.f.watchlist()) < self.K:
                self.search()
            if self.is_consolidated():
                break
            else:
                sleep(9)

        print "Selling..."
        self.sell_all()
        self.pickle_save()
        self.send_email()
        self.f.logout()


    def leanize(self):
        """Leanize the tradepile"""

        self.send_email(start=True)
        print "Relisting..."
        self.relist()
        self.send_email()


    def send_email(self, start=False):
        """Notifies start/stop of trading strategy"""

        self.log()
        now = datetime.now()

        if start:
            content = "Strategy is starting on: {}\nCredits: {}\nTradepile Size: {}".format(now.strftime('%d/%m/%Y %H:%M'), self.f.credits, len(self.f.tradepile()))
            self.tgram("Trading Started\n"+content)
        else:
            content = "Strategy has ended on {}\nCredits: {}\nTradepile Size: {}".format(now.strftime('%d/%m/%Y %H:%M'), self.f.credits, len(self.f.tradepile()))
            self.tgram("Trading Ended\n"+content)


    def log(self):
        """Logs the value of the portfolio"""

        with open('log.txt', 'a') as f:
            f.write('\n' + str(self.f.credits) + ";" + datetime.now().strftime('%d/%m/%Y %H:%M'))


    def test(self):
        """Quick Tests"""

        print self.f.watchlist()
        print self.f.tradepile()
