# transfermarkt-scraper
This scraper creates a sqlite3 database of soccer players from a select group of competitions on [transfermarkt](https://www.transfermarkt.us/). 

transfermarkt has tables of players for each documented team. These hold many different pieces of data for each professional soccer player.

![alt text][table]

[table]: https://raw.githubusercontent.com/rkparel1003/transfermarkt-scraper/master/res/transfermarkt-example.png "Player table"

This scraper takes each row on this table and inserts it into a sqlite3 database using this model:

![alt text][model]

[model]: https://raw.githubusercontent.com/rkparel1003/transfermarkt-scraper/master/res/transfermarkt-sql-table.png "Player model"
