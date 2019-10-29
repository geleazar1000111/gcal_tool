# Google Calendar Tool

This script reads events from a user's calendar and outputs information from them in a csv file.

Information includes:
  - Event name
  - Event color
  - Time start
  - Time end
  - Time spent (duration of event)
  
Instructions for allowing script to access calendar info:

**Steps below are required only for FIRST TIME USE**
  1. Acquire clients_secrets.json file (make sure to put it in the same directory as the scripts)
  2. Run driver.py; you will be redirected to the login page
  3. Because the script is not a recognized/verified app by Google, a warning will pop up. To bypass, select ADVANCED -> PROCEED 
     (I don't remember the exact words; will update when I do) I promise I'm not trying to hack you LOL
  4. Continue logging in to your Google account 
  5. A verification page stating that the authorization flow has completed will show up. You're done!
  6. Your credentials will now be saved in a pickle token.
  
Other notes:

  - The events used to be in a dictionary. I changed it to a list since only the first instance of a recurring event would be recorded
  - Tested it to handle all-day events (hope to do more improvements and testing soon)
