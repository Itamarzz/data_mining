# data_mining
## Proballers Data Mining Project

This project is a tool for scraping the Proballers website.

**Background:** <br>
The Proballers website offers a worldwide data, updates and insights on basketball.
It gives the user access to a lot of stas, players profiles, team rosters, league scores and standings
both from the past and the most recent gaems.

This package enables to scrape players profiles, leagues & compititions, teams, game results and player stats.
The data is stored in a database which can be created with its table easily.

**List of modules:**<br>

_scraping modules:_<br>

- players: scrape players profiles to create players table.
- teams: scrape team pages to create teams table.
- games: scrape league schedules per season to create games table and player stats tables.
- leagues: scrape the home page to create leagues table and get list of available leagues to scrpae.
- database: create database with its tables

_configuration and maitenance:_
- usfull functions: methods that are used by the other modules.
- scraper_config: maitain constants, tags, labels etc.
- database_config: config module for database creation and usages

main: responsible for the interaction with user, validate input and use the other modules.


## Run the code

_**Scrape and save data to the database by league and season:**_

* The user can use the scraper through CLI by running the main.py file.
*  in order to scrape and save into database the user need to provide two parameters:
    1. **league** - the league that the user is interested to scrape.
        - input: -l [league name]
    2. **season** - the season that the user is interested to scrape.
        - input: the start year of the season --> -s [year]
  
        example:<br>
              the user is interested in scraping data from the NBA league from season 2009-2010.<br>the command will be: "main.py -l nba -s 2009"<br>
   
* get list of available leagues: by typing the command "main.py -a" or "--availability" the user can print list of all available leagues to scrape.

* technical parameters:
   - chunk size for insertion in data. default value is 1,000. this value can be changed by using -c <your chunk size> or --chunk_size <your chunk size>
   - max games to scrap: to restrict the quantity of games to be scrapped. can be used for testig becuase games scrapping for whole season may take some time.
      the default value is None so there is no limit unless the user chooses to.<br>
        to set a limit use the optional command "-gl <max games to scrap>" or "--games_limit <max games to scrap>".
<br>
    
_**execute examples arguments:**_<br>
```
> -l puerto-rico-bsn -s 2019 -gl 2 # league: puerto-rico-bsn, season: 2019, max 2 games
> -l nba -s 2020 -gl 2 # league: nba, season: 2020, max 2 games
> -l nba -s 2020  -c 100 -gl 10 # league: nba, season: 2020, max 10 games with chunksize 100
```
    
_**Create and use Database:**_:<br>

- The scraper saves scrapped data into a database according to the schema (see on database section).
- The database.py module enables to create a new database with all its tables.<br>

**Todo before running the scraper:**
- update database configuration file with your credentials:
    1. go to the folder database config
    2. in the same directory create a copy of the file database_config_copy and
    rename it to be database_config.py.
    3. in the new file "database_config.py" update your sql credentials. it's in the top of the page.

- create database according to schema below. this can be done running the file "database.py". it will create new database named "proballers".
- if you already have database with this name you can choose another name by changing the DATABASE_NAME constant in the database_config.py file.
   
<br>
  
_**assumptions and default values:**_<br>
- when using the scraper by giving a league and season:
    - new records will be inserted to the following tables: players, teams, games, team_games and player_stats.
    - if a record is already exist in the database, it will not be scraped.
    - in case that some page cannot be scraped at the moment (page is not responding etc.) 
      the sraper will skip that record after several tries. Avialable data will still be scraped and saved to database.
- when running the scraper it assumes that the database is already exist. so the data base should be created before trying to scrape.
- number of tries when page is not responding  is 5 tries

## Database

**Database overview:**<br>
This database has been created with the idea that the main use of the data will be focusing on player performance and the impact on his team. Secondary use will be analyzing player performances raltive to themselves and in different leagues and stage of career.

**Tables**:
- _players_, player id_card with the fields: name, height in meters (float), position (role of player in team), date of birth with player number as primary key
- _teams_, stores team basic info (team number, name, country) with team number as primary key.
- _leagues_, stores information on leagues and competitions (league name) with league number as primary key.
- _games_, to store game information: season, date, league number as a foreign key with game number as a primary key. this table connects team_games table to league table which will allow to analyze game stats in contex of different competitions.
- _**team_games**_, stores team games with its score in the game (int), weather the team won (bool), team played at home (bool), <br>
        team number (foreign key), game number (as a foreign key) and team_game_id as a primary key.    this table is in the heart of the database, connecting all stats from               player stats table to games and then to leagues.
- _**player_stats**_, stores player stats per game (shoots taken vs shoot made, rebounds, steals, fouls, points scored, minutes played and effeciency. all are integers) with team_games_id as a foriegn key and auto increment running index as a primary key. most of the interesting data and stats that we are interested in are stored in this table  which with the link to the team_games table enable us to analyze this stats in different contexts.

comment: some tables are small and could be merged with others but we decided to keep them in order to allow scalability.

**Relationships between tables:**
- player_stats and team games, by team_game_id as FK. in order to be able to analyze player performance in contex of his team games (in different seasons and leagues).
- player_stats and players, by player_no as FK.
- team_games and games, by game_no as FK. allows to analyse teams (and player) performace in different seasons, leagues and game details.
- team_games and teams, on team_no as FK.
- games and leagues, on league_no as FK.
-league_season table is not linked for the use of db maintainace and retrieve list of avaiable leagues to scrap.

* please see full DB diagram in project folder in file "EDR Proballers.pdf" below.

Roy & Itamar
  
![image](https://user-images.githubusercontent.com/79038127/110879701-1a48ce00-82e6-11eb-9b5e-888867ba9d6a.png)

