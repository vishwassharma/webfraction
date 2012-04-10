# Webfraction automation

To user this application change the name of the config.xml.ex to config.xml

        mv config.xml.ex config.xml

Then update the config.xml file with your
        
* webfraction username and password
* domain names
* subdomain names
* applications
* type of application
* websites
* link between domain and website
* database type and database name

Once you have updated all these you can run

If you want to leave out some features you can change the main function, enable or disable some of these.

For example if you want only to register domains you can commment out rest of the function calls 
If you want only to setup database you can comment out rest of the function calls

    ```python
    def main():
    """docstring for main"""
    #soup = BeautifulSoup(open("config.xml"))
    w = Webfraction()
    w.create_domain()
    w.create_apps()
    w.create_websites()
    w.create_databases()
    ```

    python webfraction.py


And you are done.. you application will be connected and up and running in 5 min
