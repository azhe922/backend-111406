import os
import logging
import logging.config
import yaml
from initapp import create_app

app = create_app(os.getenv('flask_config') or 'default')

with open(file="./logconfig.yaml", mode='r', encoding="utf-8") as file:
    logging_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
    logging.config.dictConfig(config=logging_yaml)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
if __name__ == '__main__':
    app.run(threaded=True)