from functools import lru_cache

import pandas as pd
import reverse_geocode

from app.services.visualizer_services import DataVisualizer


@lru_cache(maxsize=1000)
def get_country_from_coords(lat, lon):
    result = reverse_geocode.search([(lat, lon)])
    return result[0]['country'] if result else 'Unknown'


def fill_country(df, batch_size=1000):
    # Check if we have the information we need
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("We need latitude and longitude to find the country.")
        return df

    # Create a COUNTRY column if it doesn't exist
    if 'country' not in df.columns:
        df['country'] = 'Unknown'

    try:
        # Go through the data in small groups
        for start in range(0, len(df), batch_size):
            end = start + batch_size

            # Get a small group of addresses
            addresses = list(zip(df['latitude'][start:end], df['longitude'][start:end]))

            # Find countries for these addresses all at once
            countries = reverse_geocode.search(addresses)

            # Put the countries we found into our data
            df.loc[start:end - 1, 'country'] = [c['country'] for c in countries]

    except Exception as e:
        print(f"Oops, something went wrong: {e}")

    return df


def get_device_count(df, diagram=None):
    visualizer = DataVisualizer()

    device_count = df.groupby(['device', 'local_ip_address', 'ip_address']).size().reset_index(name='Count')

    device_distribution = device_count.groupby('device')['Count'].sum().reset_index(name='Total Devices')

    if diagram:
        visualizer.create_bar_chart(device_distribution, 'device', "Total Devices", "Device count")

    return device_distribution


def get_device_type_count(df, diagram=None):
    visualizer = DataVisualizer()
    device_type_count = df.groupby(['device_version', 'local_ip_address', 'ip_address']).size().reset_index(
        name='Count')

    device_distribution = device_type_count.groupby('device_version')['Count'].sum().reset_index(name='Total Devices')
    if diagram:
        visualizer.create_bar_chart(device_distribution, 'device_version', "Total Devices", "Device type distribution")

    return device_distribution


def get_referer_count(df, diagram=None):
    visualizer = DataVisualizer()

    referer_count = df.groupby(['referer', 'local_ip_address', 'ip_address']).size().reset_index(name='Count')

    referer_distribution = referer_count.groupby('referer')['Count'].sum().reset_index(name='Total Referer')
    if diagram:
        visualizer.create_bar_chart(referer_distribution, 'referer', "Total Referer", "Referer distribution")

    return referer_distribution


def get_country_count(df, diagram=None):
    visualizer = DataVisualizer()
    country_count = df.groupby(['country']).size().reset_index(name='Count')
    if diagram:
        visualizer.create_pie_chart(country_count, 'country', 'Count', 'Country count')
    return country_count


def get_voyage_count(df, diagram=None):
    visualizer = DataVisualizer()

    country_count = df.groupby(['voyage_identifier']).size().reset_index(name='Count')

    total_count = country_count['Count'].sum()
    country_count['Percentage'] = (country_count['Count'] / total_count) * 100
    if diagram:
        visualizer.create_bar_chart(country_count, 'voyage_identifier', 'Count', "Voyage count")

    return country_count


def get_voyage_country_count(df, voyage_id, diagram=None):
    # Filter the dataframe for the given voyage_id
    df = df[df['voyage_identifier'] == voyage_id]

    # Create an instance of the DataVisualizer
    visualizer = DataVisualizer()

    # Group by 'COUNTRY' and count the occurrences
    country_count = df.groupby(['country']).size().reset_index(name='Count')

    # Calculate the total count and percentage for each country
    total_count = country_count['Count'].sum()
    country_count['Percentage'] = (country_count['Count'] / total_count) * 100

    # Optionally create a pie chart
    if diagram:
        visualizer.create_pie_chart(country_count, 'country', 'Count', title=f'Country Count for Voyage {voyage_id}')

    return country_count


def get_global_search_theme(df, start_date, end_date, diagram=None):
    visualizer = DataVisualizer()

    # Convert DEPARTURE_DATE to datetime if it's not already
    df['departure_date'] = pd.to_datetime(df['departure_date'])

    # Filter the dataframe by the given date range
    df_filtered = df[(df['departure_date'] >= start_date) & (df['departure_date'] <= end_date)]

    # Group by THEMES only
    search_theme = df_filtered.groupby(['themes']).size().reset_index(name='Count')

    total_count = search_theme['Count'].sum()
    search_theme['Percentage'] = (search_theme['Count'] / total_count) * 100

    # Optional visualization
    if diagram:
        visualizer.create_bar_chart(search_theme, 'themes', 'Count', "Global theme search")

    return search_theme


def get_global_search_region(df, start_date, end_date, diagram=None):
    visualizer = DataVisualizer()

    # Convert DEPARTURE_DATE to datetime if it's not already
    df['departure_date'] = pd.to_datetime(df['departure_date'])

    # Filter the dataframe by the given date range
    df_filtered = df[(df['departure_date'] >= start_date) & (df['departure_date'] <= end_date)]

    # Group by REGIONS only
    search_region = df_filtered.groupby(['regions']).size().reset_index(name='Count')

    total_count = search_region['Count'].sum()
    search_region['Percentage'] = (search_region['Count'] / total_count) * 100

    # Optional visualization
    if diagram:
        visualizer.create_bar_chart(search_region, 'regions', 'Count', "Global search region")

    return search_region


def get_global_sale(df, start_date, end_date, period_type, diagram=None):
    # Ensure 'CREATE_DATE' is a datetime type
    df['create_date'] = pd.to_datetime(df['create_date'])

    # Determine the period frequency based on period_type
    if period_type == 'year':
        period_freq = 'Y'
    elif period_type == 'month':
        period_freq = 'M'
    elif period_type == 'week':
        period_freq = 'W'
    elif period_type == 'day':
        period_freq = 'D'
    else:
        raise ValueError("Invalid period_type. Must be 'year', 'month', 'week' or 'day'.")

    # Filter the data between start_date and end_date
    df = df[(df['create_date'] >= pd.to_datetime(start_date)) & (df['create_date'] <= pd.to_datetime(end_date))]

    # Create period column
    df['period'] = df['create_date'].dt.to_period(period_freq)

    # Group by the determined period and calculate the number of '/devis' and '/buy'
    result = df.groupby('period').agg(
        Nb_de_Devis=('url_visited', lambda x: x.str.contains('/devis').sum()),
        Nb_de_Vente=('url_visited', lambda x: x.str.contains('/buy').sum())
    ).reset_index()

    # Convert 'PERIOD' to string for proper plotting
    result['period'] = result['period'].astype(str)

    # Prepare the parameters for the multi-line chart
    x_column = 'period'  # x-axis for the chart
    y_columns = ['Nb_de_Devis', 'Nb_de_Vente']  # y-axis columns
    chart_title = 'Global sale'
    custom_colors = ['red', 'blue']  # Colors for the lines

    # Create the DataVisualizer instance
    visualizer = DataVisualizer()

    if diagram:
        # Use the visualizer to create the multi-line chart
        visualizer.create_multi_line_chart(result, x_column, y_columns, chart_title, colors=custom_colors)

    return result


def get_voyage_sale(df, voyage_id, start_date, end_date, period_type, diagram=None):
    # Ensure 'CREATE_DATE' is a datetime type
    df['create_date'] = pd.to_datetime(df['create_date'])

    # Determine the period frequency based on period_type
    if period_type == 'year':
        period_freq = 'Y'
    elif period_type == 'month':
        period_freq = 'M'
    elif period_type == 'week':
        period_freq = 'W'
    elif period_type == 'day':
        period_freq = 'D'
    else:
        raise ValueError("Invalid period_type. Must be 'year', 'month', 'week' or 'day'.")

    # Filter the data for the given voyage_id and between start_date and end_date
    df = df[(df['voyage_identifier'] == voyage_id) &
            (df['create_date'] >= pd.to_datetime(start_date)) &
            (df['create_date'] <= pd.to_datetime(end_date))]

    # Create period column
    df['period'] = df['create_date'].dt.to_period(period_freq)

    # Group by the determined period and calculate the number of '/devis' and '/buy'
    result = df.groupby('period').agg(
        Nb_de_Devis=('url_visited', lambda x: x.str.contains('/devis').sum()),
        Nb_de_Vente=('url_visited', lambda x: x.str.contains('/buy').sum())
    ).reset_index()

    result['period'] = result['period'].astype(str)

    # Prepare the parameters for the multi-line chart
    x_column = 'period'  # x-axis for the chart
    y_columns = ['Nb_de_Devis', 'Nb_de_Vente']  # y-axis columns
    chart_title = f'Sales and Devis for Voyage {voyage_id}'
    custom_colors = ['red', 'blue']  # Colors for the lines

    visualizer = DataVisualizer()
    if diagram:
        visualizer.create_multi_line_chart(result, x_column, y_columns, chart_title, colors=custom_colors)
    return result


def get_tour_operateur_sale(df, user, start_date, end_date, period_type, diagram=None):
    df['create_date'] = pd.to_datetime(df['create_date'])

    if period_type == 'year':
        period_freq = 'Y'
    elif period_type == 'month':
        period_freq = 'M'
    elif period_type == 'week':
        period_freq = 'W'
    elif period_type == 'day':
        period_freq = 'D'
    else:
        raise ValueError("Invalid period_type. Must be 'year', 'month', 'week' or 'day'.")

    # Filter the data for the given voyage_id and between start_date and end_date
    df = df[(df['created_by'] == user) &
            (df['create_date'] >= pd.to_datetime(start_date)) &
            (df['create_date'] <= pd.to_datetime(end_date))]

    # Create period column
    df['period'] = df['create_date'].dt.to_period(period_freq)

    # Group by the determined period and calculate the number of '/devis' and '/buy'
    result = df.groupby('period').agg(
        Nb_de_Devis=('url_visited', lambda x: x.str.contains('/devis').sum()),
        Nb_de_Vente=('url_visited', lambda x: x.str.contains('/buy').sum())
    ).reset_index()

    result['period'] = result['period'].astype(str)

    # Prepare the parameters for the multi-line chart
    x_column = 'period'  # x-axis for the chart
    y_columns = ['Nb_de_Devis', 'Nb_de_Vente']  # y-axis columns
    chart_title = f'Sales and Devis for {user}'
    custom_colors = ['red', 'blue']  # Colors for the lines

    visualizer = DataVisualizer()
    if diagram:
        visualizer.create_multi_line_chart(result, x_column, y_columns, chart_title, colors=custom_colors)
    return result
