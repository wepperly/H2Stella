# H2Stella

GNU Public License 3.0. See license file for more details.

WesWare Copyright 2026



Set of scripts to download orbital ephemeris data from JPL Horizons website and output data in format compatible with Stellarium minor solar system bodies ini file. Stellarium has many satellite and other objects built in, but does not include many of the interplanetary and lunar spacecraft. These space vehicles have to be entered into the Stellarium via the minor solar system bodies ini file. If this file fails to be parsed by Stellarium, it will cause the program to crash. So please use with care!



Purpose:

Generate ini file data for Stellarium such that artificial space vehicle data can be imported and simulated in Stellarium planetarium software.



Below instructions assume running on Windows computer, but likely will work on Linux and Mac if but the folder and file structure will differ.



This software is provided as-is with no warranty expressed or implied. Us at your own risk!



Dependencies:

This script require python 3.x and various python libraries to be installed.

In particular, it requires the local python libraries to be installed from the Horizons Application Programming Interface (API).



https://ssd.jpl.nasa.gov/horizons/app.html#/



Once python is installed on you computer, install the required dependences from a terminal window or command line with the following:



pip install Horizons







Description and purpose.

The Horizons API will provide the orbital ephemeris data for a SV, but the user has to tell it what the primary object that it is orbiting. The data is stored in the database by index numbers, and the negative numbers are the spacecraft. So the first script is used to query the JPL database for the spacecraft in the system, and the name, and then outputs that data to a json file that is both human and machine readable, with additional fields to contain the id of the primary object that the sv orbits, and the name of the primary object.  Once the database is queried, the json file is then edited by hand to adjust the primary objects appropriately. Then the next script reads each set of data in the json file and queries the data for generating the Stellarium file, and getting the orbital elements for the appropriate primary body, and then outputs the data to an ini file, that can be appended to the end of the existing the Stellarium ini file.



If python 3.x is not installed, download and install latest bugfix (stable) version of python.

&#x09;https://www.python.org/downloads/

&#x09;Example: https://www.python.org/downloads/release/python-3152/



launch terminal window (Linux) or cmd window (Windows)

Install dependences:

&#x09;pip install Horizons



Run 1st script

ensure local copy of spacecraft\_horizons.json exists in the same folder as the script

&#x09;python horizons-SV-querry.py

&#x09;wait

Once completed, edit the spacecraft\_horizons.json with a text editor.  Look up each spacecraft that is not orbiting around or from the sun or solar system barycenter (SSB) and update the fields as appropriate. The @ symbol means barycenter rather than physical center.



&#x20; horizons\_reference\_mappings

&#x20;       "SSB": "@0"

&#x20;       "Sun": "@10"

&#x20;       "Mercury": "@199"

&#x20;       "Venus": "@299"

&#x20;       "Earth": "@399"

&#x20;       "Moon (Earth's Moon)": "@301"

&#x20;       "Mars": "@499"

&#x20;       "Jupiter": "@599"

&#x20;       "Saturn": "@699"

&#x20;       "Uranus": "@799"

&#x20;       "Neptune": "@899"

&#x20;       "Pluto": "@999"

&#x09;

Once complete, run the next script:

&#x09;python json-to-stellarium-ini.py



Once complete, copy the contents of the resulting file, into local Stellarium file:

&#x09;make backup of Stellarium ini file

&#x09;In windows, file is locate in a hidden folder:

&#x09;C:\\Users\\<YourUserName>\\AppData\\Roaming\\Stellarium\\data\\ssystem\_minor.ini

&#x09;

&#x09;open with text editor file: spacecraft\_sso.ini

&#x09;copy the contents <cntrl-c>

&#x09;open the Stellarium ini file with a text editor

&#x09;	notepad C:\\Users\\<YourUserName>\\AppData\\Roaming\\Stellarium\\data\\ssystem\_minor.ini

&#x09;navigate to the end

&#x09;paste in the contents

&#x09;	<cntrl-C>

&#x09;save the file



Launch Stellarium

If it fails to load, then replace Stellarium ini file with backup file to restore operation.



search by name of SV in Stellarium to locate.



Note:

Once the json file is created, make sure to delete the entries for Lunar Trailblazer and Lunar Flashlight as they will cause Stellarium to crash. The parent body of the orbit is probably incorrect, as these end up with very large numbers that break Stellarium.

