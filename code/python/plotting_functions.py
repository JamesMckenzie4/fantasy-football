import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo


def compare_player_fixture_difficulties(
    players=["Lukaku", "Aguero", "Zaha"], n_matches_per_player=5
):
    """Create a staked bar chart showing the difficulty of the players next n matches"""

    # Get paths
    player_fixtures_path = "../../data/fantasy-premier-league-data/player-fixtures.csv"
    players_path = "../../data/fantasy-premier-league-data/players.csv"
    # Get Dataframes
    df_fixtures = pd.read_csv(player_fixtures_path)
    df_players = pd.read_csv(players_path, encoding="ISO-8859-1")
    # Filter df_players for selected players
    df_players = df_players[df_players["web_name"].isin(players)].loc[
        :, ["id", "web_name"]
    ]
    df_players.rename({"id": "player_id"}, inplace=True, axis=1)
    # Inner join with df_fixtures
    merge_df = df_players.merge(df_fixtures, on="player_id", how="inner")
    # Sort by kickoff time and get the correct number of matches for plot
    n_matches = n_matches_per_player * len(players)
    merge_df.sort_values(by="kickoff_time", inplace=True)
    next_5_matches = merge_df.head(n_matches)

    # Groupby each player and difficulty to get counts
    count_data = (
        next_5_matches.groupby(["web_name", "difficulty"])["web_name"].count().to_dict()
    )
    # Routine to get counts for each difficulty category in correct format
    plot_counts = []
    for i in range(1, 6):
        counts = []
        for player in players:
            try:
                count = count_data[(player, i)]
            except KeyError:
                count = 0
            counts.append(count)
        plot_counts.append(counts)

    # Make plot
    data = [
        go.Bar(x=players, y=value, name=index + 1)
        for index, value in enumerate(plot_counts)
    ]
    layout = go.Layout(
        title="Fixture difficulty", barmode="stack", yaxis=dict(title="Number of Games")
    )

    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig)


if __name__ == "__main__":
    compare_player_fixture_difficulties()
