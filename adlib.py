import ldap
ldap.set_option(ldap.OPT_REFERRALS, 0)
import logging
from ldap_user import LdapUser

class AdParser(object):
    def search_result_to_users(self, search_result):
        ad_users=[]
        for i in search_result:
            user = LdapUser()

            user.login = i[0][1]['sAMAccountName'][0]
            user.first_name = unicode(i[0][1]['givenName'][0] if  'givenName' in i[0][1] else '')
            user.display_name = unicode(i[0][1]['displayName'][0] if  'displayName' in i[0][1] else '')

            user.last_name = unicode(i[0][1]['sn'][0] if  'sn' in i[0][1] else '')
            user.tel =  unicode(i[0][1]['telephoneNumber'][0] if  'telephoneNumber' in i[0][1] else '')
            user.department =  unicode(i[0][1]['department'][0] if  'department' in i[0][1] else '')
            user.title =  unicode(i[0][1]['title'][0] if  'title' in i[0][1] else '')
            user.description =  unicode(i[0][1]['description'][0] if  'description' in i[0][1] else '')
            user.mail = unicode(i[0][1]['mail'][0] if  'mail' in i[0][1] else '')
            ad_users.append(user)
        return ad_users

class Ad(object):
    def __init__(self, server, user, password, base_dn, group_dn = None):
        self.__logger = logging.getLogger('sync_ad_zimbra_stream')

        self.__server = server
        self.__group_dn = group_dn
        self.__user = user
        self.__password = password
        self.__base_dn = base_dn
        if group_dn:
            self.__filter = "(&(objectCategory=person)(objectClass=user)(memberOf:1.2.840.113556.1.4.1941:=%s))" % (group_dn)
        else:
            self.__filter = "(&(objectCategory=person)(objectClass=user))"

        self.__logger.debug(self.__filter)
        self.__parser = AdParser()

        self.__ldap = ldap.open(self.__server)
        self.__ldap.protocol_version = ldap.VERSION3
        self.__logger.debug("authorization on server %s on user: %s ..." % (self.__server, self.__user))
        if self.__ldap.simple_bind_s(self.__user, self.__password):
            self.__logger.debug("authorization... done")
        else:
            self.__logger.debug("authorization... fail")
  
    def get_users(self):
        retrieveAttributes = ['sAMAccountName','givenName','displayName','sn', 'telephoneNumber', 'department', 'title', 'description', 'mail']
        self.__logger.debug("make ldap search query...")
        result_id = self.__ldap.search(self.__base_dn, ldap.SCOPE_SUBTREE, self.__filter, retrieveAttributes)
        result_set = []

        self.__logger.debug("ldap search query processing...")
        while True:        
            result_type, result_data = self.__ldap.result(result_id, 0)
            if result_type == ldap.RES_SEARCH_ENTRY:
                result_set.append(result_data)
            if result_type == ldap.RES_SEARCH_RESULT: 
                self.__logger.debug("ldap search query processing... done")
                return self.__parser.search_result_to_users(result_set)