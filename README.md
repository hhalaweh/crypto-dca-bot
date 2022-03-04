
# Crypto DCA Bot
A python bot that allows you to automatically DCA (Dollar-Cost Averaging) into and out of cryptocurrencies of your choice using Binance.

The Crypto DCA Bot also notifies you on telegram with each buy and sell order initiated.  
## Table of Contents
- [Setup](#setup)
    - [Config File](#config-file)
        - [1. Connecting Binance API *[binance]*](#1-connecting-binance-api-binance)
        - [2. Connecting Telegram API *[telegram]*](#2-connecting-telegram-api-telegram)
        - [3. Configuring DCA *[crypto]*](#1-connecting-binance-api-binance)
    - [Python Libraries](#python-libraries)
    - [Digital Ocean Hosting](#digital-ocean-hosting)

## Setup
### Config File
#### 1. Connecting Binance API *[binance]*
[Click here](https://algotrading101.com/learn/binance-python-api-guide/#:~:text=After%20logging%20in%20to%20your,label%20for%20the%20API%20key.) to learn how to obtain the binance api key and secret for your account. Then replace both the *'binance_api'* and *'binance_secret'* in the **config.ini** file.
#### 2. Connecting Telegram API *[telegram]*
The telegram API will be connected in order to receive notifications once a buy/sell order is initiated on the account. Therefore, in case there is any issue with the Binance API you will be notified immediately.  

[Watch this video](https://www.youtube.com/watch?v=ps1yeWwd6iA) in order to learn how to obtain the telegram token and chat ID. Then replace both the *'telegram_token'* and *'telegram_cid'* in the **config.ini** file.
#### 3. Configuring DCA *[crypto]*
##### **dca_pair**
In *'dca_pair'* enter the cryptocurrency pairs that you would like to DCA into/out of separated by a comma. For instance **BTCUSDT,ETHUSDT**.  
##### **usd_amount**
In *'usd_amount'* enter the USD amount you would like to DCA into/out of the cryptocurrencies listed above. For instance, **50,50** will lead to DCAing 50 USDT into/out of *BTCUSDT* and 50 USDT into/out of *ETHUSDT*.
##### **buy_sell**
Setting it to **BUY** allows you to buy crypto, and setting it to **SELL** allows you to sell crypto.
### Python Libraries
### Digital Ocean Hosting







