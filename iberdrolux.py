import array
import datetime

class Day:

  def __init__(self, num):
    self.num = num
    self.cost = None
    self.consumption = None
    self.hourly_consumption = None

class Month:

  def __init__(self, num):
    self.num = num
    self.cost = None
    self.consumption = None
    self.days = None

class Year:

  def __init__(self, num, offset):
    self.num = num
    self.offset = offset
    self.cost = None
    self.consumption = None
    self.months = None
    self.offset = None


def ensureInputRange(msg, min, max):
  userInput = int(input(msg))
  while userInput > max or userInput < min:
    userInput = int(input(msg))

  return userInput

def ensureInputRangeEmpty(msg, min, max):
  userInput = input(msg)
  if (len(str(userInput)) == 0):
    return
  else:
    userInput = int(userInput)

  while userInput > max or userInput < min:
    userInput = input(msg)
    if (len(str(userInput)) == 0):
      return
    else:
      userInput = int(userInput)

  return userInput

def ensureFloat(msg):
  userInput = float(input(msg))
  return userInput

def showMenu():
  print("*** Bienvenido a Iberdrolux ***")
  print("** Calculador de precios para tarifas eléctricas")
  print("usando datos de consumos horarios anteriores obtenidos")
  print("de Iberdrola Distribuidora (i-de.es) **")
  print("* Mario Varona *")
  print("")
  print("Recuerde que el programa calcula una tarifa ad-hoc por ejecución, por lo que en caso de aplicarse más de una tarifa distinta en la factura anual (por ejemplo, horarios distintos en invierno o en verano), se debe fragmentar el conjunto de datos y aplicar individualmente el cálculo a cada fragmento. Es decir, en el caso de una factura anual con distinción estacionaria, se debería usar un conjunto de datos para invierno y otro para verano.")
  print("")

  firstDay = ensureInputRange("Introduzca el primer día del conjunto de datos (1-31): ", 1, 31)
  firstMonth = ensureInputRange("Introduzca el primer mes del conjunto de datos (1-12): ", 1, 12)
  year = ensureInputRange("Introduzca el año del conjunto de datos (yyyy): ", 1900, 2100)
  power = ensureFloat("Introduzca la potencia contratada con punto (.) como delimitador de decimales (Ej.: 3.5) (kW/h): ")
  powerPrice = ensureFloat("Introduzca el precio por kW de potencia contratada, con punto (.) como delimitador de decimales: ")
  normalPrice = ensureFloat("Introduzca el precio del kW/h no bonificado, con punto (.) como delimitador de decimales: ")
  discountedPrice = ensureFloat("Introduzca el precio del kW/h bonificado, con punto (.) como delimitador de decimales: ")
  beginDiscountHour = ensureInputRangeEmpty("Introduzca la hora de comienzo del precio bonificado (0-24, deje en blanco si no hay precio bonificado): ", 0, 24)
  endDiscountHour = ensureInputRangeEmpty("Introduzca la hora de fin del precio bonificado (0-24, deje en blanco si no hay precio bonificado): ", 0, 24)

  return firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour


# Entry point:

firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour = showMenu()
