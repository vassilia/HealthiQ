from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Load the Excel file
file_path = 'data_raw.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')  # Ensure this line loads the data as a DataFrame

# Prepare data
current_year = 2025
data['Age'] = current_year - data['BIRTH']
age_bins = [0, 12, 18, 39, 65, 75, 85, 90, np.inf]
age_labels = ['0-12', '13-18', '19-39', '40-65', '66-75', '76-85', '86-90', '90+']
data['Age Group'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels, right=False)
discharge_columns = [col for col in data.columns if 'DischargeReason' in col]
data['Gender'] = data['gender Male -1 Female 0'].replace({1: 'Male', 0: 'Female'})

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Discharge Reasons Analysis Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Age Group:"),
        dcc.Dropdown(
            id='age-group-dropdown',
            options=[{'label': age, 'value': age} for age in age_labels],
            value='40-65',
            clearable=False,
        )
    ], style={'width': '40%', 'margin': '0 auto'}),

    html.Div([
        dcc.Graph(id='stacked-bar-chart'),
        dcc.Graph(id='donut-chart'),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around'}),
])


# Callback to update the stacked bar chart
@app.callback(
    Output('stacked-bar-chart', 'figure'),
    Input('age-group-dropdown', 'value')
)
def update_stacked_bar_chart(selected_age_group):
    filtered_data = data[data['Age Group'] == selected_age_group]
    male_data = filtered_data[filtered_data['Gender'] == 'Male'][discharge_columns].sum()
    female_data = filtered_data[filtered_data['Gender'] == 'Female'][discharge_columns].sum()

    combined_data = pd.DataFrame({'Male': male_data, 'Female': female_data}).reset_index()
    combined_data.columns = ['Discharge Reason', 'Male', 'Female']
    melted_data = combined_data.melt(id_vars='Discharge Reason', var_name='Gender', value_name='Count')

    fig = px.bar(
        melted_data,
        x='Discharge Reason',
        y='Count',
        color='Gender',
        barmode='stack',
        title=f"Discharge Reasons for Age Group: {selected_age_group}",
        labels={'Count': 'Count', 'Discharge Reason': 'Discharge Reason'}
    )
    return fig


# Callback to update the donut chart
@app.callback(
    Output('donut-chart', 'figure'),
    Input('age-group-dropdown', 'value')
)
def update_donut_chart(selected_age_group):
    filtered_data = data[data['Age Group'] == selected_age_group]
    male_data = filtered_data[filtered_data['Gender'] == 'Male'][discharge_columns].sum()
    female_data = filtered_data[filtered_data['Gender'] == 'Female'][discharge_columns].sum()
    total_data = male_data + female_data

    fig = px.pie(
        names=discharge_columns,
        values=total_data,
        title=f"Distribution of Discharge Reasons for Age Group: {selected_age_group}",
        hole=0.5
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
