import joblib

class Model:

    def __init__(self, path_to_model):
        self.model = joblib.load(path_to_model)

    def _sex_translate(self, sex_value):
        if sex_value == "Male":
            return [True, False, False]
        if sex_value == "Gravid Female":
            return [False, True, False]
        if sex_value == "Non Gravid Female":
            return [False, False, True]
        return [False, False, False]

    def _label_translate(self, class_name):
        if class_name == 1:
            return "Low"
        if class_name == 2:
            return "Mid"
        if class_name == 3:
            return "High"
        if class_name == 4:
            return "Permanent"
        return "None"

    def predict(self, inputs):
        sexes = self._sex_translate(inputs['sex'])
        in_probe = [
            [
                sexes[0], 
                sexes[1], 
                sexes[2],
                inputs['rsg'], 
                inputs['rer'],
                inputs['ren'],
                inputs['qnt'],
                inputs['gsv'],
                inputs['fic']
            ]
        ]
        class_name = self._label_translate(self.model.predict(in_probe))
        proba_list = self.model.predict_log_proba(in_probe).tolist()
        return class_name, proba_list