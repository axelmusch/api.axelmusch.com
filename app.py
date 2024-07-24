from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger

from api_functions import api_response
import wordle_solver


app:Flask = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template={
    "info": {
        "title": "api.axelmusch.be",
        "description": "Just some fun things",
        "version": "0.0.1"
    }
})

class UppercaseText(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')

        return jsonify({"text": text.upper()})
    
class GetBestWords(Resource):
    def get(self):
        """
        This method responds to the GET request for returning a list of the best words.
        ---
        tags:
        - Wordle solver
        parameters:
            - name: count
              in: query
              type: integer
              required: false
              description: The number of words to return, Max 50
              default : 15
        responses:
            200:
                description: A successful GET request
                schema:
                    type: object
                    properties:
                        success:
                            type: boolean
                        data:
                            type: object
                            properties:
                                words:
                                    type: array
                                    items:
                                        type: object
                                        properties:
                                            soare:
                                                type: number
                                                description: The word and its score
                                                example: 5.885960110378863
                                        type: object
                                        properties:
                                            carte:
                                                type: number
                                                description: The word and its score
                                                example: 5.794557247295705
            400:
                description: An unsuccessful GET request
                schema:
                    type: object
                    properties:
                        success:
                            type: boolean
                        data:
                            type: object
                            properties:
                                error:
                                    type: string
                                    description: Error
                                    example: count has to be a positive integer between 0 and 50
                                    
        """

        count:int = int(request.args.get('count'))
        if not (count<50 and count>0):
            #return {"success": False, "error":"count has to be a positive integer between 0 and 50"}, 400
            return api_response(False,{"error":"count has to be a positive integer between 0 and 50"},400)

        words:list[dict] = wordle_solver.get_best_words(count)
        #return {"success": True, "data":{"words":words}}, 200
        return api_response(True,{"words":words},200)


#api.add_resource(UppercaseText, "/uppercase")
api.add_resource(GetBestWords, "/wordle-solver/bestwords")

if __name__ == "__main__":
    app.run(debug=True)