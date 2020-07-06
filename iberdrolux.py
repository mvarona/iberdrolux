import array
import datetime
import json
from calendar import monthrange
import sys

# Constants:

MIN_HOUR = 0
MAX_HOUR = 23
MIN_DAY = 1
MAX_DAY = 31
MIN_MONTH = 1
MAX_MONTH = 12
MIN_YEAR = 1900
MAX_YEAR = 2100
MIN_SHOW_DETAILED = 1
DAYS_NORMAL_FEBRUARY = 28
DAYS_NORMAL_YEAR = 365
DAYS_LEAP_FEBRUARY = 29
DAYS_LEAP_YEAR = 366
WH_TO_KWH = 1000
HOURS_IN_DAY = 24

# Classes:

class Day:

  def __init__(self, num):
    self.num = num
    self.cost = 0.00
    self.consumption = 0.00
    self.hourly_consumption = []

class Month:

  def __init__(self, num):
    self.num = num
    self.cost = 0.00
    self.consumption = 0.00
    self.days = []

class Year:

  def __init__(self, num):
    self.num = num
    self.cost = 0.00
    self.consumption = 0.00
    self.months = []

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
  print("de Iberdrola Distribución Eléctrica (i-de.es) **")
  print("* Mario Varona *")
  print("")
  print("Recuerda que el programa calcula una tarifa ad hoc por ejecución,\npor lo que en caso de aplicarse más de una tarifa distinta en la factura anual (por ejemplo, horarios distintos en\ninvierno o en verano), se debe fragmentar el conjunto de datos y aplicar individualmente el cálculo a cada fragmento.\nEs decir, en el caso de una factura anual con distinción estacionaria, se debe usar un conjunto de datos\npara invierno y otro para verano.")
  print("")
  print("Recuerda que las unidades de consumo del conjunto de datos deben estar en W/h.")
  print("")

  firstDay = ensureInputRange("Introduce el primer día del conjunto de datos (1-31): ", MIN_DAY, MAX_DAY)
  firstMonth = ensureInputRange("Introduce el primer mes del conjunto de datos (1-12): ", MIN_MONTH, MAX_MONTH)
  year = ensureInputRange("Introduce el año del conjunto de datos (yyyy): ", MIN_YEAR, MAX_YEAR)
  power = ensureFloat("Introduce la potencia contratada con punto (.) como delimitador de decimales (Ej.: 3.5) (kW/año): ")
  powerPrice = ensureFloat("Introduce el precio en euros por kW/año de potencia contratada, con punto (.) como delimitador de decimales: ")
  normalPrice = ensureFloat("Introduce el precio en euros del kW/h no bonificado, con punto (.) como delimitador de decimales: ")
  discountedPrice = ensureFloat("Introduce el precio en euros del kW/h bonificado, con punto (.) como delimitador de decimales: ")
  beginDiscountHour = ensureInputRangeEmpty("Introduce la hora de comienzo del precio bonificado (0-23, deja en blanco si no hay precio bonificado): ", MIN_HOUR, MAX_HOUR)
  endDiscountHour = ensureInputRangeEmpty("Introduce la hora de fin del precio bonificado (0-23, deja en blanco si no hay precio bonificado): ", MIN_HOUR, MAX_HOUR)
  filename = ensureString("Introduce el nombre del archivo .json donde se encuentra el conjunto de datos: ")
  showDetailed = ensureInputRangeEmpty("Introduce un 1 si quieres que se muestre el cálculo detallado para cada día. Deja en blanco si quieres el cálculo resumido por mes: ", MIN_SHOW_DETAILED, MIN_SHOW_DETAILED)

  if (len(str(showDetailed)) == 0):
    showDetailed = 0

  return firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, filename, showDetailed


def getFile(filename):
  with open(filename) as file:
    data = json.load(file)

  data = data['y']['data'][0]

  return data

def getNumberDaysForYear(year):
  if (getNumberDaysForMonth(2, year) == DAYS_NORMAL_FEBRUARY):
    return DAYS_NORMAL_YEAR
  elif (getNumberDaysForMonth(2, year) == DAYS_LEAP_FEBRUARY):
    return DAYS_LEAP_YEAR


def calculateCostForDay(hourly_consumption, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, year):

  cost = power * powerPrice / getNumberDaysForYear(year)

  hour = 0
  for hour_consumption in hourly_consumption:

    if (len(str(beginDiscountHour)) == 0 and len(str(endDiscountHour)) == 0):
      # There aren't any discount hours:

      cost += normalPrice * float(hour_consumption)

    elif (len(str(beginDiscountHour)) != 0 and len(str(endDiscountHour)) != 0):
      # There are discount hours:

      if (beginDiscountHour < endDiscountHour):
        # Range of discount hours do not overlap with the following day:
        # AND to join both conditions within one day:

        if (hour >= beginDiscountHour and hour <= endDiscountHour):
          cost += discountedPrice * float(hour_consumption)
        else:
          cost += normalPrice * float(hour_consumption)

      else:
        # Range of discount hours overlap with the following day:
        # OR to join both conditions across two days:

        if (hour >= beginDiscountHour or hour <= endDiscountHour):
          cost += discountedPrice * float(hour_consumption)
        else:
          cost += normalPrice * float(hour_consumption)

    else:
      # There is only one discount hour limit, so the other is missing:

      print("Falta uno de los límites de las horas de bonificación")
      sys.exit()

    hour += 1

  return cost


def getNextMonth(month):
  if (month != MAX_MONTH):
    nextMonth = month + 1
  else:
    nextMonth = MIN_MONTH

  return nextMonth


def getNameForMonth(month):
  if (month == 1):
    return "Enero"
  if (month == 2):
    return "Febrero"
  if (month == 3):
    return "Marzo"
  if (month == 4):
    return "Abril"
  if (month == 5):
    return "Mayo"
  if (month == 6):
    return "Junio"
  if (month == 7):
    return "Julio"
  if (month == 8):
    return "Agosto"
  if (month == 9):
    return "Septiembre"
  if (month == 10):
    return "Octubre"
  if (month == 11):
    return "Noviembre"
  if (month == 12):
    return "Diciembre"


def showSummary(power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, filename):
  print("")
  print("* Para los siguientes datos de entrada: *")
  print("Potencia contratada: " + str(power) + " kW/año")
  print("Precio kW/año de potencia contratada: " + str(powerPrice) + " €")
  print("Precio kW/hora consumido durante horas no bonificadas: " + str(normalPrice) + " €")
  print("Precio kW/hora consumido durante horas bonificadas: " + str(discountedPrice) + " €")
  print("Inicio horas bonificadas: " + str(beginDiscountHour) + " h")
  print("Fin horas bonificadas: " + str(endDiscountHour) + " h")
  print("Datos de consumo del archivo: " + filename)
  print("")
  print("* Se ha calculado un consumo estimado de: *")


def showCalc(result, showDetailed):
  for year in result:
    print("")
    print("• AÑO " + str(year.num) + ":")
    print("  - Consumo: " + str(float("{:.3f}".format(year.consumption))) + " kW/hora")
    print("  -   Coste: " + str(float("{:.2f}".format(year.cost))) + " €")

    for month in year.months:
      print("")
      print("    • " + getNameForMonth(month.num) + ":")
      print("      - Consumo: " + str(float("{:.3f}".format(month.consumption))) + " kW/hora")
      print("      -   Coste: " + str(float("{:.2f}".format(month.cost))) + " €")

      if (showDetailed == 1):
        for day in month.days:
          print("")
          print("      • Día " + str(day.num) + ":")
          print("        - Consumo: " + str(float("{:.3f}".format(day.consumption))) + " kW/hora")
          print("        -   Coste: " + str(float("{:.2f}".format(day.cost))) + " €")


# Entry point:

firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, filename, showDetailed = showMenu()

hours = getFile(filename)

if (firstDay > getNumberDaysForMonth(firstMonth, year)):
  print("El día inicial del conjunto de datos no puede ser mayor que el número de días que tiene el mes al que pertenece")
  sys.exit()

numDay = firstDay
numMonth = firstMonth
numYear = year

day = Day(numDay)
month = Month(numMonth)
year = Year(numYear)

result = []

for hour in hours:

  if (hour is None):
    day.hourly_consumption.append(float(0))
  else:
    day.hourly_consumption.append(float(hour['valor']) / WH_TO_KWH)

  if (len(day.hourly_consumption) == HOURS_IN_DAY or hour == hours[-1]):
    day.consumption = sum(day.hourly_consumption)
    day.cost = calculateCostForDay(day.hourly_consumption, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, numYear)

    if (day not in month.days):
      month.days.append(day)

    numDay += 1

    if (numDay > getNumberDaysForMonth(numMonth, numYear) or hour == hours[-1]):
      month_consumption = 0
      month_cost = 0

      for month_day in month.days:
        month_consumption += month_day.consumption
        month_cost += month_day.cost

      month.consumption = month_consumption
      month.cost = month_cost

      if (month not in year.months):
        year.months.append(month)

      year_consumption = 0
      year_cost = 0

      for year_month in year.months:
        year_consumption += year_month.consumption
        year_cost += year_month.cost

      year.consumption = year_consumption
      year.cost = year_cost

      if (year not in result):
        result.append(year)

      numDay = MIN_DAY
      numMonth = getNextMonth(numMonth)
      if (numMonth == MIN_MONTH):
        numYear += 1
        year = Year(numYear)
      month = Month(numMonth)

    day = Day(numDay)

showSummary(power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour, filename)
showCalc(result, showDetailed)