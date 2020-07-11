from flask import Flask, render_template, request, jsonify
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

from src.utils import *
from config import *



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():

    open_waste_slot()

    return render_template('insert.html')


@app.route('/waste/pick-type')
def pick_type():
    close_waste_slot()

    return render_template('type.html')

@app.route('/confirmation_pred')
def confirmation_pred():

    return render_template('confirmation.html')

@app.route('/confirmation', methods=['POST'])
def confirmation():
    waste_type = request.form['type']

    process_waste(waste_type)
    return render_template('confirmation.html')


@app.route('/predict')
def prediction():

    #Prise de la photo
    #Lancez les fonctions concernant la prise de photo
    #Sauvegarde de l'image



    # Now there is a trained endpoint that can be used to make a prediction
    prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
    predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)


    with open(base_image_url + "/triof/camera/couvert-plastique.jpg", "rb") as image_contents:
        results = predictor.classify_image(
            project_id, publish_iteration_name, image_contents.read())

        # Display the results.
        resultat = []
        for prediction in results.predictions:
            print("\t" + prediction.tag_name +
                  ": {0:.2f}%".format(prediction.probability * 100))
            resultat.append((str(prediction.tag_name), str(round(prediction.probability * 100, 2))))

    #resultat_json = jsonify({'reponse': resultat})

    #Define variables
    bouteille_name = resultat[0][0]
    bouteille_pred = resultat[0][1]

    gobelet_name = resultat[1][0]
    gobelet_pred = resultat[1][1]

    couverts_name = resultat[2][0]
    couverts_pred = resultat[2][1]

    #Define the context
    context = {

        "bouteille_name" : bouteille_name,
        "bouteille_pred" : bouteille_pred,
        "gobelet_name" : gobelet_name,
        "gobelet_pred" : gobelet_pred,
        "couverts_name" : couverts_name,
        "couverts_pred" : couverts_pred
    }

    return render_template('pred.html', **context)


if __name__ == "__main__":
    app.run(debug=True)