"""
This file contains helper function
"""

import time
import math


def get_local_utc_offset():
  """
  This function calculates the UTC offset for the
  local timezone and converts it in to string
  """
  # Get the utc_offset in seconds and convert in hours
  utc_offset = time.localtime().tm_gmtoff/(60*60)

  # The UTC_OFFSET can be in fraction, create tuple of fraction and int
  integer_fraction_tuple = math.modf(utc_offset)

  # Check if tuple is not greater than o means its an int offset
  if not integer_fraction_tuple[0] > 0:

      # Safely stores in int
      utc_offset = int(integer_fraction_tuple[1])

  str_utc_offset = ''

  # Check if the offset is in - or +
  # For + offsets need to add + sign with it also
  if utc_offset > -1:
      str_utc_offset = '+{utc_offset}'.format(utc_offset=utc_offset)
  else:
      str_utc_offset = '{utc_offset}'.format(utc_offset=utc_offset)
  return str_utc_offset