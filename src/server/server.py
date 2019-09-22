from flask import Flask
server = Flask(__name__)

if __name__ == '__main__':
  server.run(debug=True)

@server.route('/power', methods=['POST'])
def power():
  print('hit power api. switching:')
  return 'power'

@server.route('/schedule', methods=['POST'])
def schedule():
  print('schedule api hit')
  return 'schedule'

@server.route('/hold', methods=['POST'])
def hold(): 
  print('hold request hit:')
  return 'hold'
