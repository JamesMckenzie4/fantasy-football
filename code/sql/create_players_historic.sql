CREATE TABLE fantasy.players_historic(
game_week text,
first_name text,
second_name text,
position text,
team text,
cost float,
points_last_round int,
total_points int,
average_points float,
average_points_per_pound float,
total_points_per_pound float,
game_week_weighting float,
transfers_out int,
yellow_cards int,
goals_conceeded int,
goals_conceeded_points int,
saves int,
saves_points int,
goals_scored int,
goals_scored_points int,
value_season float,
transfers_out_round int,
price_rise int,
price_fall_round int,
last_seasons_points int,
price_fall int,
value_form float,
penalties_missed int,
form float,
bonus_points int,
fan_rating float,
clean_sheets int,
clean_sheet_points int,
assists int,
selected_by_percent float,
transfers_in int,
own_goals int,
ea_index int,
penalties_saved int,
dream_team_count int,
minutes_played int,
transfers_in_round int,
price_rise_round int,
red_cards int,
bsp int,
next_fixture_1 text,
next_fixture_2 text,
next_fixture_3 text,
next_fixture_4 text,
next_fixture_5 text,
PRIMARY KEY (first_name, second_name, next_fixture_1))