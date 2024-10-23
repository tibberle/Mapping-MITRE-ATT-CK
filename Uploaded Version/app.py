import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Load your dataset from an Excel file, reading all sheets into a dictionary
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Create the relative file path
file_path = os.path.join(current_dir, "./enterprise-attack-v15.1.xlsx")
sheets = pd.read_excel(file_path, sheet_name=None)


# Select the relevant sheets for techniques and data analysis
techniques = sheets['techniques']
data_analysis_sheet = sheets['DataAnalysis']

# Extract relevant columns from the techniques sheet
techniques_relevant = techniques[['ID', 'name', 'description', 'tactics', 'platforms', 'is sub-technique', 
                                   'sub-technique of', 'created', 'last modified', 'detection']]

# Filter out main techniques that are not sub-techniques
main_techniques = techniques_relevant[techniques_relevant['is sub-technique'] == False]

# Predefined dropdown options for tactics and platforms for filtering
tactic_options = [
    {'label': 'Defense Evasion', 'value': 'Defense Evasion'},
    {'label': 'Privilege Escalation', 'value': 'Privilege Escalation'},
    {'label': 'Collection', 'value': 'Collection'},
    {'label': 'Command and Control', 'value': 'Command and Control'},
    {'label': 'Credential Access', 'value': 'Credential Access'},
    {'label': 'Discovery', 'value': 'Discovery'},
    {'label': 'Execution', 'value': 'Execution'},
    {'label': 'Exfiltration', 'value': 'Exfiltration'},
    {'label': 'Impact', 'value': 'Impact'},
    {'label': 'Initial Access', 'value': 'Initial Access'},
    {'label': 'Lateral Movement', 'value': 'Lateral Movement'},
    {'label': 'Persistence', 'value': 'Persistence'},
    {'label': 'Reconnaissance', 'value': 'Reconnaissance'},
    {'label': 'Resource Development', 'value': 'Resource Development'},
]

platform_options = [
    {'label': 'Azure AD', 'value': 'Azure AD'},
    {'label': 'Google Workspace', 'value': 'Google Workspace'},
    {'label': 'IaaS', 'value': 'IaaS'},
    {'label': 'Linux', 'value': 'Linux'},
    {'label': 'Office 365', 'value': 'Office 365'},
    {'label': 'Windows', 'value': 'Windows'},
    {'label': 'macOS', 'value': 'macOS'},
    {'label': 'SaaS', 'value': 'SaaS'},
    {'label': 'Containers', 'value': 'Containers'},
    {'label': 'Network', 'value': 'Network'},
    {'label': 'PRE', 'value': 'PRE'},
]

# Create a Dash app and include external stylesheets for Bootstrap
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

# Function to create a table of techniques grouped by tactics
def create_tactic_table():
    # Create a list to hold table rows
    table_rows = []
    
    # Get a unique list of tactics without any grouping
    unique_tactics = main_techniques['tactics'].str.split(', ').explode().unique()

    # Create a mapping of tactics to their techniques
    tactic_to_techniques = {tactic: [] for tactic in unique_tactics}

    for _, technique in main_techniques.iterrows():
        # Split tactics in case of multiple
        tactics_list = technique['tactics'].split(", ") if isinstance(technique['tactics'], str) else [technique['tactics']]
        for tactic in tactics_list:
            tactic_to_techniques[tactic].append(technique)

    # Create table headers with tactics as column headers
    table_header = [
        html.Tr([html.Th(tactic) for tactic in unique_tactics])
    ]

    # Find the maximum number of techniques for any tactic
    max_techniques = max(len(techniques) for techniques in tactic_to_techniques.values())

    # Iterate to create rows for the table
    for i in range(max_techniques):
        row = []
        for tactic in unique_tactics:
            # Get techniques for the current tactic
            techniques = tactic_to_techniques[tactic]
            if i < len(techniques):
                technique = techniques[i]
                row.append(html.Td(
                    html.A(technique['name'], href=f"/techniques/{technique['ID']}", style={"text-decoration": "underline", "color": "#007bff"}),
                    style={"border": "1px solid #ddd", "padding": "8px", "backgroundColor": "#f8f9fa"} 
                ))
            else:
                row.append(html.Td(''))  # Empty cell if no more techniques

        table_rows.append(html.Tr(row))

    # Return the complete table
    return html.Table(children=table_header + table_rows, style={"border-collapse": "collapse", "width": "100%", "margin-bottom": "20px", "border": "1px solid #ddd"})

# Function to create a detailed view for a specific technique
def detail_page(technique_id):
    try:
        # Retrieve the technique by its ID
        tech = techniques_relevant[techniques_relevant['ID'] == technique_id].iloc[0]
    except IndexError:
        return html.Div("Error: Technique not found.")

    # Find any sub-techniques related to this technique
    sub_techniques = techniques_relevant[techniques_relevant['sub-technique of'] == technique_id]

    # Create a link back to the parent technique if it exists
    parent_technique_link = None
    if pd.notna(tech['sub-technique of']):
        parent_id = tech['sub-technique of']
        parent_technique_link = html.A(
            "Back to Parent Technique",
            href=f"/techniques/{parent_id}",
            className='btn btn-secondary',
            style={"margin-top": "20px", "margin-right": "10px"}
        )
    
    # Create a link to go back to the main techniques table
    back_to_table_link = html.A(
        "Back to Techniques Table",
        href="/",
        className='btn btn-primary',
        style={"margin-top": "20px"}
    )

    # Prepare the detection content
    detection_content = html.Div([
        html.H3("Detection", style={"margin-top": "20px"}),
        html.P(tech['detection']) if pd.notna(tech['detection']) else html.P("No detection information available.")
    ])

    # Prepare the content for sub-techniques
    sub_techniques_content = html.Div([
        html.H3("Sub-techniques", style={"margin-top": "20px"}),
        html.Ul([
            html.Li(html.A(sub_tech['name'], href=f"/techniques/{sub_tech['ID']}", target="_blank"))
            for _, sub_tech in sub_techniques.iterrows()
        ]) if not sub_techniques.empty else html.P("No sub-techniques available")
    ])

    # Create a section for Detection and Sub-techniques
    tags_section = html.Div([
        html.Div(detection_content, style={"margin-bottom": "20px"}),
        html.Div(sub_techniques_content)
    ], style={"padding": "15px", "border": "1px solid #ddd", "border-radius": "5px", "background-color": "#f9f9f9"})

    # Return the detailed view layout
    return html.Div([
        html.H1(tech['name'], style={"color": "#003366"}),
        html.P(f"Tactic: {tech['tactics']}"),
        html.P(f"Description: {tech['description']}"),
        html.P(f"Platforms: {tech['platforms']}"),
        html.P(f"Date Created: {tech['created']}"),
        html.P(f"Last Modified: {tech['last modified']}"),
        tags_section,  # Add the tags section here
        parent_technique_link,
        back_to_table_link
    ], style={"margin": "20px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px", "background-color": "#f9f9f9"})

# Function to create the data analysis visualization
def data_analysis_visualisation():
    # Group the data by platforms and calculate the sum of counts
    grouped_data = data_analysis_sheet.groupby('Platforms').sum().reset_index()
    grouped_data = grouped_data.sort_values(by='Count', ascending=False)

    # Create a bar chart for the data visualization
    fig = px.bar(
        grouped_data, 
        x='Platforms', 
        y='Count', 
        color='Platforms',  
        title='Number of Techniques by Individual Platform',
        text='Count'  
    )

    # Update traces for the figure for better display
    fig.update_traces(texttemplate='%{text}', textposition='outside')  
    fig.update_layout(
        yaxis_title='Count', 
        xaxis_title='Platforms',
        height=625
    )

    # Return the visualization component
    return html.Div([
        html.H2("Data Analysis Visualisation", style={"margin-top": "20px"}),
        dcc.Graph(id='data-analysis-graph', figure=fig)
    ], style={"padding": "20px", "margin": "20px", "border": "1px solid #ddd", "border-radius": "5px", "background-color": "#f9f9f9"})

# Function to filter techniques and sub-techniques based on selected tactics and platforms
def filter_techniques(selected_tactics, selected_platforms):
    filtered = techniques_relevant.copy()

    # Apply filtering based on selected tactics if any are selected
    if selected_tactics:
        filtered = filtered[filtered['tactics'].apply(lambda x: all(tactic in x for tactic in selected_tactics))]

    # Apply filtering based on selected platforms if any are selected
    if selected_platforms:
        filtered = filtered[filtered['platforms'].apply(lambda x: all(platform in x for platform in selected_platforms))]
    
    # If no techniques are found after filtering, return a message
    if filtered.empty:
        return html.Div("No techniques or sub-techniques found for the selected filters.")
    
    count_display = html.Div(f"Total records found: {len(filtered)}", style={"font-weight": "bold", "margin-bottom": "10px"})

    # Create a list of technique cards for the filtered results
    technique_cards = [
        html.Div(className='card mb-3', style={"padding": "15px"}, children=[
            html.Div(className='card-body', children=[
                html.H5(className='card-title', children=technique['name']),
                html.P(f"ID: {technique['ID']}", className='card-text'),
                html.P(f"Tactics: {technique['tactics']}", className='card-text'),
                html.P(f"Platforms: {technique['platforms']}", className='card-text'),
                html.A("View Technique", href=f"/techniques/{technique['ID']}", className='btn btn-secondary', target="_blank")
            ])
        ]) for _, technique in filtered.iterrows()
    ]

    # Return the filtered results along with the count display
    return html.Div([count_display] + technique_cards, style={"margin-top": "20px"})

# Update app layout with tabs and location for routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Techniques Table', value='tab-1'),
        dcc.Tab(label='Data Analysis', value='tab-2'),
        dcc.Tab(label='Query Techniques', value='tab-3'),
    ], style={"fontWeight": "bold"}, className='nav nav-tabs'),
    html.Div(id='tabs-content', className='mt-4')
])

# Callback to switch between tabs and handle URL routing
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'), Input('url', 'pathname')]
)
def render_content(tab, pathname):
    # If the URL is for a specific technique, render its detail page
    if pathname and pathname.startswith('/techniques/'):
        try:
            technique_id = pathname.split('/')[2]
            return detail_page(technique_id)
        except IndexError:
            return html.Div("Error: Invalid technique URL.")
    
    # Render the corresponding content based on the selected tab
    if tab == 'tab-1':
        return create_tactic_table()
    elif tab == 'tab-2':
        return data_analysis_visualisation()
    elif tab == 'tab-3':
        return html.Div([
            html.H2("Filter Techniques", className="mb-3"),
            html.Div(className="row", children=[
                html.Div(className="col-md-6 mb-3", children=[
                    html.Label("Choose Tactics:"),
                    dcc.Dropdown(
                        id='tactic-dropdown',
                        options=tactic_options,
                        value=[],
                        multi=True,  # Enable multi-select
                        placeholder="Select tactics",
                        className='form-control'  # Bootstrap styling
                    )
                ]),
                html.Div(className="col-md-6 mb-3", children=[
                    html.Label("Choose Platforms:"),
                    dcc.Dropdown(
                        id='platform-dropdown',
                        options=platform_options,
                        value=[],
                        multi=True,  # Enable multi-select
                        placeholder="Select platforms",
                        className='form-control'  # Bootstrap styling
                    )
                ])
            ]),
            # Button to trigger the filtering action
            html.Button('Search', id='search-button', className='btn btn-primary mb-3'),
            html.Div(id='filter-results', style={"margin-top": "20px"})
        ], style={"padding": "20px", "margin": "20px", "border": "1px solid #ddd", "border-radius": "5px", "background-color": "#f9f9f9"})  # Added padding to filter section

# Callback to handle filtering of techniques and sub-techniques
@app.callback(
    Output('filter-results', 'children'),
    [Input('search-button', 'n_clicks')],
    [Input('tactic-dropdown', 'value'), Input('platform-dropdown', 'value')]
)
def update_filter_results(n_clicks, selected_tactics, selected_platforms):
    # When the search button is clicked, update the filter results
    if n_clicks is not None and n_clicks > 0:
        return filter_techniques(selected_tactics, selected_platforms)
    return ""

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
