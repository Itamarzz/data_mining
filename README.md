# data_mining
## Proballers Data Mining Project

This project is a tool for scraping the Proballers website.

**Background:** <br>
The Proballers website offers a worldwide data, updates and insights on basketball.
It gives the user access to a lot of stas, players profiles, team rosters, league scores and standings
both from the past and the most recent gaems.

This package enables to scrape players profiles, leagues & compititions, teams and scores.
It also serves as a platform for future extention to scrape detailed player stas for every game in every season and every compitition.

**List of modules:**
- players: scrape players profiles to create player ID card / data farame of Id cards.
- teams: scrape team pages to create team ID card or recive it as a data frame of all teams.
- games: scrape league schedules per season to get game details and results.
- leagues: scrape the home page to get a data frame of all available leagues.
- usfull functions : methods that are used by the other modules.

**Run the code**

players:
  run the get_id_card(player_url) function to get a single player ID card for provided player url*.
  to get a dataframe of player ID cards run the function get_players_df(lst_of_urls) which takes a list of player urls.
  
  * player url - the general from of player url is : 'https://www.proballers.com/basketball/player/**id/name**'
    to scrape all players : run the df function with a list or range of integers from 1 to LAST_PLAYER_ID (which is now 229373).
      
games:
  to get all game results of a given league in a given season run: get_games_from_league_and_season(league_id, season)
  to get a list with all game IDs from a league, season and page number run: get_game_ids(league_id, season, page)
	Here it is important to specify the pagination and if you want to run for all the pages run get_pagination(league_id, season) to
	get the number of game pages that exist for a league in a specific season and then iterate over all pages.

teams:
  to get all team results of a given league run: get_teams_from_league(league_id)
  to get a list with details (name, country) for a given team run: get_team_details(team_id)
  to get all the teams that participated in the league league_id in the season season run: get_teams_per_season(league_id, season)

leagues:
  run the get_league_urls() function to get a list of all leagues urls.
  run the get_leagues_df(league_urls) with the list of urls to get a data frame with leagues IDs, name and url.

useful functions:
  contians the get_all_season(league_url) which is very useful in combination with the leagues df.
  
main challenge:
  for none of the concepts above there is no option to retrieve a complete table of all records.
  almost for each data point the user need to navigate through: continent --> league --> season --> page and so on..
  we solved it by creating the usful_function module which with combination with the league module and team module give
  us the ability to nevigate through the all website easily!
 
 ### Database
**Database overview:**<br>
This database has been created with the idea that the main use of the data will be focusing on player performance and the impact on his team. Secondary use will be analyzing player performances raltive to themselves and in different leagues and stage of career.

**Tables**:
- _players_, player basic info such as: name, height, position, date of birth with player number as primary key
- _teams_, stores team basic info (team number, name, country) with team number as primary key.
- _leagues_, stores information on the league with leagur number as primary key.
- _games_, to store game information (league, season, date) with game number as a primary key.
- _**team_games**_, stores team games with its score, weather it was a win and if the team played at home. 
- _**player_stats**_, stores player stats per game (shoots taken, shoot made, rebounds, steals etc.).

comment: some tables are small and could be merged with others but we decided to keep them in order to allow scalability.

**Relationships between tables:**
- player_stats and team games, by team_game_id as FK. in order to be able to analyze player performance in contex of his team games (in different seasons and leagues).
- player_stats and players, by player_no as FK.
- team_games and games, by game_no as FK. allows to analyse teams (and player) performace in different seasons, leagues and game details.
- team_games and teams, on team_no as FK.
- games and leagues, on league_no as FK.
-league_season table is not linked for the use of db maintainace and retrieve list of avaiable leagues to scrap.

* please see full DB diagram in project folder
* field details in different


Roy & Itamar
  
