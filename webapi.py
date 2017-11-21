from flask import Flask
from flask_restplus import Api
from flask_restplus import fields
from flask_restplus import Resource
from sklearn.externals import joblib
from pandas import DataFrame

app = Flask(__name__)

api = Api(
   app,
   version='1.0',
   title='Restaurant Rating API',
   description='Prediction API for Restaurant ratings')

ns = api.namespace('restaurant',
   description='Restaurant Operations')

mappers = joblib.load('mapping.dat')
model = joblib.load('model.dat')

parser = api.parser()
for key, mapper in mappers.items():
   parser.add_argument(key,
                       required=True,
                       help='Allowed values: ' + ', '.join(mapper.classes_),
                       choices=list(mapper.classes_),
                       location='form')

response_model = api.model('Response', { 'result': fields.String})


@ns.route('/')
class RestaurantApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(api.model('Response', { 'result': fields.String}))
    def post(self):
       args = parser.parse_args()
       values = {}
       for key, mapper in mappers.items():
          values[key] = mapper.transform([args[key]])[0]
       df = DataFrame([values]);
       result = model.predict(df)[0]
       return { 'result': result }

@api.errorhandler(Exception)
def handle_exception(error):
    app.logger.error('Server Error: %s', (error))
    '''Return a custom message and 500 status code'''
    return {'message': 'Unspecified error occured. See log for details.'}

if __name__ == '__main__':
    app.run(debug=True)
