import joblib

class Model:

    def __init__(self, path_to_model):
        self.model = joblib.load(path_to_model)

    def _sex_translate(self, sex):
        if sex == "Male":
            return [True, False, False]
        if sex == "Gravid Female":
            return [False, True, False]
        if sex == "Non Gravid Female":
            return [False, False, True]
        return [False] * 3

    def _label_translate(self, prediction):
        prediction = prediction[0]
        if prediction == 0: return "NONE"
        if prediction == 1: return "LOW"
        if prediction == 2: return "MID"
        if prediction == 3: return "HIGH"
        if prediction == 4: return "PERMANENT"
        raise ValueError("Invalid prediction encountered: {}".format(prediction))

    def predict(self, sex, rsg, rer, ren, qnt, gsv, fic):
        sexes = self._sex_translate(sex)
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
        return self._label_translate(self.model.predict(in_probe))
