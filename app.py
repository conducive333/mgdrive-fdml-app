import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import layouts
import joblib
import model
import dial
import dash

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
rfm = {
    5  : model.Model("pretrained_models/HLT_WOP_05_RF.joblib"),
    10 : model.Model("pretrained_models/HLT_WOP_10_RF.joblib"),
    25 : model.Model("pretrained_models/HLT_WOP_25_RF.joblib"),
    50 : model.Model("pretrained_models/HLT_WOP_50_RF.joblib")
}

# DO NOT DELETE THIS - this is required for Heroku deployment to succeed
server = app.server

app.layout = html.Div([
    dbc.Col(html.H2('Welcome!')),
    dbc.Col(html.Hr()),
    dbc.Row([
        dbc.Col(
            dbc.Container([
                layouts.mdl_div,
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
    [
        dash.dependencies.Input('mdl-slider', 'value'),
        dash.dependencies.Input('sex-radio' , 'value'),
        dash.dependencies.Input('rsg-input' , 'value'),
        dash.dependencies.Input('rer-slider', 'value'),
        dash.dependencies.Input('ren-slider', 'value'),
        dash.dependencies.Input('qnt-slider', 'value'),
        dash.dependencies.Input('gsv-input' , 'value'),
        dash.dependencies.Input('fic-slider', 'value'),
    ]
)
def update_prediction(mdl, sex, rsg, rer, ren, qnt, gsv, fic):
    return rfm[mdl].predict(sex, rsg, rer, ren, qnt, gsv, fic)

@app.callback(
    dash.dependencies.Output('dial', 'children'),
    [
        dash.dependencies.Input('mdl-slider', 'value'),
        dash.dependencies.Input('sex-radio' , 'value'),
        dash.dependencies.Input('rsg-input' , 'value'),
        dash.dependencies.Input('rer-slider', 'value'),
        dash.dependencies.Input('ren-slider', 'value'),
        dash.dependencies.Input('qnt-slider', 'value'),
        dash.dependencies.Input('gsv-input' , 'value'),
        dash.dependencies.Input('fic-slider', 'value'),
    ]
)
def update_dial(mdl, sex, rsg, rer, ren, qnt, gsv, fic):
    prediction = rfm[mdl].predict(sex, rsg, rer, ren, qnt, gsv, fic)
    return dcc.Graph(figure=dial.create_dial(prediction))

if __name__ == '__main__':
    app.run_server(debug=True)
