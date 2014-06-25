Saloon.tf
=========
### Dependencies
1. Python 2.7
2. PostgreSQL
3. Node.js
4. Grunt

### Getting started
1. First you'll have to import database which you can find in the main folder of this reposistory.
2. Now add the bot information to the bots table using your tool of choice, everything is pretty self describing so you shouldn't have a problem. Please not that you have to use the gmail address in order to make authentication authomatic.
3. After you've done that you have to adjust the settings in Daemon/settings.py, enter the api key which you can generate at http://steamcommunity.com/dev/apikey and the database data
4. Later go to the Website directory and run the ```easy_install website``` which will install all dependencies for you.
5. After this head to the Website/website/grunt directory and run ```nodejs install``` to get all dependencies for the grunt.
