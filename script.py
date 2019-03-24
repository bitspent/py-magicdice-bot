from steem import Steem
import hashlib, binascii, random, time

def randhash():
    m = hashlib.sha256()
    m.update((str(random.randint(1,101)*time.time())).encode('utf-8'))
    m.update((m.hexdigest() + str(random.randint(1,101))).encode('utf-8'))
    x = m.hexdigest()
    return x[2:12]

def newTx(s, amount, direction, target):
    randh = randhash() 
    query = "{0} {1} {2}".format(direction, target, randh)
    s.commit.transfer('magicdice',amount,'STEEM', memo = query, account="aro.steem")
    return randh

def roll(steem, amt) : 
    

    randh = newTx(steem,  amt, 'under', 30)
    
    txId = '-1'
    won = 0
    
    randh = str(randh)
    
    # wait for the tx id
    while True :
        dta = steem.get_account_history('aro.steem', index_from=-1, limit=20)
        for i in range(len(dta)):
            dd = dta[i][1]
            if dd['op'][0] == 'transfer' and dd['op'][1]['to'] == 'magicdice' and dd['op'][1]['memo'].find(randh) > -1:
                txId = str(dd['trx_id'])
                break
        if str(txId) != '-1':
            break
        time.sleep(2)
    
    # wait for the result
    while True :
        dta = steem.get_account_history('aro.steem', index_from=-1, limit=20)
        for i in range(len(dta)):
            dd = dta[i][1]
            if dd['op'][0] == 'transfer' and dd['op'][1]['from'] == 'magicdice' and dd['op'][1]['memo'].find(txId) > -1:
                if dd['op'][1]['amount'] == '0.001 STEEM':
                    won = -1
                else:
                    won = 1
                break
        if won != 0:
            break
        time.sleep(2)
    return txId, won, randh

s = Steem(keys=["<your active private key>", "<your active private key>"])

st = time.time()

txId, won, randh = roll(s, 0.1)

et = time.time()

print(et - st, txId, won)