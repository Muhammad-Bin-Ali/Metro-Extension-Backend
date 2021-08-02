from flask import Flask
from flask_restful import Api, Resource, reqparse
from abstract_ML_extract import get_summary
from parse_article import parse
from flask_cors import CORS

#instantiating App
app = Flask(__name__)
CORS(app)
api = Api(app)

#validating arguments sent in form
request_args = reqparse.RequestParser()
request_args.add_argument("url", type = str, help = "Did not work")

#Resource that deals with requests
class Summarize(Resource):
    def post(self):
        args = request_args.parse_args() #stow
        url = args["url"]
        article = parse(url)
        summary = get_summary(article) 
        return {"summary": summary}

#Adding resource to API
api.add_resource(Summarize, "/summarize-article")

#run app when this file is being run
if __name__ == "__main__":
    app.run(debug=True)