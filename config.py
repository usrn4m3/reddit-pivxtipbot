

## sample of config file

rpc_config = {
    "rpc_port": "51470",
    "rpc_host": "127.0.0.1",
    "rpc_username": "hidametohejlfdsahfsadgshfah",
    "rpc_password": "fsdghudhzdgyusdgyuoyduagusffdohgoudyhgiudysgityslgtdyilsgdt",
    "timeout": 60
}

# with ending /

DATA_PATH = 'C:/home/pivxtipbot/'

bot_name = "pivxtipbot"
backup_wallet_path = "C:/backup"

user_file = DATA_PATH + 'user_files.json'
unregistered_tip_user = DATA_PATH + 'unregistered_tip_user.json'

logs_path = DATA_PATH + 'logs/'
history_path = DATA_PATH + 'history/'


spam_limit = 1000
rate_fee = 0.003

sendfeeaddress = 'input here'
ffeetip = 0

url_get_value = {
    "coincap": 'https://coincap.io/page/PIVX',
    "cryptocompare": 'https://min-api.cryptocompare.com/data/price?fsym=PIVX&tsyms=USD',
    "blockcypher": 'http://chainz.cryptoid.info/pivx/api.dws?t=txinfo'
}

tip_keyword = {
    "pivxcar" : 98
}
#if you want to let them input there address for a fee 
# vanity-gen request
vanity_enabled = False
vanitygen = DATA_PATH + 'vanitygen.json'
vanitygen_address = "Sk72N2KFYqf78axAGMS2cmDLBTKUvp1iaw"
vanitygen_price = {
 "3":"10",
 "4":"50"
}


# shop
shop_enabled = False
shop_fee = float(1/100)
