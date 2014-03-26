ad_zimbra_sync
==============

Tool for synchronize zimbra email accounts with Active Directory.

## Install

    cd /opt
    git clone https://github.com/alateas/ad_zimbra_sync.git
    cd ad_zimbra_sync
    cp run.py.sample run.py
    ##add to CentOS cron
    echo '0 * * * * root python /opt/ad_zimbra_sync/run.py' > /etc/cron.d/zimbrasync
edit run.py to add your own settings
    
    vim run.py
    
## Run

    python run.py
    
You can make cron rule for schedule synchronization.
