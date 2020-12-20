import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import layouts
import model
import dial
import dash
import os
import re

MODELS = 'pretrained_models'
def get_kv_pair(model_name):
    key = int(re.search(r'[0-9]+', model_name)[0])
    val = model.Model(os.path.join(MODELS, model_name))
    return key, val

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
rfm = dict(get_kv_pair(model_name) for model_name in os.listdir(MODELS))

# DO NOT DELETE THIS - this is required for Heroku deployment to succeed
server = app.server

app.layout = html.Div([
    dbc.Col(html.H2('Welcome!')),
    dbc.Col(html.Hr()),
    dbc.Row([
        dbc.Col(
            dbc.Container([
                layouts.mdl_div(rfm.keys()),
                layouts.rer_div,
                layouts.fic_div,
                layouts.ren_div,
                layouts.qnt_div,
                dbc.Row([                            
                    dbc.Col(layouts.sex_div),
                    dbc.Col(layouts.gsv_div),
                    dbc.Col(layouts.rsg_div),
                    dbc.Col(layouts.prd_div)
                ], justify='between')
            ])
        ),
        dbc.Col(
            dbc.Container([
                html.Div(html.H5("Prediction Dial:")),
                html.Div(id='dial')
            ])
        )
    ])
])

@app.callback(
    dash.dependencies.Output('prediction', 'children'),
    dash.dependencies.Output('dial', 'children'),    
    dash.dependencies.Input('mdl-slider', 'value'),
    dash.dependencies.Input('sex-radio' , 'value'),
    dash.dependencies.Input('rsg-input' , 'value'),
    dash.dependencies.Input('rer-slider', 'value'),
    dash.dependencies.Input('ren-slider', 'value'),
    dash.dependencies.Input('qnt-slider', 'value'),
    dash.dependencies.Input('gsv-input' , 'value'),
    dash.dependencies.Input('fic-slider', 'value')
)
def update_prediction(mdl, sex, rsg, rer, ren, qnt, gsv, fic):
    prediction = rfm[mdl].predict(sex, rsg, rer, ren, qnt, gsv, fic)
    return prediction, dcc.Graph(figure=dial.create_dial(prediction))

if __name__ == '__main__':
    app.run_server(debug=True)
