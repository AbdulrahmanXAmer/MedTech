import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import re

# Load and preprocess data (assuming you have a file called 'medicine_data.csv')
salt_side_effects= pd.read_csv('./medicine_data.csv')

# # Function to extract salt names
# def extract_salts(salt_comp):
#     salts = re.findall(r'[A-Za-z\s]+(?=\s*\()', salt_comp)
#     return salts

# # Apply the function to the salt_composition column
# df['salt_names'] = df['salt_composition'].apply(extract_salts)

# # Explode the salt_names column to create one row per salt
# df_exploded = df.explode('salt_names')

# # Filter out any empty salt names
# df_exploded = df_exploded[df_exploded['salt_names'].str.strip() != '']

# # Group by salt names and aggregate side effects
# salt_side_effects = df_exploded.groupby('salt_names')['side_effects'].apply(lambda x: ', '.join(x)).reset_index()

# # Clean side effects
# def clean_side_effects(effects):
#     unique_effects = set([effect.strip() for effect in effects.split(',')])
#     return ', '.join(unique_effects)

# # Apply the cleaning function to the side_effects column
# salt_side_effects['side_effects'] = salt_side_effects['side_effects'].apply(clean_side_effects)

# Get unique salts for the dropdown options, ensuring empty names are excluded
salt_options = [{'label': salt, 'value': salt} for salt in salt_side_effects['salt_names'].unique() if salt]

# Create the Dash app
app = dash.Dash(__name__)

# Custom styles for UI/UX enhancements with uniform font size
app.layout = html.Div([
    html.Div([
        html.H1("Salt Composition and Side Effects", style={'textAlign': 'center', 'color': '#333', 'fontSize': '18px'}),
        
        # Instructions Section
        html.Div([
            html.H3("How to Use the Application", style={'fontSize': '18px', 'marginBottom': '10px'}),
            html.P("This application allows you to explore the relationship between different salts (drugs) and their associated side effects in a 3D interactive network graph.", style={'fontSize': '16px'}),
            html.P("To get started, select one or more salts from the dropdown below. The graph will visualize the selected salts and their side effects. You can zoom, rotate, and pan the graph to explore the connections. Salts are colored blue, and side effects are green.", style={'fontSize': '16px'}),
            html.P("Click 'Submit' after selecting your salts to update the graph.", style={'fontSize': '16px'}),
        ], style={'width': '60%', 'margin': 'auto', 'padding': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '10px', 'marginBottom': '20px'}),
        
        html.Div([
            html.Label("Select Salts:", style={'fontSize': '18px'}),
            dcc.Dropdown(
                id='salts',
                options=salt_options,
                value=['Dutasteride', 'Menthol'],  # Default values
                multi=True,  # Allow multiple selections
                clearable=True,
                style={'marginBottom': '20px'}
            ),
            html.Button(id='submit-button', n_clicks=0, children='Submit', style={
                'marginTop': '20px', 'padding': '10px 20px', 'backgroundColor': '#008CBA',
                'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '18px'
            })
        ], style={'width': '50%', 'margin': 'auto', 'fontSize': '18px'}),
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderBottom': '1px solid #ddd'}),

    # Graph Container
    html.Div([
        dcc.Graph(id='network-graph', config={'displayModeBar': False})
    ], style={'padding': '20px', 'fontSize': '18px'}),
])

# Callback to update the graph based on user input
@app.callback(
    Output('network-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [Input('salts', 'value')]
)
def update_graph(n_clicks, selected_salts):
    # Create a graph
    G = nx.Graph()

    # Add edges between salts and their side effects
    for i, row in salt_side_effects.iterrows():
        salt = row['salt_names']
        side_effects = row['side_effects'].split(',')
        for effect in side_effects:
            G.add_edge(salt, effect.strip())

    # Ensure that selected salts are in the graph
    existing_salts = [salt for salt in selected_salts if salt in G.nodes()]
    
    if not existing_salts:
        # Return an empty figure if none of the selected salts exist in the graph
        return go.Figure()

    # Create a subgraph containing only the selected salts and their side effects
    subgraph = G.subgraph(existing_salts + [effect for salt in existing_salts for effect in G.neighbors(salt)])

    # 3D spring layout
    pos = nx.spring_layout(subgraph, dim=3)

    # Create edges
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in subgraph.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create nodes with different colors for salts and side effects
    node_x = []
    node_y = []
    node_z = []
    node_text = []
    node_color = []

    for node in subgraph.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_text.append(node)

        # Differentiate salts and side effects by color
        if node in existing_salts:
            node_color.append('lightblue')  # Color for salts
        else:
            node_color.append('lightgreen')  # Color for side effects

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="top center",
        marker=dict(
            showscale=False,
            color=node_color,
            size=10,  # Same size for all nodes
            line_width=2),
        textfont=dict(
            size=12  # Uniform font size for all node labels
        )
    )

    # Create the figure with 3D graph, no axis tickers, and customized hover
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="3D Network Graph",
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        scene=dict(
                            xaxis=dict(showbackground=False, showticklabels=False, visible=False),
                            yaxis=dict(showbackground=False, showticklabels=False, visible=False),
                            zaxis=dict(showbackground=False, showticklabels=False, visible=False),
                        ),
                        annotations=[dict(
                            text="Salt composition network",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)]))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
