import plotly.graph_objects as go
import numpy as np

base_chart = {
    "values": [40, 10, 10, 10, 10],
    "labels": [" ", " ", " ", " ", " ", " "],
    "domain": {"x": [0, .9]},
    "marker": {
        "colors": [
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
            'rgb(255, 255, 255)',
        ],
        "line": {
            "width": 0
        }
    },
    "name": "Gauge",
    "hole": .4,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 90,
    "showlegend": False,
    "hoverinfo": "none",
    "textinfo": "label",
    "textposition": "outside"
}

meter_chart = {
    "values": [40, 10, 10, 10, 10, 10],
    "labels": [' ', 'NONE', 'LOW', 'MID', 'HIGH', 'PERMANENT'],
    "marker": {
        'colors': [
            'rgb(255, 255, 255)',
            'rgb(245,252,255)',
            'rgb(219,243,250)',
            'rgb(183,233,247)',
            'rgb(146,223,243)',
            'rgb(122,215,240)'
        ]
    },
    "domain": {"x": [0, 0.9]},
    "name": "Gauge",
    "hole": .3,
    "type": "pie",
    "direction": "clockwise",
    "rotation": 100,
    "showlegend": False,
    "textinfo": "label",
    "textposition": "inside",
    "hoverinfo": "none",
}

def rotate_coord(coord, degrees):
    radians = np.radians([degrees])[0]
    return np.array([
        [np.cos(radians), -np.sin(radians)],
        [np.sin(radians),  np.cos(radians)]
    ]) @ np.array(coord)

def rotate_coords(coords, degrees, origin=(0.45, 0.5)):
    points = []
    origin = np.array(origin)
    for coord in map(np.array, coords):
        coord = coord - origin
        coord = rotate_coord(coord, degrees)
        coord = coord + origin
        points.append(tuple(coord))
    return points

def create_path(coords):
    path = "M 0.445 0.5 L {} L 0.455 0.5 Z"
    coords = [" ".join(map(str, c)) for c in coords]
    return path.format(coords[1])

def get_path(prediction):
    mid_coords = [(0.445, 0.5), (0.45, 0.65), (0.455, 0.5)]
    if prediction == "LOW":
        return create_path(rotate_coords(mid_coords, 25))
    if prediction == "MID":
        return create_path(rotate_coords(mid_coords, 0))
    if prediction == "HIGH":
        return create_path(rotate_coords(mid_coords, -25))
    if prediction == "PERMANENT":
        return create_path(rotate_coords(mid_coords, -90))
    return create_path(rotate_coords(mid_coords, 90))

def point_to(prediction):
    return {
        'shapes': [
            {
                'type': 'path',
                'path': get_path(prediction),
                'fillcolor': 'rgba(28,104,192, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ]
    }

def create_dial(prediction):
    return go.Figure([base_chart, meter_chart], layout=point_to(prediction))