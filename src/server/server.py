from flask import Flask
app = Flask(__name__)

@app.route('/power', methods=['POST'])
def power()
  print('hit power api. switching:', request)
  return 'power'

@app.route('/schedule', methods=['POST'])
def schedule()
  print('schedule api hit', request)
  return 'schedule'

@app.route('/hold', methods=['POST'])
def hold()
  print('hold request hit:', request)
  return 'hold'

