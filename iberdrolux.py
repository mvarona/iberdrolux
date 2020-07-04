import array
import datetime
import json
from calendar import monthrange

# Constants:

MIN_HOUR = 0
MAX_HOUR = 24
MIN_DAY = 1
MAX_DAY = 31
MIN_MONTH = 1
MAX_MONTH = 12
MIN_YEAR = 1900
MAX_YEAR = 2100

# Classes:

class Day:

  def __init__(self, num):
    self.num = num
    self.cost = 0.00
    self.consumption = 0.00
    self.hourly_consumption = None

class Month:

  def __init__(self, num):
    self.num = num
    self.cost = 0.00
    self.consumption = 0.00
    self.days = None

class Year:

  def __init__(self, num):
    self.num = num
    self.offset = offset
    self.cost = 0.00
    self.consumption = 0.00
    self.months = None

# Functions:

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


def ensureString(msg):
  userInput = str(input(msg))
  return userInput


def getNumberDaysForMonth(month, year):
  num = monthrange(year, month)
  return num[1]


def showMenu():
  print("*** Bienvenido a Iberdrolux ***")
  print("** Calculador de precios para tarifas eléctricas")
  print("usando datos de consumos horarios anteriores obtenidos")
  print("de Iberdrola Distribuidora (i-de.es) **")
  print("* Mario Varona *")
  print("")
  print("Recuerde que el programa calcula una tarifa ad-hoc por ejecución, por lo que en caso de aplicarse más de una tarifa distinta en la factura anual (por ejemplo, horarios distintos en invierno o en verano), se debe fragmentar el conjunto de datos y aplicar individualmente el cálculo a cada fragmento. Es decir, en el caso de una factura anual con distinción estacionaria, se debería usar un conjunto de datos para invierno y otro para verano.")
  print("")

  firstDay = ensureInputRange("Introduzca el primer día del conjunto de datos (1-31): ", MIN_DAY, MAX_DAY)
  firstMonth = ensureInputRange("Introduzca el primer mes del conjunto de datos (1-12): ", MIN_MONTH, MAX_MONTH)
  year = ensureInputRange("Introduzca el año del conjunto de datos (yyyy): ", MIN_YEAR, MAX_YEAR)
  power = ensureFloat("Introduzca la potencia contratada con punto (.) como delimitador de decimales (Ej.: 3.5) (kW/año): ")
  powerPrice = ensureFloat("Introduzca el precio en euros por kW/año de potencia contratada, con punto (.) como delimitador de decimales: ")
  normalPrice = ensureFloat("Introduzca el precio en euros del kW/h no bonificado, con punto (.) como delimitador de decimales: ")
  discountedPrice = ensureFloat("Introduzca el precio en euros del kW/h bonificado, con punto (.) como delimitador de decimales: ")
  beginDiscountHour = ensureInputRangeEmpty("Introduzca la hora de comienzo del precio bonificado (0-24, deje en blanco si no hay precio bonificado): ", MIN_HOUR, MAX_HOUR)
  endDiscountHour = ensureInputRangeEmpty("Introduzca la hora de fin del precio bonificado (0-24, deje en blanco si no hay precio bonificado): ", MIN_HOUR, MAX_HOUR)
  filename = ensureString("Introduzca el nombre del archivo .json donde se encuentra el conjunto de datos: ")

  return firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, filename


def getFile(filename):
  with open(filename) as file:
    data = json.load(file)

  data = data['y']['data'][0]

  return data


def calculateCostForDay(hourly_consumption, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour):

  

  return cost


def getNextMonth(month):
  if (month != MAX_MONTH):
    nextMonth = month + 1
  else:
    nextMonth = MIN_MONTH

  return nextMonth


# Entry point:

#firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, filename = showMenu()

filename = "test_2017.json"
hours = getFile(filename)

if (firstDay > getNumberDaysForMonth(firstMonth, year)):
  print("El día inicial del conjunto de datos no puede ser mayor que el número de días que tiene el mes al que pertenece")
  return

numDay = firstDay
numMonth = firstMonth
numYear = year

day = Day(numDay)
month = Month(numMonth)
year = Year(numYear)

for hour in hours:

  day.hourly_consumption.append(hour['valor'])

  if (len(day.hourly_consumption) == MAX_HOUR or hour == hours[-1]):
    day.consumption = sum(day.hourly_consumption)
    day.cost = calculateCostForDay(day.hourly_consumption, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour)

    month.days.append(day)
    numDay += 1

    if (numDay == getNumberDaysForMonth(numMonth, numYear)):
      year.months.append(month)
      numDay = MIN_DAY
      numMonth = getNextMonth(numMonth)
      if (numMonth == MIN_MONTH):
        numYear += 1
        year = Year(numYear)
      month = Month(numMonth)

    day = Day(numDay)