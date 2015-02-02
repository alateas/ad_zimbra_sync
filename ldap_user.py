class LdapUser(object):
    def __init__(self):
        self.login = None, 
        self.first_name = None, 
        self.display_name = None, 
        
        first_name = None
        display_name = None
        self.last_name = None
        self.tel = None
        self.department = None
        self.title = None
        self.description = None
        self.domain = None
        self.mail = None
        self.info = None

    def __eq__(self, other):
        return (isinstance(other, LdapUser) and self.login == other.login)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "%s" % (self.login)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self)
