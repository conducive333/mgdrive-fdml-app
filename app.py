import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import layouts
import joblib
import dial
import dash

model = joblib.load("pretrained_models/HLT_WOP_50_RF.joblib")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div(
    [
        dbc.Col(html.H2('Welcome!')),
        dbc.Col(html.Hr()),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Container(
                        [
                            layouts.rer_div,
                            layouts.fic_div,
                            layouts.ren_div,
                            layouts.qnt_div,
                            dbc.Row(
                                [                            
                                    dbc.Col(layouts.sex_div),
                                    dbc.Col(layouts.gsv_div),
                                    dbc.Col(layouts.rsg_div),
                                    dbc.Col(layouts.prd_div)
                                ], justify='between'
                            )
                        ]
                    )
                ),
                dbc.Col(
                    dbc.Container(
                        [
                            html.Div(html.H5("Prediction Dial:")),
                            html.Div(id='dial')
                        ]
                    )
                )
            ]
        ),
    ]
)

def sex_translate(sex):
    if sex == "Male":
        return [True, False, False]
    if sex == "Gravid Female":
        return [False, True, False]
    if sex == "Non Gravid Female":
        return [False, False, True]
    return [False] * 3

def label_translate(prediction):
    prediction = prediction[0]
    if prediction == 0: return "NONE"
    if prediction == 1: return "LOW"
    if prediction == 2: return "MID"
    if prediction == 3: return "HIGH"
    if prediction == 4: return "PERMANENT"
    raise ValueError("Invalid prediction encountered: {}".format(prediction))

@app.callback(
    dash.dependencies.Output('prediction', 'children'),
    [
        dash.dependencies.Input('sex-radio' , 'value'),
        dash.dependencies.Input('gsv-input' , 'value'),
        dash.dependencies.Input('rsg-input' , 'value'),
        dash.dependencies.Input('rer-slider', 'value'),
        dash.dependencies.Input('fic-slider', 'value'),
        dash.dependencies.Input('ren-slider', 'value'),
        dash.dependencies.Input('qnt-slider', 'value'),
    ]
)
def update_prediction(sex, gsv, rsg, rer, fic, ren, qnt):
    sexes = sex_translate(sex)
    in_probe = [
        [
            sexes[0], 
            sexes[1], 
            sexes[2], 
            float(rsg), 
            float(rer),
            int(ren),
            int(qnt),
            float(gsv), 
            float(fic)
        ]
    ]
    return label_translate(model.predict(in_probe))

@app.callback(
    dash.dependencies.Output('dial', 'children'),
    [
        dash.dependencies.Input('sex-radio' , 'value'),
        dash.dependencies.Input('gsv-input' , 'value'),
        dash.dependencies.Input('rsg-input' , 'value'),
        dash.dependencies.Input('rer-slider', 'value'),
        dash.dependencies.Input('fic-slider', 'value'),
        dash.dependencies.Input('ren-slider', 'value'),
        dash.dependencies.Input('qnt-slider', 'value'),
    ]
)
def update_dial(sex, gsv, rsg, rer, fic, ren, qnt):
    sexes = sex_translate(sex)
    in_probe = [
        [
            sexes[0], 
            sexes[1], 
            sexes[2], 
            float(rsg), 
            float(rer),
            int(ren),
            int(qnt),
            float(gsv), 
            float(fic)
        ]
    ]
    prediction = label_translate(model.predict(in_probe))
    return dcc.Graph(figure=dial.create_dial(prediction))

if __name__ == '__main__':
    app.run_server(debug=True)