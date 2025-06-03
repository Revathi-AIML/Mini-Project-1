import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine


def get_con():
    host = "localhost"
    user = "Revathi"
    password = "Nithisha_6"
    port = 3306
    database = "MAT4"
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    return engine

def load_data():
    try:
        engine = get_con()
        query = "SELECT * FROM cleaned_movies;"
        df = pd.read_sql(query,engine)
        return df
    except Exception as e:
        st.error(f"error loading data : {e}")
        return pd.DataFrame()
    
df=load_data()
if df.empty:
    st.stop()

st.sidebar.header("Filters")
st.sidebar.title("MovieZone")
page=st.sidebar.radio("Go To",["Movie Trends & Analysis - 2024", "Find Your Movie"])

if page == "Movie Trends & Analysis - 2024":
    
    st.title("IMDB 2024 Movie Analysis - Overall")

    # Top 10 Rating and Voting Counts
    st.subheader("Top 10 Movies by Rating and Voting Counts")
    top_movies=df.sort_values(['Rating','Voting'], ascending=False).head(10)
    st.dataframe(top_movies)

    # Genre Distribution
    st.subheader("Genre Distribution")
    genre_count = df['Genre'].value_counts().reset_index()
    genre_count.columns = ['Genre', 'Count']
    st.plotly_chart(px.bar(genre_count, x='Genre', y= 'Count', color = 'Genre'))

    # Average Duration by Genre
    st.subheader("Average Duration by Genre")
    avg_dur=df.groupby("Genre")["Duration"].mean().reset_index()
    st.plotly_chart(px.bar(avg_dur, x="Duration", y="Genre", orientation="h"))

    # Voting Trends by Genre
    st.subheader("Voting Trends by Genre")
    avg_vote=df.groupby("Genre")["Voting"].mean().reset_index()
    st.plotly_chart(px.bar(avg_vote, x="Genre", y="Voting"))

    # Rating Distribution
    st.subheader("Rating Distribution")
    st.plotly_chart(px.histogram(df, x="Rating", nbins=20, title="Rating Distribution of Movies"))

    # Top Rated Movie per Genre
    st.subheader("Top-Rated Movie per Genre")
    top_genre = df.loc[df.groupby("Genre")["Rating"].idxmax()]
    st.dataframe(top_genre[['Genre', 'Title', 'Rating']].sort_values(by="Rating", ascending=False))

    # Most Popular Genres by Voting
    st.subheader("Most Popular Genres by Voting")
    genre_votes = df.groupby("Genre")["Voting"].sum().reset_index()
    st.plotly_chart(px.pie(genre_votes, values="Voting", names="Genre", title="Most Popular Genres by Voting"))

    # Duration Extremes
    st.subheader("Duration Extremes")
    df_duration=df[df['Duration'] > 0]
    short = df_duration.loc[df_duration['Duration'].idxmin()]
    long = df_duration.loc[df_duration['Duration'].idxmax()]
    st.markdown("**Shortest Movie:**")
    st.write(short[['Title', 'Genre', 'Duration']])
    st.markdown("**Longest Movie:**")
    st.write(long[['Title', 'Genre', 'Duration']])

    # Ratings by Genre
    st.subheader("Ratings by Genre")
    genre_rating_pivot = df.pivot_table(values='Rating', index='Genre', aggfunc='mean')
    fig1, ax = plt.subplots()
    sns.heatmap(genre_rating_pivot, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
    st.pyplot(fig1)

    # Correlation Analysis
    st.subheader("Correlation Analysis")
    fig2 = px.scatter(df, x='Voting', y='Rating', hover_data=['Title', 'Genre'], title="Ratings vs Votes")
    st.plotly_chart(fig2)

elif page == "Find Your Movie":
    st.title("Find Your Favourite Movies")

    st.sidebar.header("Filters")
    select_gener = st.sidebar.multiselect("Select Genre", df['Genre'].unique())
    min_rate = st.sidebar.slider("Minimum Rating",0.0,10.0,5.0,0.1)
    max_rate = st.sidebar.slider("Maximum Rating",0.0,10.0,10.0,0.1)
    min_vote = st.sidebar.slider("Minimum Votes", 0, int(df["Voting"].max()), 1000, 100)
    duration_filter=st.sidebar.radio("Select Duration",["All","< 2 hrs","2 - 3 hrs","> 3 hrs"])
    filter_df=df[(df["Rating"] >= min_rate) & (df["Rating"] <= max_rate) & (df["Voting"] >= min_vote)]
    if(duration_filter == "< 2 hrs"):
        filter_df = filter_df[filter_df["Duration"] < 120]
    elif(duration_filter == "2 - 3 hrs"):
        filter_df = filter_df[(filter_df["Duration"] >= 120) & (filter_df["Duration"] <= 180)]
    elif(duration_filter == "> 3 hrs"):
        filter_df = filter_df[filter_df["Duration"] > 180]
    if select_gener:
        filter_df = filter_df[filter_df['Genre'].isin(select_gener)]
    
        #st.dataframe(filter_df.reset_index(drop=True))
    
    if not filter_df.empty:
        # Top 10 Rating and Voting Counts
        st.subheader("Top 10 Movies by Rating and Voting Counts")
        top_movies=filter_df.sort_values(['Rating','Voting'], ascending=False).head(10)
        st.dataframe(top_movies)

        # Genre Distribution
        st.subheader("Genre Distribution")
        genre_count = filter_df['Genre'].value_counts().reset_index()
        genre_count.columns = ['Genre', 'Count']
        st.plotly_chart(px.bar(genre_count, x='Genre', y= 'Count', color = 'Genre'))

        # Average Duration by Genre
        st.subheader("Average Duration by Genre")
        avg_dur=filter_df.groupby("Genre")["Duration"].mean().reset_index()
        st.plotly_chart(px.bar(avg_dur, x="Duration", y="Genre", orientation="h"))

        # Voting Trends by Genre
        st.subheader("Voting Trends by Genre")
        avg_vote=filter_df.groupby("Genre")["Voting"].mean().reset_index()
        st.plotly_chart(px.bar(avg_vote, x="Genre", y="Voting"))

        # Rating Distribution
        st.subheader("Rating Distribution")
        st.plotly_chart(px.histogram(filter_df, x="Rating", nbins=20, title="Rating Distribution of Movies"))

        # Top Rated Movie per Genre
        st.subheader("Top-Rated Movie per Genre")
        top_genre = filter_df.loc[filter_df.groupby("Genre")["Rating"].idxmax()]
        st.dataframe(top_genre[['Genre', 'Title', 'Rating']].sort_values(by="Rating", ascending=False))

        # Most Popular Genres by Voting
        st.subheader("Most Popular Genres by Voting")
        genre_votes = filter_df.groupby("Genre")["Voting"].sum().reset_index()
        st.plotly_chart(px.pie(genre_votes, values="Voting", names="Genre", title="Most Popular Genres by Voting"))

        # Duration Extremes
        st.subheader("Duration Extremes")
        df_duration=filter_df[filter_df['Duration'] > 0]
        short = df_duration.loc[df_duration['Duration'].idxmin()]
        long = df_duration.loc[df_duration['Duration'].idxmax()]
        st.markdown("**Shortest Movie:**")
        st.write(short[['Title', 'Genre', 'Duration']])
        st.markdown("**Longest Movie:**")
        st.write(long[['Title', 'Genre', 'Duration']])

        # Ratings by Genre
        st.subheader("Ratings by Genre")
        genre_rating_pivot = filter_df.pivot_table(values='Rating', index='Genre', aggfunc='mean')
        fig1, ax = plt.subplots()
        sns.heatmap(genre_rating_pivot, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
        st.pyplot(fig1)

        # Correlation Analysis
        st.subheader("Correlation Analysis")
        fig2 = px.scatter(filter_df, x='Voting', y='Rating', hover_data=['Title', 'Genre'], title="Ratings vs Votes")
        st.plotly_chart(fig2)
    else:
        st.warning("No movies match your filters. Try adjusting the filters.")
