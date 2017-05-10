# Soundcloud Data Scraper
This is a small python script used for scraping user data from Soundcloud, using Soundcloud API.
The script currently creates two files: **edge_list.txt**, which contains a list of edges from which you can easily create a graph, and **user_data.txt**, which contains the data for every user scraped (of course you can select which data you want to keep)

# Installation

Important: **you need a soundcloud client Id for this script to work**. see more at http://developers.soundcloud.com/

If you have the client id, just download `scraper.py`, and run in your console:
`python scraper.py yourClientId firstUserIdToFetch`

And you're all set. the script will do the rest.

Hope this will help someone!

Alessandro
