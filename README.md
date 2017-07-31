# FIFATrading
Trading strategies for FIFA 17 Ultimate Team

## Install Dependencies
- fut (for managing your FUT account via Python): https://github.com/oczkers/fut
- telepot (optional, for sending updates via a Telegram bot): https://github.com/nickoala/telepot

## How it works:
- set in ```Strategy.py``` the ```self.idle``` variable, which sets the interval (in seconds) between a "Trade" cycle and a "Leanize" cycle.
- set in ```Strategy.py``` the ```K``` variable, which sets the maximum amount of contracts to buy before the "Trade" cycle stops.
- insert your FUT credentials
- (optional) set the Telegram variables or remove that part
- run ```python Strategy.py```
