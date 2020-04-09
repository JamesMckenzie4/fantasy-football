INSERT INTO fantasy.players(
SELECT a.*,
	   t.team_id
  FROM (
		SELECT t.season_start_date,
			   t.season_end_date,
			   gw.player_name,
			   gw.player_id,
			   CASE WHEN gw.was_home = true THEN fd.home_team
					ELSE fd.away_team
					 END
					  AS team_name
		  FROM fantasy.game_weeks AS gw
		 INNER JOIN fantasy.teams AS t
			ON gw.opponent_team = t.team_id
		   AND gw.kickoff_time BETWEEN t.season_start_date AND t.season_end_date
		 INNER JOIN fantasy.football_data AS fd
			ON (fd.home_team = t.team_name OR
				fd.away_team = t.team_name)
		   AND fd.match_date = date(gw.kickoff_time)
	    ) AS a
  INNER JOIN fantasy.teams AS t
     ON t.team_name = a.team_name
	AND a.season_start_date = t.season_start_date
	AND a.season_end_date = t.season_end_date)
     ON CONFLICT DO NOTHING