import colorama as color
import settings
import urllib2

color.init()

class DataHolder:
  def __init__(self, value=None, attr_name='value'):
      self._attr_name = attr_name
      self.set(value)
  def __call__(self, value):
      return self.set(value)
  def set(self, value):
      setattr(self, self._attr_name, value)
      return value
  def get(self):
      return getattr(self, self._attr_name)

class BotLog:
  def __init__(self, message, id):
    print color.Fore.BLUE + color.Style.BRIGHT + "[" + settings.bots[id]["name"] + "] " + color.Fore.RESET + color.Style.RESET_ALL + message