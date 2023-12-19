import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


st.set_page_config(page_title="Olympic Data Analysis")


df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

#st.dataframe(df)

#st.sidebar.title()

user_menu=st.sidebar.radio('Select an option', ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise analysis'))

if user_menu=='Medal Tally':

    years=helper.years(df)

    countries=helper.countries(df)

    medal_tally=helper.medal_tally(df)

    selected_year=st.sidebar.selectbox("Select Year",years)

    selected_country=st.sidebar.selectbox("Select Country",countries)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    elif selected_year!= 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally for year" + str(selected_year))

    elif selected_year== 'Overall' and selected_country != 'Overall':
        st.title("Overall Medal tally for " + selected_country)

    elif selected_year!= 'Overall' and selected_country != 'Overall':
        st.title("Overall Medal tally for " + selected_country + " for year " + str(selected_year))

    medal_count=helper.medal_count(df,selected_year,selected_country)

    st.table(medal_count)

    #st.dataframe(medal_tally)

if user_menu=="Overall Analysis":
        editions=df['Year'].unique().shape[0]-1 #one year is  not conisdered as olympics 1996
        cities=df['City'].unique().shape[0]
        sports= df['Sport'].unique().shape[0]
        events= df['Event'].unique().shape[0]
        athletes= df['Name'].unique().shape[0]
        nations=df['region'].unique().shape[0]

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header("Editions")
            st.title(editions)

        with col2:
            st.header("Hosts")
            st.title(cities)


        with col3:
            st.header("Sports")
            st.title(sports)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Events")
            st.title(events)

        with col2:
            st.header("Athletes")
            st.title(athletes)

        with col3:
            st.header("Nations")
            st.title(nations)

        nations_over_time=helper.participating_nations_over_time(df)
        fig = px.line(nations_over_time, x="Year", y="count", title='No of Participating Nations Year wise')
        st.plotly_chart(fig)

        events_over_time=helper.events_over_time(df)
        fig1= px.line(events_over_time, x="Year", y="count", title='Number of events Year wise')
        st.plotly_chart(fig1)

        athletes_over_time = helper.athletes_over_time(df)
        fig1 = px.line(athletes_over_time, x="Year", y="count", title='Number of athletes Year wise')
        st.plotly_chart(fig1)

        x = df.drop_duplicates(['Year', 'Sport', 'Event'])

        st.header("No of Events(each sport) over the Years")
        fig, ax = plt.subplots(figsize=(20, 20))
        ax= sns.heatmap(
            x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
            annot=True)
        st.pyplot(fig)

if user_menu=="Country-wise Analysis":

    st.title("Country Wise Analysis")

    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox("Select a country ",country_list)


    country_tally= helper.country_tally(df,selected_country)
    fig = px.line(country_tally, x="Year", y="Medal", title='Number of medal Year wise')
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in following sports")

    country_heatmap=helper.country_heatmap(df,selected_country)

    if(country_heatmap.shape[0]==0):
           st.write("No record")
    else:
       fig, ax = plt.subplots(figsize=(20, 20))
       ax=sns.heatmap(country_heatmap.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0),
                annot=True)
       st.pyplot(fig)

    st.title("Top 10 Athletes")

    top_10=helper.top_athletes(df,selected_country)
    st.table(top_10)




if user_menu=="Athlete wise analysis":
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)

    st.title("Distribution of Age")
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo',
                     'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis',
                     'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
                     'Ice Hockey']

    x = []
    name = []

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]

        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig1 = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=1000, height=600)

    st.title("Distribution of Age wrt Sport(Gold Medalist)")
    st.plotly_chart(fig1)






