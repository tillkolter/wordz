import datetime
import json
import re
from collections import defaultdict

from flask import Flask, jsonify, request, current_app
from flask_redis import FlaskRedis
from flask_restful import Resource, Api

redis_store = FlaskRedis()
api = Api()


def cache_words(force=False):
    word_dict = redis_store.get('words_loaded')
    if word_dict is None or force:
        word_dict = defaultdict(list)
        print('Loading words from file...')

        start = datetime.datetime.now()

        with open(app.config['MORPHOLOGY_FILE'], 'r') as wordforms_file:
            counter = 0
            for line in wordforms_file.readlines():
                parts = re.split(r'\t+', line.strip())
                word_dict[parts[0]].append(
                    {'stem': parts[1], 'features': parts[2]})
                counter += 1

        for word, morphology in word_dict.items():
            redis_store.set('words:' + word.lower(), json.dumps(morphology))

        end = datetime.datetime.now()
        print("took {} seconds to read {} lines".format((end - start).seconds,
                                                        counter))
    else:
        print("Loading from cache")
        word_dict = json.loads(word_dict.decode('utf-8'))
        print("Loaded from cache")
    return word_dict


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.base.Config')

    print("Init app")
    api.init_app(app)
    print("Init redis cache")
    redis_store.init_app(app)

    print("Register cli")
    register_cli(app)

    return app


def register_cli(app):
    @app.cli.command('init_words')
    def init_words_command():
        cache_words()


class WordInfoList(Resource):
    def get(self):
        term = request.args.get('term', None)
        if term:
            morphology_forms = redis_store.get('words:'+term.lower()) or []
        else:
            morphology_forms = []

        if morphology_forms:
            morphology_forms = json.loads(morphology_forms.decode('utf8'))

        result_dict = {
            term: morphology_forms
        }

        return jsonify(result_dict)


api.add_resource(WordInfoList, '/wordinfo/')

app = create_app()


if __name__ == "__main__":
    app.run(debug=app.debug, host='0.0.0.0')
