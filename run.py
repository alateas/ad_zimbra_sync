from ad_zimbra_syncer import Syncer

s = Syncer('omzavod.spb.ru', '192.168.0.33', 'sync', 'zxc', 'DC=spbdoors,DC=local', safe_mode=False)
s.add_mail_domain_filter()
s.sync()