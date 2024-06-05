import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp

st.set_page_config(layout="wide")

# Load the datasets
# all_pbp_df = pd.read_csv("all_pbp_df.csv")
all_weekly_players_df = pd.read_csv("all_weekly_players_df.csv")
all_seasonal_players_df = pd.read_csv("all_seasonal_players_df.csv")
all_ngs_passing_df = pd.read_csv("all_ngs_passing_df.csv")
all_ngs_receiving_df = pd.read_csv("all_ngs_receiving_df.csv")
all_ngs_rushing_df = pd.read_csv("all_ngs_rushing_df.csv")

# List of parameters for selection
parameters = [
    "completions", "attempts", "passing_yards", "passing_tds", "interceptions", 
    "carries", "rushing_yards", "rushing_tds", "receptions", "targets", 
    "receiving_yards", "receiving_tds", "fantasy_points"
]

# Explanation of NFL terms
st.sidebar.header("NFL Statistics Explained")
st.sidebar.write("""
- **Completions**: The number of successful passes thrown by a quarterback.
- **Attempts**: The number of passes thrown by a quarterback.
- **Passing Yards**: The total yards gained by the quarterback through passing.
- **Passing TDs**: The number of touchdown passes thrown by a quarterback.
- **Interceptions**: The number of passes intercepted by the opposing defense.
- **Carries**: The number of rushing attempts by a player.
- **Rushing Yards**: The total yards gained by a player through rushing.
- **Rushing TDs**: The number of touchdowns scored by a player through rushing.
- **Receptions**: The number of successful catches made by a receiver.
- **Targets**: The number of times a receiver was thrown the ball.
- **Receiving Yards**: The total yards gained by a receiver through catching passes.
- **Receiving TDs**: The number of touchdowns scored by a receiver through catching passes.
- **Fantasy Points**: A scoring system used in fantasy football to evaluate player performance.
""")

# Get the top 200 players by total fantasy points across all seasons
top_players_seasons_list = all_seasonal_players_df.groupby(['display_name'])['fantasy_points'].sum().nlargest(200).index.tolist()

# Filter the dataframe for these top players
all_seasonal_players_df_top10 = all_seasonal_players_df[all_seasonal_players_df['display_name'].isin(top_players_seasons_list)]

# # Get the list of player names for the multiselect
# player_list = list(all_seasonal_players_df_top10['display_name'].value_counts().index)

# Streamlit app
st.title("NFL Yearly Top Player Statistics (1999-2023)")

# Multiselect option for player names
selected_players = st.multiselect(
    'Select Players',
    options=top_players_seasons_list,
    default=top_players_seasons_list[:2]
)

# Filter the dataframe based on selected players
all_seasonal_players_df_top10_s = all_seasonal_players_df_top10[all_seasonal_players_df_top10['display_name'].isin(selected_players)]

# Create subplots
fig = sp.make_subplots(
    rows=13, cols=1,
    subplot_titles=[
        "Completions", "Attempts", "Passing Yards", "Passing TDs", "Interceptions", 
        "Carries", "Rushing Yards", "Rushing TDs", "Receptions", "Targets", 
        "Receiving Yards", "Receiving TDs", "Fantasy Points"
    ]
)

# Define columns to visualize
columns = [
    "completions", "attempts", "passing_yards", "passing_tds", "interceptions", 
    "carries", "rushing_yards", "rushing_tds", "receptions", "targets", 
    "receiving_yards", "receiving_tds", "fantasy_points"
]

# Add traces to the subplots
color_map = px.colors.qualitative.Plotly  # Use Plotly's qualitative color scheme
player_colors = {player: color_map[i % len(color_map)] for i, player in enumerate(selected_players)}

for player in selected_players:
    player_data = all_seasonal_players_df_top10_s[all_seasonal_players_df_top10_s['display_name'] == player]
    for i, column in enumerate(columns, start=1):
        hover_text = player_data.apply(lambda row: f"{player}<br>Season: {row['season']}<br>{column}: {row[column]}", axis=1)
        fig.add_trace(
            go.Scatter(
                x=player_data["season"], 
                y=player_data[column], 
                mode="lines+markers", 
                name=player if i == 1 else None,  # Show legend only for the first subplot
                line=dict(color=player_colors[player]),
                showlegend=True if i == 1 else False,  # Show legend only once per player
                hovertext=hover_text,
                hoverinfo="text"
            ),
            row=i, col=1
        )

# Update layout
fig.update_layout(
    height=2500*2,  # Increase height
    width=800,  # Increase width
    title_text="Yearly Analysis of Selected Players' Performance",
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)  # Disable container width to use specified width
