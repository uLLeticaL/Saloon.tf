Saloon.tf
=========
### Dependencies
* Python 2.7
  * pyCrypto
  * mechanize
  * autobahn
  * zope.interface
  * WebOb 1.3.1 (```pip install WebOb==1.3.1```)
* Node.js
* Grunt

### Getting started
1. First you'll have to import database which you can find in the main folder of this reposistory.
2. Now add the bot information to the ```bots``` table using your tool of choice, everything is pretty self describing so you shouldn't have a problem. Please note that you have to use the gmail address in order to make authentication automatic.
3. After you've done that you'll have to enter the database information in the Daemon/settings.py.
4. Later go to the Website directory and run the ```easy_install website``` which should install all Pylons' dependencies for you.
5. After this head to the Website/website/grunt directory and run ```npm install``` to get everything set up for grunt.
