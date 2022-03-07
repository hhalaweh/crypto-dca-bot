# Import libraries
import configparser as cp
from binance.client import Client
import requests as rq
from datetime import datetime
import prettytable as pt
import logging
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Logging setup
logging.basicConfig(level=logging.INFO, filename = 'log.txt', format='%(asctime)s - %(levelname)s - %(message)s')

# Read config file
config = cp.ConfigParser()
config.read('config.ini')

# Initializing config file variables
binance_api = config['binance']['binance_api']
binance_secret = config['binance']['binance_secret']
telegram_token = config['telegram']['telegram_token']
telegram_cid = config['telegram']['telegram_cid']
dca_list = config['crypto']['dca_pair'].split(',')
amount_list = config['crypto']['usd_amount'].split(',')
buy_sell = config['crypto']['buy_sell']

# Initializing Binance client
client = Client(binance_api, binance_secret)
client.API_URL = config['binance']['api_url']

# Create request template for telegram api
request_template_text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=html'
request_template_image = 'https://api.telegram.org/bot{}/sendPhoto?chat_id={}&caption={}'

# Create csv folder to store csv files
try:
    os.mkdir('csv')
except:
    pass

# Create orders csv file, which contains each order's information such as the crypto bought/sold, amount, price, etc.
if (os.path.exists(os.getcwd() + '/csv/orders.csv')):
    orders = pd.read_csv(os.getcwd() + '/csv/orders.csv')
else:
    orders = pd.DataFrame(columns=['Order ID', 'Crypto', 'Amount', 'USDT Equivalent', 'Price', 'Buy/Sell', 'Time'])

# Used functions

# Helps to convert the string to float and round it to the number of decimals required
float_and_round = lambda x: round(float(x),6)

'''
This function is responsible for two main things:

    1. It will create a table which contains the crypto, amount, usdt equivalent, average price bought, and average price sold, which is sent to the tg channel.
    2. It will create a csv file which contains the user's balance over time, with each dca order.
'''
def create_table():
    if (os.path.exists(os.getcwd() + '/csv/balances.csv')):
        balances = pd.read_csv(os.getcwd() + '/csv/balances.csv')
    else:
        balances = pd.DataFrame(columns=['Time', 'Total']+dca_list)

    table = pt.PrettyTable(['Crypto', 'Amount', 'USDT Equivalent', 'Average Price Bought', 'Average Price Sold'])
    table.align['Crypto'] = 'l'
    table.align['Amount'] = 'r'
    table.align['USDT Equivalent'] = 'r'
    table.align['Average Price Bought'] = 'r'
    table.align['Average Price Sold'] = 'r'
    table.padding_width = 1
    table.set_style(pt.PLAIN_COLUMNS)

    data = []
    total_usd = float_and_round(client.get_asset_balance(asset=dca_list[0][3:])["free"])
    b_row = {}

    for c in dca_list:
        asset_balance = float_and_round(client.get_asset_balance(asset=c[0:3])["free"])
        usd_equivalent = asset_balance * float(client.get_symbol_ticker(symbol=c)["price"])
        total_usd += usd_equivalent 
        b_row[c] = [asset_balance]

        if (len(orders[orders['Buy/Sell'] == 'BUY']) == 0):
            average_price_buy = 0
        else:
            average_price_buy = orders[orders['Buy/Sell'] == 'BUY'].groupby('Crypto')['Price'].mean()[c]
        
        if(len(orders[orders['Buy/Sell'] == 'SELL']) == 0):
            average_price_sell = 0
        else:
            average_price_sell = orders[orders['Buy/Sell'] == 'SELL'].groupby('Crypto')['Price'].mean()[c]

        data.append((c[0:3], asset_balance, usd_equivalent, average_price_buy, average_price_sell))

    b_row['Total'] = [total_usd]
    b_row['Time'] = [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    bal = float_and_round(client.get_asset_balance(asset=c[3:])["free"])
    data.append((c[3:], bal, bal, bal, bal))

    for crypto, amount, usd, avg_buy, avg_sell in data:
        table.add_row([crypto, f'{amount:.5f}', f'{usd:.3f}', f'{avg_buy:.3f}', f'{avg_sell:.3f}'])

    balances = pd.concat([balances, pd.DataFrame(b_row)], ignore_index=True)
    return f'<pre>{table}</pre>', balances

# Removes the html tags from a string, so it can be easily written to the log file
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).replace('\n', ' ')

# Checks the number of decimals required when placing a buy/sell order for any crypto
def check_decimals(symbol):
    info = client.get_symbol_info(symbol)
    val = info['filters'][2]['stepSize']
    decimal = 0
    is_dec = False

    for c in val:
        if is_dec is True:
            decimal += 1
        if c == '1':
            break
        if c == '.':
            is_dec = True
    return decimal

if (__name__ == '__main__'):
    # Create buy/sell orders and send messages
    for c, a in zip(dca_list, amount_list):
        try:
            purchase_amount = round((float(a)/float(client.get_symbol_ticker(symbol = c)['price'])), check_decimals(c))
            order = client.create_order(symbol=c, side=f'{buy_sell}', type='MARKET', quantity=purchase_amount)
            new_row = {'Order ID': [order['orderId']], 'Crypto': [c], 'Amount': [float_and_round(order["fills"][0]["qty"])], 'USDT Equivalent': [float_and_round(order["cummulativeQuoteQty"])], 'Price': [float_and_round(order["fills"][0]["price"])], 'Time': [datetime.fromtimestamp(int(order["transactTime"])/1000)], 'Buy/Sell': [buy_sell]}
            msg = f'{buy_sell.title()} order for <b>{c}</b> with amount <b>{new_row["Amount"][0]} {c[0:3]}</b> for <b>{new_row["USDT Equivalent"][0]} {c[3:]}</b> has been created @ <i><b><u>{new_row["Price"][0]}</u></b></i>\n<b>Order ID: {new_row["Order ID"][0]}</b>\n<b>DateTime: {new_row["Time"][0]}</b>'
            logging.info(remove_html_tags(msg))
            rq.get(request_template_text.format(telegram_token, telegram_cid, msg))
            orders = pd.concat([orders, pd.DataFrame(new_row)], ignore_index=True)
        except:
            logging.error(f'Error buying/selling {c}', exc_info = True)    
            rq.get(request_template_text.format(telegram_token, telegram_cid, f'<b>Error buying/selling {c}</b>'))
        
    # Send table of current balances and acquire balances csv
    table, balances = create_table()
    rq.get(request_template_text.format(telegram_token, telegram_cid, table))

    # Save tables on local hard drive
    orders.to_csv(os.getcwd() + '/csv/orders.csv', index=False)
    balances.to_csv(os.getcwd() + '/csv/balances.csv', index=False)

    # Create line plot of the balance over time
    try:
        os.mkdir('plots')
    except:
        pass

    balances['Time'] = pd.to_datetime(balances['Time'])
    ax = sns.lineplot(x='Time', y='Total', data=balances, color = '#5A8CB7')
    ax.set(xticklabels=[])
    ax.tick_params(bottom=False)
    plt.title('USD Equivalent Balance Over Time', fontsize = 16, y = 1.05)
    sns.despine()
    my_path = os.getcwd()
    photo_path = my_path + f'/plots/{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.png'
    plt.savefig(photo_path, bbox_inches='tight', dpi = 300)
    file = {'photo': open(photo_path, 'rb')}
    rq.post(request_template_image.format(telegram_token, telegram_cid, f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}'), files = file)

    

    








