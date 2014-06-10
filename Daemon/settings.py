bots = [3]
steam = {
  'guard': {
    'interval': 5,
    'retries': 3
  },
  'trade': {
    'incorrectHandler': 'declineOffer'
  },
  'api': "Enter your api key here"
}
database = 'postgresql://user:password@localhost:port/Database'