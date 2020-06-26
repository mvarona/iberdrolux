import array
import datetime

class Day:

  int num
  float cost
  float consumption
  float[] hourly_consumption

  def __init__(self, num):
    self.num = num

class Month:

  int num
  float cost
  float consumption
  Day[] days

  def __init__(self, num):
    self.num = num

class Year:

  int num
  float cost
  float consumption
  Month[] months
  date offset

  def __init__(self, num, offset):
    self.num = num
    self.offset = offset