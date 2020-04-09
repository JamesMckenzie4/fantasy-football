CREATE TABLE fantasy.teams(
season_start_date date,
season_end_date date,
team_name text,
team_id int,
PRIMARY KEY(season_start_date, season_end_date, team_name, team_id))