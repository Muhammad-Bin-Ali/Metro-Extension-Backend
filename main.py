from flask import Flask
from flask_restful import Api, Resource, reqparse
from abstract_ML_extract import get_summary
from parse_article import parse
from flask_cors import CORS
from basic_operations import createUser, addLink, getAll, delLink, checkIfExist, getSaved

#instantiating App
app = Flask(__name__)
CORS(app)
api = Api(app)

#validating arguments sent in form
request_args = reqparse.RequestParser()
request_args.add_argument("url", type = str)
request_args.add_argument("body", type = str)
request_args.add_argument("title", type = str)
request_args.add_argument("email", type = str)
request_args.add_argument("save_link", type = str)
request_args.add_argument("del_link", type = str)
request_args.add_argument('get_saved_link', type = str)

#Resource that deals with requests
class Main(Resource):
    def post(self, user_id):
        args = request_args.parse_args() 

        if args['url']:
            url = args["url"]
            article = parse(url)
            summary = get_summary(article)
            exists = checkIfExist(user_id, url) 
            if summary:
                return {"summary": summary, "exists": exists}, 200
            else: 
                return False, 409
        
        if args['get_saved_link']:
            title = args['title']
            body = getSaved(user_id, title)
            if body:
                return {"body": body}, 200
            else:
                return False, 404

        if user_id:
            createUser(user_id, args["email"])
            return True, 201

    def put(self, user_id):
        args = request_args.parse_args()

        if args['save_link']:
            title = args['title']
            body = args['body']
            link = args['url']
          
            result = addLink(user_id, link, title, body)
            if result:
                return True, 201
            else: 
                return False, 409

    def get(self, user_id):
        if user_id:
            links = getAll(user_id)
            if links:
                return {"links": links}, 200
            else: 
                return False, 404

    def delete(self, user_id):
        args = request_args.parse_args()

        if args['del_link']:
            title = args['title']
            body = args['body']


            result = delLink(user_id, title, body)
            if result:
                return True, 201
            else: 
                return False, 409   

#Adding resource to API
api.add_resource(Main, "/summarize-article/<string:user_id>")

#run app when this file is being run
if __name__ == "__main__":
    app.run(debug=True)