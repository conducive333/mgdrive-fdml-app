import dash_html_components as html
import dash_core_components as dcc

def get_marks(start, end, step, norm=None):
    marks = dict()
    for i in range(start, end, step):
        if norm:
            if i == start or i == end - 1:
                marks[int(i / norm)] = str(int(i / norm))
            else:
                marks[i / norm] = str(i / norm)
        else:
            marks[i] = str(i)
    return marks

def mdl_div(model_keys):
    if len(model_keys) == 0: raise ValueError("Found 0 models to use!")
    mink = min(model_keys)
    maxk = max(model_keys)
    return html.Div([
        html.H5('Model:'),
        dcc.Slider(
            id='mdl-slider',
            min=mink,
            max=maxk,
            step=None,
            value=maxk,
            marks={ k : str(k) for k in model_keys }
        )
    ])

sex_div = html.Div([
    html.H5('Gender:'),
    dcc.RadioItems(
        id='sex-radio',
        options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Gravid Female', 'value': 'Gravid Female'},
            {'label': 'Non Gravid Female', 'value': 'Non Gravid Female'}
        ],
        value='Male',
        labelStyle={'display': 'block'}
    )
])

gsv_div = html.Div([
    html.H5('Genetic Standing Variation:'),
    dcc.Input(
        id="gsv-input",
        type="number",
        value=1e-3
    )
])

rsg_div = html.Div([
    html.H5('Resistance Generation:'),
    dcc.Input(
        id="rsg-input",
        type="number",
        value=1e-5
    )
])

rer_div = html.Div([
    html.H5('Released Fraction:'),
    dcc.Slider(
        id='rer-slider',
        min=0,
        max=1,
        step=0.1,
        value=0.5,
        marks=get_marks(0, 10 + 1, 1, 10)
    )
])

fic_div = html.Div([
    html.H5('Fitness Cost:'),
    dcc.Slider(
        id='fic-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.5,
        marks=get_marks(0, 100 + 1, 5, 100)
    )
])

ren_div = html.Div([
    html.H5('Release Number (weekly):'),
    dcc.Slider(
        id='ren-slider',
        min=0,
        max=10,
        step=1,
        value=5,
        marks=get_marks(0, 10 + 1, 1)
    )
])

qnt_div = html.Div([
    html.H5('Quantile:'),
    dcc.Slider(
        id='qnt-slider',
        min=0,
        max=95,
        step=5,
        value=50,
        marks=get_marks(0, 100, 5)
    )
])

prd_div = html.Div([
    html.H5('Prediction:'),
    html.Div(id='prediction')
])
