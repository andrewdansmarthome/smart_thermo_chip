from flask import Flask
app = Flask(__name__)

@app.route('/schedule', methods=['POST'])
def schedule()
  print('schedule api hit', request)
  return 'schedule'
