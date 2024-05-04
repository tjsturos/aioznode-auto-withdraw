# AIOZ Node Auto-Withdraw
If running the [AIOZ Node CLI here](https://github.com/AIOZNetwork/aioz-dcdn-cli-node), then you can automate the process of withdrawing rewards.

This takes into account that the minimum withdrawal is 1, but you can set it to whatever, just know the amount needs to be in attoaioz (1 aioz = 10^18attoaioz).

## Assumptions
- The python script is moved to the same directory as your CLI installation.
- Python3 is installed (`python3 --version`)


## Installing
```bash
# Navigate to the directory you installed the AIOZ Node
git clone https://github.com/tjsturos/aioznode-auto-withdraw.git
mv aioznode-auto-withdraw/withdraw-aioz.py withdraw-aioz.py
chmod +x withdraw-aioz.py
```

### Definding the variables
In the Python script change the 'address' and 'aioznode_dir' to reflect your installation.

The 'address' variable is the public hex address for your wallet you want to withdraw to.

The 'aioznode_dir' is the absolute dir to where your install is.  This is required to find the binary, as well as the privkey.json file, assuming you've left them to their defaults.

### Modifying other variables
There is room for customizing this to reflect your custom install, but you'll have to figure that out on your own.

## General Usage
```bash
python3 withdraw-aioz.py
```

### Retries
This script will retry a withdrawal if you are rate limited.  Rate limiting happens (as far as I can tell) when you've withdrawn to a certain wallet once in the past hour (so 1 withdrawal per wallet per hour).  

## Automating Calling This Script
If using a Unix based machine with a cron system:
```bash
crontab -e
```

and then insert:
```
0 0 * * * python3 /absolute/path/to/withdraw-aioz.py
```

This will run once a day at midnight.

## Logging
There is logging that is outputting the balance every time this checks the balance.