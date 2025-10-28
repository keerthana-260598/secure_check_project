import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def get_connection():
    connection = mysql.connector.connect(
       host="localhost",
       user="root",
       password="shailesh",
       database= "secure_check"
    )
    return connection





def fetch_data(query):
    connection = get_connection()
    if connection :
        try :
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        finally:
            connection.close()
    else:
        return pd.DataFrame()
    

st.set_page_config(page_title="SecureCheck: A Python-SQL Digital Ledger for Police Post Logs", layout="wide")




st.sidebar.title("📍 Navigation")

page = st.sidebar.radio("Go to", ["🔰 Project Introduction", "📊 Data Visualization", " 📃 SQL Queries","🔎 Smart filter panel" ,"👩🏻Creator Info"])




#page 5

if page == "👩🏻Creator Info":

    st.title("👩‍💻 Creator of this Project")
    st.write("""
       **Developed by:** Keerthana A  
       **Skills:** Python, SQL, Data Analysis,Streamlit, Pandas   
       """)
    

    st.markdown("<h1 style='text-align: center;'>Thank You!</h1>", unsafe_allow_html=True)                           
      
# page 3

elif   page == " 📃 SQL Queries":
    st.title(" 📃SQL Query Results")
    st.subheader( "Medium Level⏳")

    queries  = {
       "top 10 vehicle_Number involved in drug-related stops" :"""SELECT vehicle_number, COUNT(*) AS drug_stops FROM secure_check WHERE drugs_related_stop = 1 GROUP BY vehicle_number ORDER BY drug_stops DESC LIMIT 10;""" ,
       "most frequently searched vehicles" : """SELECT vehicle_number, COUNT(*) as search_type from secure_check group by  vehicle_number order by search_type desc limit 10;""" ,
       "driver age group having highest arrest rate" : """SELECT CASE WHEN driver_age < 18 THEN 'Under 18' WHEN driver_age BETWEEN 18 AND 25 THEN '18-25' WHEN driver_age BETWEEN 26 AND 40 THEN '26-40' WHEN driver_age BETWEEN 41 AND 60 THEN '41-60' ELSE '61+' END AS age_group, COUNT(*) AS total_stops, SUM(is_arrested = 1) AS total_arrests, ROUND(SUM(is_arrested = 1)/COUNT(*)*100, 2) AS arrest_rate_percent FROM secure_check GROUP BY age_group ORDER BY arrest_rate_percent DESC;""" ,
       "gender distribution of drivers stopped in each country" : """select country_name, driver_gender, COUNT(*) as total_stops from secure_check group by country_name, driver_gender order by country_name, driver_gender;""",
       "race and gender combination having highest search rate" : """SELECT driver_race,driver_gender,COUNT(*) AS total_stops, SUM(search_conducted = TRUE) AS total_searches, ROUND(SUM(search_conducted = 1) / COUNT(*) * 100, 2) as search_conducted from secure_check group by driver_race, driver_gender order by search_conducted desc limit 1;""" ,
       "What time of day sees the most traffic stops" : """select stop_time, count(*) as total_stops from secure_check group by stop_time order by total_stops desc;""" ,
       "average stop duration for different violations" : """select violation, avg(stop_duration) as avg_stop_duration from secure_check group by violation having avg_stop_duration;""" ,
       "Are stops during the night more likely to lead to arrests" : """select CASE WHEN HOUR(stop_time) BETWEEN 6 AND 17 THEN 'Day'ELSE 'Night'END as time_period,count(*) AS total_stops,round(sum(is_arrested = 1)/count(*)*100, 2) as arrest_rate from secure_check group by time_period;""" ,
       "violations that are mostly associated with searches or arrests" : """select violation, sum(search_conducted =1) as searched, sum(is_arrested = 1) as arrested from secure_check group by violation order by searched , arrested desc;""" ,
       "violations are most common among younger drivers (<25)" : """select violation, count(*) as total_stops from secure_check where driver_age < 25 group by violation order by total_stops desc;""" ,
       "violation that rarely results in search or arrest" : """select violation, sum(search_conducted =1) as searched, sum(is_arrested = 1) as arrested from secure_check group by violation order by searched , arrested asc limit 1 ;""" ,
       "countries report the highest rate of drug-related stops" : """select country_name, count(*) as country, sum(drugs_related_stop= 1) as drugs_related_stops, round(sum(search_conducted = 1) / count(*) * 100, 2) as highest_rate from secure_check group by country_name order by highest_rate desc ;""" ,
       "arrest rate by country and violation" : """select country_name, violation, round(sum(is_arrested = 1) / COUNT(*) * 100, 2) as arrest_rate from secure_check group by country_name, violation order by country_name, violation, arrest_rate desc;""" ,
       "country having the most stops with search conducted" : """select country_name,count(*)as country, sum(search_conducted =1) as searched from secure_check group by country_name order by searched desc ;""" 
       }


    selected_medium_query = st.selectbox("Choose a medium_level Query", list(queries.keys()))
    query_result = fetch_data(queries[selected_medium_query])
    
    st.write("### Query Result:")
    st.dataframe(query_result)

    if query_result.empty:
        st.warning("⚠ No data returned for this query.")
    else:
        st.success(f"✅ Query executed successfully! Showing.")
        



    st.subheader("Complex Level⌛") 
    complex_queries  = {
        "Yearly Breakdown of Stops and Arrests by Country" : """ select country_name,year,total_stops,total_arrests, round(total_arrests / total_stops * 100, 2) as arrest_rate, RANK() over (PARTITION BY year order by total_arrests desc) as rank_by_arrest from (select country_name,year(stop_date) as year,COUNT(*) as total_stops, sum(is_arrested = 1) as total_arrests from secure_check group by country_name, year) as yearly_summary order by year asc, total_arrests desc;""" ,
        "Driver Violation Trends Based on Age and Race" : """select driver_race, age_group, violation, total_violations, round(total_violations * 100.0 /sum(total_violations) OVER (PARTITION BY driver_race, age_group),2) as percent_within_group from (select driver_race, CASE WHEN driver_age BETWEEN 16 AND 25 THEN '16-25' WHEN driver_age BETWEEN 26 AND 35 THEN '26-35' WHEN driver_age BETWEEN 36 AND 50 THEN '36-50' WHEN driver_age > 50 THEN '50+'   ELSE 'Unknown' END AS age_group, violation, count(*) as total_violations from secure_check group by driver_race, age_group, violation) as summary order by age_group, total_violations, driver_race;""",
        "Number of Stops by Year,Month, Hour of the Day" : """select YEAR(stop_date) as year, MONTH(stop_date) as month, HOUR(stop_time) as hour, count(*) as total_stops from secure_check group by year, month, hour order by year asc, month asc, hour asc;""" ,
        "Violations with High Search and Arrest Rates" : """select violation, total_stops, total_searches, total_arrests, round(total_searches * 100.0 / total_stops, 2) as search_rate, round(total_arrests * 100.0 / total_stops, 2) as arrest_rate, RANK() OVER (ORDER BY (total_searches * 1.0 / total_stops) DESC) AS search_rank, RANK() OVER (ORDER BY (total_arrests * 1.0 / total_stops) DESC) AS arrest_rank from (select violation,count(*) as total_stops, SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches, SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests from secure_check group by violation) as violation_summary order by arrest_rate,search_rate desc;""" ,
        "Driver Demographics by Country (Age, Gender, and Race)" : """select country_name,count(*) as total_drivers,round(avg(driver_age), 1) as avg_age, SUM(CASE WHEN driver_gender = 'M' THEN 1 ELSE 0 END) AS male_count, SUM(CASE WHEN driver_gender = 'F' THEN 1 ELSE 0 END) AS female_count, SUM(CASE WHEN driver_race = 'White' THEN 1 ELSE 0 END) AS white_drivers, SUM(CASE WHEN driver_race = 'Black' THEN 1 ELSE 0 END) AS black_drivers, SUM(CASE WHEN driver_race = 'Hispanic' THEN 1 ELSE 0 END) AS hispanic_drivers, SUM(CASE WHEN driver_race = 'Asian' THEN 1 ELSE 0 END) AS asian_drivers, SUM(CASE WHEN driver_race NOT IN ('White','Black','Hispanic','Asian') THEN 1 ELSE 0 END) AS other_race from secure_check group by country_name order by total_drivers;""" ,
        "Top 5 Violations with Highest Arrest Rates" : """select violation,count(*) as total_stops, round(sum(is_arrested = 1) / count(*) * 100, 2) as arrest_rate from secure_check group by violation order by arrest_rate desc limit 5;"""
        }

    selected_complex_query = st.selectbox("Choose a complex_level Query", list(complex_queries.keys()))
    complex_query_result = fetch_data(complex_queries[selected_complex_query])
    
    st.write("### Query Result:")
    st.dataframe(complex_query_result)

    if complex_query_result.empty:
        st.warning("⚠ No data returned for this query.")
    else:
        st.success(f"✅ Query executed successfully! Showing.")



#page 4

elif  page == "🔎 Smart filter panel":

    st.title("🔎 Smart filter panel")

    st.header("🚨 Using the police post logs predict the needed results")

    st.markdown("⬇  **fill in the details below to get a simple language and understandable prediction**")

    final_query = "SELECT * FROM secure_check;"
    data = fetch_data(final_query)

    with st.form("post_logs_form"):
        stop_date = st.date_input("Stop Date")
        stop_time = st.time_input("Stop Time")
        country_name = st.text_input("Country Name")
        driver_age = st.number_input("Driver Age", min_value=16, max_value=100)
        driver_gender = st.selectbox("Driver Gender", ["male","female"])
        search_conducted = st.selectbox("was search conducted?", ["0","1"])
        violation = st.text_input("Violation")
        drugs_related_stop = st.selectbox("was it drug related?", ["0","1"])
        stop_outcome = st.text_input ("Stop outcome")
        vehicle_number = st.text_input("Vehicle Number")
        stop_duration = st.selectbox("Stop Duration", data["stop_duration"].unique())

        submitted = st.form_submit_button("Predict Violation and Stop outcome ")


        if submitted:
            filtered_data = data[
                (data["driver_age"] == driver_age) &
                (data["driver_gender"] == driver_gender) &
                (data["drugs_related_stop"] == int(drugs_related_stop)) &
                (data["search_conducted"] == int(search_conducted)) &
                (data["stop_duration"] == stop_duration) 
                
            ]

            if not filtered_data.empty: 
                predicted_violation = filtered_data['violation'].mode()[0]
                predicted_outcome = filtered_data['stop_outcome'].mode()[0]
            else:
                predicted_violation = "speeding"
                predicted_outcome = "warning"

            search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
            drug_stop = "was drug-related" if int(drugs_related_stop) else "was not drug-related"

            st.markdown(f"""
                ✅**prediction summary**
                        
                -  Predicted violation : {predicted_violation}
                -  Predicted stop_outcome : {predicted_outcome}

                📝 A {driver_age}-year-old {driver_gender} driver in {country_name} was stopped for {predicted_violation} at {stop_time.strftime('%I:%M %p')} on {stop_date}.
                {search_text},and the person received a {predicted_outcome}. The stop lasted {stop_duration} and {drug_stop}.
                
                Vehicle Number : **{vehicle_number}**
                """)
            
elif  page == "📊 Data Visualization":

        final_query = "SELECT * FROM secure_check;"
        data = fetch_data(final_query) 

        
        st.header("🚔 Digital Ledger for Police Post Logs")

        st.dataframe(data)

        st.header("📈 Visual Insights")

        grouped = (
          data.groupby(["country_name", "violation", "stop_outcome"])
          .size()
          .reset_index(name="count")
         )
        

        chosen_outcome = st.selectbox("Choose Stop Outcome", grouped["stop_outcome"].unique())
        filtered = grouped[grouped["stop_outcome"] == chosen_outcome]
        fig = px.bar(
        filtered,
        x="country_name",
        y="count",
        color="violation",
        barmode="group",
        title=f"Violations by Country for Stop Outcome: {chosen_outcome}"
      )
        st.plotly_chart(fig, use_container_width=True)



elif  page == "🔰 Project Introduction":

    st.title("🚔 SecureCheck: A Python-SQL Digital Ledger for Police Post Logs")

    st.subheader(" 🚥 A Streamlit App for Exploring Police Logs")
    st.image("C:/Users/ACER/AppData/Roaming/Microsoft/Windows/Network Shortcuts/officer-giving-directions-to-tourist-using-sign-post-guidance-helpful-officer-directs-lost-tourist-sign-post-383650304.webp")

    st.write("""
    This project analyzes police logs for different queries and prediction using mysql database.
    It provides visualizations for violations done and outcome of logs.
    
    **Features:**
    - Predict stop outcome and violation in police_logs
    - View and filter police_logs data by violation and country.
    - Generate dynamic visualizations.
    - Run predefined SQL queries to explore insights.
             
    """)

    