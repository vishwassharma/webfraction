import xmlrpclib
from bs4 import BeautifulSoup

API_URL = 'https://api.webfaction.com/'


class Webfraction(object):
    """docstring for Webfraction"""
    def __init__(self, xmlconfig="./config.xml"):
        super(Webfraction, self).__init__()
        self.soup = self._read_xml()
        # if soup exist then continue else exit
        self.server = self.connect()
        (self.session_id, self.account) = self.login()
        #print self.session_id, self.account

    def parse_account_information(self):
        # webserver
        # mailserver
        #
        # home
        # username
        #
        # id
        pass

    def _read_xml(self, xml='config.xml'):
        """read the config.xml"""
        soup = BeautifulSoup(open(xml))
        return soup

    def connect(self):
        """Connect to the server"""
        return xmlrpclib.ServerProxy(API_URL, allow_none=True)

    def login(self):
        """docstring for login"""
        username, password = self._get_credentials()
        print "Trying to login (username) : %s" % (username)
        result = self.server.login(username, password)
        return result

    def _get_credentials(self):
        """Get the credentials from the config.xml file"""
        credentials = self.soup.credentials
        username = credentials.username.string 
        password = credentials.password.string
        return (username.strip(), password.strip())

    def _get_apps(self):
        """Get all the application out of the system"""
        pass

    def _get_domain(self):
        """docstring for _get_domain"""
        domain = self.soup.domain
        domain_name = domain.value
        my_domain = domain_name.string.strip()
        my_subdomain = self._get_subdomains(domain)
        return (my_domain, my_subdomain)

    def _get_subdomains(self, domain):
        """docstring for _get_subdomains"""
        subdomains = domain.find_all('subdomain')
        my_subdomains = []
        for s in subdomains:
            my_subdomains.append(s.value.string.strip()) 
        return my_subdomains

    def create_app(self, app):
        """docstring for create_application"""
        name = app.value.string.strip()
        type_id = app.type.string.strip()
        autostart = app.autostart.string.strip()
        extra_info = app.extra_info.string.strip()

        if extra_info == "None":
            extra_info = None

        if autostart == "True" :
            autostart = True
        elif autostart == "False":
            autostart = False

        print "# Creating Application : %s of the type %s .. " %(name, type_id), 
        
        if extra_info == None:
            result = self.server.create_app(self.session_id, name, type_id, autostart, None)
        else:
            result = self.server.create_app(self.session_id, name, type_id, autostart, extra_info)
        print "...... Done"
        self.parse_application_information(result)
        return result

    def parse_application_information(self, application):
        """docstring for parse_application_information"""
        #{'app_type': 'static_only', 'name': 'dafsgfsk_com', 'id': 3asdfasdf, 'machine': 'Wesadfas', 'autostart': False, 'port': 0, 'extra_info': ''}
        #{'app_type': 'django14_mw33_27', 'name': 'safdsdgfom', 'id': 39asdfasf, 'machine': 'Wasdfasd', 'autostart': False, 'port': 0, 'extra_info': ''}
        pass

    def _get_apps(self):
        """Get all the applications from the config.xml file"""
        apps = self.soup.apps
        return apps

    def create_apps(self):
        """Create all the application at once"""
        apps = self._get_apps()
        for eachapp in apps.find_all('app'):
            self.create_app(eachapp)
        return

    def create_website(self, website):
        """docstring for create_website"""
        name = website.value.string.strip()
        ip = website.ip.string.strip()
        https = website.https.string.strip()
        
        # Do something with subdomains
        _subdomains = website.subdomains
        subdomain = []
        for each_sdomain in _subdomains.find_all('subdomain'):
            subdomain.append(each_sdomain.value.string.strip())

        # Do something with apps
        _apps = website.apps
        apps = []
        for each_app in _apps.find_all('app'):
            value = each_app.value.string.strip()
            uri = each_app.uri.string.strip()
            apps.append([value, uri])

        if https == "False":
            https = False
        elif https == "True":
            https = True

        print "### Creating Link between website and app ..", 
        result = self.server.create_website(self.session_id, name, ip, https, subdomain, *apps)
        print "....Done"
        self.parse_website_information(result)
        return result

    def parse_website_information(self, website):
        """docstring for parse_website_information"""
        #{'name': 'dddddddddddddd', 'ip': 'xx.xx.xx.xx', 'subdomains': ['domain.com', 'www.domain.com'], 'https': False, 'id': 251282, 'site_apps': [['domain_com', '/']]}
        pass

    def create_websites(self):
        """docstring for create_websites"""
        #erver.create_website(session_id,
        #... 'widgets_on_the_web',
        #... '174.133.82.194',
        #... True,
        #... ['widgetcompany.biz', 'www.widgetcompany.biz'],
        #... ['django', '/'])
        websites = self._get_websites()
        for each_site in websites.find_all('website'):
            self.create_website(each_site)

    def _get_websites(self):
        """docstring for _get_websites"""
        websites = self.soup.websites
        return websites

    def create_domain(self):
        """docstring for create_domain"""
        (domain, subdomain) = self._get_domain()
        result = self.server.create_domain(self.session_id, domain, *subdomain)
        if 'domain' in result:
            print "# Done -- Domain Setup -- %s" % (result['domain'])
            for each in result['subdomains']:
                print "# Done -- subdomain Setup -- %s.%s" % (each, domain)
        return result 

    def _get_databases(self):
        """docstring for _get_databases"""
        databases = self.soup.databases
        return databases
    
    def create_database(self, database):
        """docstring for create_database"""
        type_id = database.type.string.strip()
        name = database.value.string.strip()
        password = database.password.string.strip()
        #create_db(session_id, name, db_type, password)
        print "# Creating Database (name) %s of type %s" % (name, type_id)
        result = self.server.create_db(self.session_id, name, type_id, password)
        self.parse_database_information(result)
        return result

    def parse_database_information(self, database):
        """docstring for parse_database_information"""
        pass

    def create_databases(self):
        """docstring for create_databases"""
        databases = self._get_databases()
        for database in databases.find_all('database'):
            self.create_database(database)

    def list_machines(self):
        """
        List all of the machines associated with the account. The method returns a list of dictionaries with the following key-value pairs:
        
        """
        result = self.server.list_machines(self.session_id)
        return result

    def list_ips(self):
        """
        List all of the machines associated with the account and their IP addresses. This method returns a list of dictionaries with the following key-value pairs:
        """
        result = self.server.list_ips(self.session_id)
        return result

    def system(self, cmd):
        """
        Execute a command as the user, as if through SSH. If an application was installed previously in the session, 
        the command will be run from the directory where that application was installed.
        """
        result = self.server.system(self.session_id, cmd)
        return result


def main():
    """docstring for main"""
    #soup = BeautifulSoup(open("config.xml"))
    w = Webfraction()
    w.create_domain()
    w.create_apps()
    w.create_websites()
    w.create_databases()

if __name__ == '__main__':
    main()
