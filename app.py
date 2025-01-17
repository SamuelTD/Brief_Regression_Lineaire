import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import pearsonr

# Load your data
df = pd.read_pickle('exp_data.pkl')

# Puting my numerical variables in categories 
ages_bin_edges = [0, 25, 55, float('inf')]  # Float('inf') for ages 55+
ages_bin_labels = ['<25', '25-55', '55+']


bmi_bin_edges = [0, 18.5, 24.29, 29.9 ,float('inf')]  # Float('inf') for bmi 29.9
bmi_bin_labels = ['<Under_weight','Regular_weight','Over_weight','Obese']

# Create the age binned column
df['age_category'] = pd.cut(df['age'], bins=ages_bin_edges, labels=ages_bin_labels, right=False)

# Create the bmi binned column
df['bmi_category'] = pd.cut(df['bmi'], bins=bmi_bin_edges, labels=bmi_bin_labels, right=False)


# Streamlit app title
st.title("Market Research for Insurance Prices")

# Assuming `df` and `numerical_vars` are pre-defined
# Replace these with your actual DataFrame and variable lists
# df = your_dataframe
numerical_vars = ['age', 'bmi', 'children']
# new_categorical_columns = ['sex', 'region', 'smoker', 'age_category', 'bmi_category']

# Calculate metrics
total_charges = df['charges'].sum()
total_clients = len(df)

# Layout: Two columns for cards, followed by graphics and scatter plots
col1, col2 = st.columns(2)

# Display cards
with col1:
    st.metric("Total Charges", f"${total_charges:,.2f}")

with col2:
    st.metric("Total Clients", total_clients)

# Interactive Graphics for Categorical Variables
st.subheader("Analysis of Categorical Variables")

new_categorical_columns = ['sex', 'region', 'smoker', 'age_category', 'bmi_category']
for var in new_categorical_columns:
    # Create a subplot for each categorical variable
    fig = make_subplots(rows=1, cols=1)

    # Bar plot: Mean charges by category
    mean_values = df.groupby(var)['charges'].mean()
    bar = go.Bar(
        x=mean_values.index,
        y=mean_values,
        name=f"Bar {var}",
        visible=True  # Default visibility
    )

    # Add mean annotations
    bar_annotations = [
        go.layout.Annotation(
            x=x_pos,
            y=y_pos,
            text=f'{y_pos:.2f}',
            showarrow=False,
            font=dict(size=12),
            bgcolor='white',
            xanchor='center',
            yanchor='bottom'
        )
        for x_pos, y_pos in zip(mean_values.index, mean_values)
    ]

    # Box plot: Charges distribution by category
    box = go.Box(
        x=df[var],
        y=df['charges'],
        name=f"Box {var}",
        visible=False  # Default visibility is off
    )

    # Violin plot: Charges distribution by category
    violin = go.Violin(
        x=df[var],
        y=df['charges'],
        name=f"Violin {var}",
        box_visible=True,
        visible=False  # Default visibility is off
    )

    # Add all traces and annotations
    fig.add_trace(bar)
    fig.add_trace(box)
    fig.add_trace(violin)
    fig.update_layout(annotations=bar_annotations)

    # Buttons for switching between plot types
    buttons = [
        {'label': 'Bar', 'method': 'update', 'args': [{'visible': [True, False, False]}, {'title': f'Average Insurance Price per {var} - Bar Plot'}]},
        {'label': 'Box', 'method': 'update', 'args': [{'visible': [False, True, False]}, {'title': f'Insurance Price Distribution per {var} - Box Plot'}]},
        {'label': 'Violin', 'method': 'update', 'args': [{'visible': [False, False, True]}, {'title': f'Insurance Price Distribution per {var} - Violin Plot'}]}
    ]

    # Update layout with buttons
    fig.update_layout(
        title=f'Choose Plot Type for {var}',
        updatemenus=[{
            'buttons': buttons,
            'direction': 'down',
            'showactive': True,
            'x': 1.1,
            'xanchor': 'left',
            'y': 0.5,
            'yanchor': 'middle'
        }],
        showlegend=True,
        height=600,
        width=800
    )

    # Display the figure in Streamlit
    st.plotly_chart(fig)

# Scatter Plots for Numerical Variables
st.subheader("Analysis of Numerical Variables Per Smoker Category")

numerical_vars = ['age', 'bmi', 'children']  # Replace with your actual numerical variables
for var in numerical_vars:
    if var != "charges":
        # Pearson correlation
        corr, _ = pearsonr(df[var], df['charges'])

        # Scatter plot with regression line
        fig = px.scatter(
            df,
            x=var,
            y='charges',
            color='smoker',
            trendline='ols',
            title=f"Insurance Charges vs {var} (Pearson r = {corr:.2f})",
            labels={var: var.capitalize(), 'charges': 'Charges'},
            template='plotly_white'
        )
        fig.update_layout(
            title_font_size=16,
            xaxis_title=var.capitalize(),
            yaxis_title='Charges',
            legend_title_text='Smoker Status',
            height=500
        )
        st.plotly_chart(fig)
