from subprocess import call, Popen, PIPE, STDOUT
from ldap_user import LdapUser
import logging
import string
from random import sample, choice


class ZimbraUser(LdapUser):
    def __str__(self):
        return "%s@%s" % (self.login, self.domain)

    def save(self):
        passw = ''.join(choice(string.letters + string.digits) for _ in range(8))
        cmd = ["/opt/zimbra/bin/zmprov", "ca", str(self), passw,
                    "displayName", self.display_name,
                    "givenName", self.first_name]

        if self.last_name : cmd.extend(["sn", self.last_name])
        if self.tel: cmd.extend(["telephoneNumber", self.tel])
        if self.department: cmd.extend(["company", self.department])
        if self.title: cmd.extend(["title", self.title])

        return True if call(cmd, stderr=STDOUT, shell=False)==0 else False

    def delete(self):
        cmd = ["/opt/zimbra/bin/zmprov", "da", str(self)]
        return True if call(cmd, stderr=STDOUT, shell=False)==0 else False

class Zimbra(object): 
    def __init__(self, domain):
        self.__domain = domain

    def __nonsystem_accounts(self, account):
        if not account:
            return False
        login = account.split('@')[0]
        if login.startswith('ham.') or login.startswith('spam.') or login.startswith('virus-quarantine.') or login == 'galsync':
            return False
        return True

    def get_users(self):
        cmd = ["/opt/zimbra/bin/zmprov", "-l", "gaa", self.__domain]
        output = Popen(cmd, stdout=PIPE).communicate()[0].split("\n")
        output = filter(self.__nonsystem_accounts, output)
        users = []
        for account in output:
            u = ZimbraUser()
            u.login = account.split('@')[0]
            u.domain = self.__domain
            users.append(u)
        return users

    def convert_ad_to_zimbra_user(self, ad_user):
        zimbra_user = ZimbraUser()
        zimbra_user.__dict__.update(ad_user.__dict__)
        zimbra_user.domain = self.__domain
        return zimbra_user
