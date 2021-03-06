from zimbralib import ZimbraUser, Zimbra
from adlib import Ad
import loglib

class Syncer(object):
    def __init__(self, zimbra_domain, domain_conntroller, user, password, base_dn, group_dn=None, report_file=None, safe_mode=False, delete=False):
        loglib.init_logging(report_file)
        self.__stream_logger = loglib.get_stream_logger()
        self.__report_logger = loglib.get_report_logger()
        self.__ad = Ad(domain_conntroller, user, password, base_dn, group_dn)
        self.__zimbra = Zimbra(zimbra_domain)
        self.__mail_domain = zimbra_domain
        self.__safe_mode = safe_mode
        self.__delete = delete
        self.__filters = []

    def __apply_filters(self, users):
        filtred_users = users
        for i in self.__filters:
            filtred_users = filter(i, filtred_users)
        return filtred_users

    def __refresh_data(self):
        self.__ad_users = self.__apply_filters(self.__ad.get_users())
        self.__zimbra_users = self.__zimbra.get_users()
        
    def __save_user(self, user):
        passw = user.save()
        if passw:
            self.__report_logger.info("User created : %s" % (user, ))
        else:
            self.__stream_logger.info("Error with creating user %s" % user)

    def __delete_user(self, user):
        if user.delete():
            self.__stream_logger.info("User %s successfully deleted" % user)
        else:
            self.__stream_logger.info("Error with deleting user %s" % user)

    def __create_sync(self):
        self.__stream_logger.info("Number of Active Directory users to check: %d" % len(self.__ad_users))
        empty = True
        for ad_user in self.__ad_users:
            if ad_user not in self.__zimbra_users:
                empty = False
                z_user = self.__zimbra.convert_ad_to_zimbra_user(ad_user)
                if not self.__safe_mode:
                    self.__save_user(z_user)
                else:
                    self.__stream_logger.debug("[safe mode]To create %s" % z_user)
        if empty:
            self.__stream_logger.info("Nothing to create.")
    
    def __delete_sync(self):
        for z_user in self.__zimbra_users:
            if z_user not in self.__ad_users:
                if not self.__safe_mode:
                    self.__delete_user(z_user)
                else:
                    self.__stream_logger.debug("[safe mode]To delete %s" % z_user)
 
    def add_mail_domain_filter(self):
        def filter_mail_domain(user):
            if len(user.mail.split("@"))==2:
                return user.mail.split("@")[1] == self.__mail_domain
            return False
        
        self.__filters.append(filter_mail_domain)

    def sync(self):
        self.__refresh_data()
        self.__create_sync()
        if self.__delete:
            self.__delete_sync()
