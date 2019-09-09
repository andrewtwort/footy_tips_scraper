# ESPN footy tips scraper

Python webscraper with simple userform/ GUI to download AFL tipping competiton data from ESPN footy tips (www.footytips.com.au). Script currently will fetch data for a single round at a time but could easily be run in a loop to get data from all rounds

## Features
- Written in Python (using Selenium and a Chrome webdriver)
- Simple user form (GUI using the Tkinter library)
- CSV exports

## Usage
This script has been previously used for the 2018 and 2019 AFL footy tipping seasons with minor modifications
### Key parameters
- Users will need to edit the script (lines 13 and 14) with their unique competition ID's which can be found in the competition URL onced logged in via the footy tips website
- The image below highlights in yellow where these parameters can be found
<img src="https://github.com/andrewtwort/footy_tips_scraper/blob/master/images/URL_params.png" width=800>

- Users will also need to enter their login credentials into the user form (GUI window) to run the script. Alternatively the placeholder values in the script can be updated (lines 46 and 47) for those willing to store plain text. Note: the user form/ GUI will not show the users password in plain text and instead will be hidden with asterisks

### Prerequisites
- Selenium
- Tkinter
- Numpy
- Pandas

### Limits
- Be polite with your requests
- This script was created with the intented frequency of one call per week during the footy tipping season

## Sample screens
<table>
  <tr>
    <th>User form/ GUI</th>
    <th>Leaderboard CSV</th>
    <th>Tips CSV</th>
  <tr>
    <td><img src="https://github.com/andrewtwort/footy_tips_scraper/blob/master/images/GUI.png" width=400></td>
    <td><img src="https://github.com/andrewtwort/footy_tips_scraper/blob/master/images/Leaderboard.png" width=300></td>
    <td><img src="https://github.com/andrewtwort/footy_tips_scraper/blob/master/images/Tips.png" width=300></td>
  <tr>
    <td>Simple user form with credentials and round fields</td>
    <td>CSV export with competition leaderboard for each round appended into a master file</td>
    <td>CSV export with all competition tips for each round appended into a master file</td>
</table>

## License
[MIT](https://github.com/andrewtwort/footy_tips_scraper/blob/master/license.md) © Andrew Twort
