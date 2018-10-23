import json
import numpy as np
import utils as _utils
from flask import Flask, request, Response, render_template

app = Flask(__name__)


def get_features() -> np.array:
    """
    Extract a specific field from a post request form
    :param form_field:
    :return: the value in the form field
    """
    features = [float(request.form.get(f)) for f in
                _utils.CLASS_FEATURES]
    return np.array(features).reshape(1, -1)


def format_prediction(pred: int) -> str:
    """
    Format the prediction output to a corresponding phrase
    :param pred: prediction output
    :return: json formatted app output
    """
    map = {
        0: 'Not Likely',
        1: 'Likely'
    }
    return json.dumps(
        {"Survival": map[pred]}
    )


@app.route('/', methods=['GET'])
def index(name=None):
    """
    Main landing page
    :param name:
    :return:
    """
    return render_template('titanic.html', name=name)


@app.route('/titanic', methods=['POST'])
def predict_survival() -> Response:
    """
    Perform survival prediction based off form input
    :return: flask response with prediction output and status code 200
    """
    clf = _utils.load_model(_utils.MODEL_LOC,
                            _utils.MODEL_NAME
                            )
    prediction = clf.predict(get_features())[0]
    return Response(
        format_prediction(prediction),
        200
    )


if __name__ == '__main__':
    app.run(debug=False)
