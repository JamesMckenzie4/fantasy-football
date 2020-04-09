create table fantasy.players(
season_start_date date,
season_end_date date,
player_name text,
player_id int,
team_name text,
team_id int,
primary key(season_start_date, season_end_date, player_id, team_id))