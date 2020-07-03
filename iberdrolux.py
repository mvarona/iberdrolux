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


def showMenu():
  print("*** Bienvenido a Iberdrolux ***")
  print("** Calculador de precios para tarifas eléctricas")
  print("usando datos de consumos horarios anteriores obtenidos")
  print("de Iberdrola Distribuidora (i-de.es) **")
  print("* Mario Varona *")
  print("")
  print("Recuerde que el programa calcula una tarifa ad-hoc por ejecución, por lo que en caso de aplicarse más de una tarifa distinta en la factura anual (por ejemplo, horarios distintos en invierno o en verano), se debe fragmentar el conjunto de datos y aplicar individualmente el cálculo a cada fragmento. Es decir, en el caso de una factura anual con distinción estacionaria, se debería usar un conjunto de datos para invierno y otro para verano.")
  print("")

  firstDay = input("Introduzca el primer día del conjunto de datos (0-31): ")
  firstMonth = input("Introduzca el primer mes del conjunto de datos (1-12): ")
  year = input("Introduzca el año del conjunto de datos (yyyy): ")
  power = input("Introduzca la potencia contratada (kW/h): ")
  powerPrice = input("Introduzca el precio por kW (potencia): ")
  normalPrice = input("Introduzca el precio del kW/h no bonificado: ")
  discountedPrice = input("Introduzca el precio del kW/h bonificado: ")
  beginDiscountHour = input("Introduzca la hora de comienzo del precio bonificado (0-24, deje en blanco si no hay precio bonificado): ")
  endDiscountHour = input("Introduzca la hora de fin del precio bonificado (0-24, deje en blanco si no hay precio bonificado): ")

  return firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour


# Entry point:

firstDay, firstMonth, year, power, powerPrice, normalPrice, discountedPrice, beginDiscountHour, endDiscountHour = showMenu()
