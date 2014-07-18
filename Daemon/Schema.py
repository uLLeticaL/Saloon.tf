import colorama as color, database as db
from SteamBot import Handler

class OCommunicate(object):
  def log(self, handler, name, message):
    print color.Fore.YELLOW + color.Style.BRIGHT + "[" + handler + "] " + color.Fore.GREEN + "[" + name + "] " + color.Fore.RESET + color.Style.RESET_ALL + message

Communicate = OCommunicate()

RBot = db.Session.query(db.Bots).first()
Handler(RBot, Communicate).Schema.update()