import streamlit as st
import pandas as pd
from datetime import datetime
from read_data import data_reader
import plotly.express as px

def select_gas():
    """Create a dropdown to select the gas type."""
    selected_gas = st.selectbox(
        "Select Gas",
        ("Select Gas", "CO2")
    )
    return selected_gas.lower()

def select_year():
    """Create a dropdown to select the year."""
    selected_year = st.selectbox(
        "Select Year",
        ['Select Year'] + list(range(2000, datetime.now().year + 1))
    )
    return selected_year if selected_year != 'Select Year' else None

def select_month():
    """Create a dropdown to select the month."""
    selected_month = st.selectbox(
        "Select Month",
        ['Select Month', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
    month_dict = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    return month_dict.get(selected_month, None)  # Return None if 'Select Month'

def get_data_source(selected_gas):
    """Retrieve data from the selected gas CSV file."""
    file_path = f"data/{selected_gas}.csv"

    if selected_gas == "select gas":
        return None

    try:
        return data_reader(file_path)
    except FileNotFoundError:
        st.error(f"No file found for {selected_gas}")
        return None

def generate_story(df, selected_gas, selected_year=None, selected_month=None, chart_type=None):
    """Generate a story based on user selections and chart type."""
    total_rows = len(df)
    gas_name = selected_gas.upper()

    # Story generation based on chart type
    if chart_type == "line":
        story_type = "Line Chart"
    elif chart_type == "scatter":
        story_type = "Scatter Plot"
    elif chart_type == "std_scatter":
        story_type = "Standard Deviation Scatter Plot"
    else:
        story_type = "Data Overview"

    if selected_year and selected_month:
        story = (f"The {story_type} represents the concentration of {gas_name} during "
                 f"{datetime(2000, selected_month, 1).strftime('%B')} {selected_year}. The dataset contains "
                 f"{total_rows} data points for this time period, showing how the concentration of {gas_name} "
                 "varied across this month.")
    elif selected_year:
        story = (f"The {story_type} highlights the {gas_name} levels recorded in {selected_year}. "
                 f"There are {total_rows} data points representing {gas_name} concentration changes over the year. "
                 "This visualization captures the yearly fluctuation and trends in gas concentration.")
    else:
        story = (f"The {story_type} covers the full dataset with {total_rows} records for {gas_name}. "
                 "This chart provides a comprehensive overview of {gas_name} concentrations over the entire recorded "
                 "period, allowing us to observe both seasonal and longer-term trends.")
    
    return story

def draw_time_series(df, selected_gas, selected_year=None, selected_month=None):
    """Draw time series plots based on user selections and generate a story."""
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows where 'date' conversion failed
    df.dropna(subset=['date'], inplace=True)

    # Extract the year for grouping
    df['year'] = df['date'].dt.year

    # Display full dataset initially (without filters)
    if selected_year is None and selected_month is None:
        fig = px.line(df, x='date', y='Alt_Mean', title='Full Dataset: Alt_Mean Over Time')
        st.plotly_chart(fig, use_container_width=True)
        st.write(generate_story(df, selected_gas, chart_type="line"))
    
    # If user selects a year but not a month
    elif selected_year is not None and selected_month is None:
        filtered_df = df[df['year'] == selected_year]
        if not filtered_df.empty:
            fig = px.line(filtered_df, x='date', y='Alt_Mean', title=f'Alt_Mean Over Time in {selected_year}')
            st.plotly_chart(fig, use_container_width=True)
            st.write(generate_story(filtered_df, selected_gas, selected_year, chart_type="line"))
        else:
            st.warning("No data available for the selected year.")
    
    # If user selects both year and month
    elif selected_year is not None and selected_month is not None:
        filtered_df = df[(df['year'] == selected_year) & (df['date'].dt.month == selected_month)]
        if not filtered_df.empty:
            fig = px.line(filtered_df, x='date', y='std CO2', title=f'Standard Deviation of CO2 in {selected_month} {selected_year}')
            st.plotly_chart(fig, use_container_width=True)
            st.write(generate_story(filtered_df, selected_gas, selected_year, selected_month, chart_type="line"))
        else:
            st.warning("No data available for the selected month and year.")

def draw_scatter_plot(df, selected_gas, selected_year=None, selected_month=None):
    """Generate scatter plots based on user selections and generate a story."""
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows where 'date' conversion failed
    df.dropna(subset=['date'], inplace=True)

    # Extract the year for grouping
    df['year'] = df['date'].dt.year

    # Display full dataset initially (without filters)
    if selected_year is None and selected_month is None:
        fig = px.scatter(df, x='date', y='Alt_Mean', title='Full Dataset: Alt_Mean Over Time')
        st.plotly_chart(fig, use_container_width=True)
        st.write(generate_story(df, selected_gas, chart_type="scatter"))
    
    # If user selects a year but not a month
    elif selected_year is not None and selected_month is None:
        filtered_df = df[df['year'] == selected_year]
        if not filtered_df.empty:
            fig = px.scatter(filtered_df, x='date', y='Alt_Mean', title=f'Alt_Mean Over Time in {selected_year}')
            st.plotly_chart(fig, use_container_width=True)
            st.write(generate_story(filtered_df, selected_gas, selected_year, chart_type="scatter"))
        else:
            st.warning("No data available for the selected year.")
    
    # If user selects both year and month
    elif selected_year is not None and selected_month is not None:
        filtered_df = df[(df['year'] == selected_year) & (df['date'].dt.month == selected_month)]
        if not filtered_df.empty:
            fig = px.scatter(filtered_df, x='date', y='Alt_Mean', title=f'Alt_Mean Over Time in {selected_month} {selected_year}')
            st.plotly_chart(fig, use_container_width=True)
            st.write(generate_story(filtered_df, selected_gas, selected_year, selected_month, chart_type="scatter"))
        else:
            st.warning("No data available for the selected month and year.")

def draw_std_co2_scatter_plot(df, selected_gas, selected_year=None, selected_month=None):
    """Generate scatter plots using std CO2 based on user selections and generate a story."""
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows where 'date' conversion failed
    df.dropna(subset=['date'], inplace=True)

    # Extract the year for grouping
    df['year'] = df['date'].dt.year

    # Display full dataset initially (without filters)
    if selected_year is None and selected_month is None:
        fig = px.scatter(df, x='date', y='std CO2', title='Full Dataset: std CO2 Over Time')
        st.plotly_chart(fig, use_container_width=True)
        st.write(generate_story(df, selected_gas, chart_type="std_scatter"))
    
    # If user selects a year but not a month
    elif selected_year is not None and selected_month is None:
        filtered_df = df[df['year'] == selected_year]
        if not filtered_df.empty:
            fig = px.scatter(filtered_df, x='date', y='std CO2', title=f'std CO2 Over Time in {selected_year}')
            st.plotly_chart(fig, use_container_width=True)
            st.write(generate_story(filtered_df, selected_gas, selected_year, chart_type="std_scatter"))
        else:
            st.warning("No data available for the selected year.")
    
    # If user selects both year and month
    elif selected_year is not None and selected_month is not None:
        filtered_df = df[(df['year'] == selected_year) & (df['date'].dt.month == selected_month)]
        if not filtered_df.empty:
            fig = px.scatter(filtered_df, x='date', y='std CO2', title=f'std CO2 Over Time in {selected_month} {selected_year}')
            st.plotly_chart(fig, use_container_width=True)
            st.write(generate_story(filtered_df, selected_gas, selected_year, selected_month, chart_type="std_scatter"))
        else:
            st.warning("No data available for the selected month and year.")

def main():
    """Main application function."""
    st.title("Atmospheric Gases Concentration Dashboard")

    selected_gas = select_gas()
    selected_year = select_year()
    selected_month = select_month()

    if selected_gas == "select gas":
        st.info("Please select a gas to start.")
        return

    df = get_data_source(selected_gas)

    if df is not None:
        draw_time_series(df, selected_gas, selected_year, selected_month)
        draw_scatter_plot(df, selected_gas, selected_year, selected_month)
        draw_std_co2_scatter_plot(df, selected_gas, selected_year, selected_month)

if __name__ == "__main__":
    main()
