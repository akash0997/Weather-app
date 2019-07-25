from flask import Flask, render_template
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from ezw_restful_controller import EZWRController
app = Flask(__name__, static_folder="build/static", template_folder="build")
api = Api(app)
CORS(app)

@app.route("/")
def hello():
    return render_template('index.html')
app.debug=True
 
class Ezw_API(Resource):
    def post(self):
        json_data = request.get_json()
        latitude = json_data['latitude']
        longitude = json_data['longitude']
        start_date = json_data['start_date']
        end_date = json_data['end_date']
        print(json_data)
        ezw = EZWRController()
        ezw_reports = ezw.getWeatherReports(start_date, end_date, latitude, 
                                        longitude)
        return {'reports': ezw_reports}

api.add_resource(Ezw_API, '/ezw_api')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)

