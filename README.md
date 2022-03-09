
# Crypto DCA Bot
The Crypto DCA Bot allows you to automatically DCA (Dollar-Cost Averaging) into and out of cryptocurrencies of your choice using Binance.

The Crypto DCA Bot also notifies you on Telegram with each buy or sell order initiated.  

---
<p align="center">
  <img src="https://user-images.githubusercontent.com/78810452/157315520-56587405-4026-4b8d-b6de-86bd87a752cc.PNG" />
</p>  


---
## Table of Contents
- [Setup](#setup)
    - [Git Clone](#git-clone)
    - [Config File](#config-file)
        - [Config File Sample](#config-file-sample)
        - [1. Connecting Binance API ```[binance]```](#1-connecting-binance-api-binance)
        - [2. Connecting Telegram API ```[telegram]```](#2-connecting-telegram-api-telegram)
        - [3. Configuring DCA ```[crypto]```](#1-connecting-binance-api-binance)
    - [Python Requirements](#python-requirements)
    - [Setting Up Cron Job](#setting-up-cron-job)
    - [Cloud Hosting](#cloud-hosting)
- [License](#license)  

---
## Setup
### Git Clone
Run the following command to clone the repository files:  
```git clone https://github.com/hhalaweh/crypto-dca-bot ```
### Config File
#### Config File Sample
```ini
[binance]
binance_api = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
binance_secret = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
api_url = https://testnet.binance.vision/api
[telegram]
telegram_token = 0000000000:XXXXX0XXX0XX0XXXXXX-XXX0XXXX0XXX0XX
telegram_cid = -000000000
[crypto]
dca_pair = BTCUSDT,ETHUSDT
usd_amount = 50,50
buy_sell = BUY
```
#### 1. Connecting Binance API ```[binance]```
[Click here](https://algotrading101.com/learn/binance-python-api-guide/#:~:text=After%20logging%20in%20to%20your,label%20for%20the%20API%20key.) to learn how to obtain the binance api key and secret for your account. Then replace both the ```binance_api``` and ```binance_secret``` in the **config.ini** file.
#### 2. Connecting Telegram API ```[telegram]```
The telegram API will be connected in order to receive notifications once a buy/sell order is initiated on the account. Therefore, in case there is any issue with the Binance API you will be notified immediately.  

[Watch this video](https://www.youtube.com/watch?v=ps1yeWwd6iA) in order to learn how to obtain the telegram token and chat ID. Then replace both the ```telegram_token``` and ```telegram_cid``` in the **config.ini** file.
#### 3. Configuring DCA ```[crypto]```
##### **dca_pair**
In ```dca_pair``` enter the cryptocurrency pairs that you would like to DCA into/out of separated by a comma. For instance ```BTCUSDT,ETHUSDT```.  
##### **usd_amount**
In ```usd_amount``` enter the USD amount you would like to DCA into/out of the cryptocurrencies listed above. For instance, ```50,50``` will lead to DCAing 50 USDT into/out of *BTCUSDT* and 50 USDT into/out of *ETHUSDT*.
##### **buy_sell**
Setting it to ```BUY``` allows you to buy crypto, and setting it to ```SELL``` allows you to sell crypto.
### Python Requirements
To install all requirements for the python file, run the following command:  
```pip install -r /path/to/requirements.txt```
### Setting Up Cron Job
To setup the cron job to run at a specific time, edit crontab, then add the job. In the example below the file will run on a weekly basis.  
``` crontab -e ```  
```@weekly bash -c 'cd /home/crypto-dca-bot && python3 main.py' >> /home/cron.log```

### Cloud Hosting
The bot can be hosted on Digital Ocean so the cron job can run 24/7 without the need to keep your local machine running.  
You can use my [referral link](https://m.do.co/c/0ccb438f7c20) to receive $100 credit for 60 days to test the code.

---
## License
[MIT License](https://opensource.org/licenses/MIT)






