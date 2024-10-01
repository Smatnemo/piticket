from datetime import datetime
from piticket.smartcard import is_date_valid, is_card_valid



# Procedure for the duration of the use of the card
# Read the start date from the card
# Read the end date from the card
# If today is greater than the start date but less than the end date:
# return True
# otherwise
# False
# Test cases (date within a month)
# NOTE: date is datetime.now()
# 1. A date between start date and end date. Expected True
test_1 = {'input':{'start_date':datetime.strptime('20240901000000','%Y%m%d%H%M%S'), 
                    'end_date':datetime.strptime('20241001125959','%Y%m%d%H%M%S')},
          'output': True
          }
# 2. A date outside start date and end date. Expected False
test_2 = {'input':{'start_date':datetime.strptime('20240918185010','%Y%m%d%H%M%S'), 
            'end_date':datetime.strptime('20241018235959','%Y%m%d%H%M%S')},
          'output': False
          }
# 3. A date same as start date after the time written on the card. Expected True
test_3 = {'input':{'start_date':datetime.strptime('20240917125010','%Y%m%d%H%M%S'), 
                    'end_date':datetime.strptime('20241017235959','%Y%m%d%H%M%S')},
          'output': True
          }
# 4. A date same as start date before the time written on the card. Expected False
test_4 = {'input':{'start_date':datetime.strptime('20240917185010','%Y%m%d%H%M%S'), 
                   'end_date':datetime.strptime('20241017235959','%Y%m%d%H%M%S')},
          'output': False
          }
# 5. A date same as end date before 23:59:59 pm. Expected True
test_5 = {'input':{'start_date':datetime.strptime('20240817185010','%Y%m%d%H%M%S'), 
                    'end_date':datetime.strptime('20240917235959','%Y%m%d%H%M%S')},
          'output': True
          }
# 6. A date between a start date in one year and an end date in the next year.
#   .The date should also be in next year. Expected True
# Modify and change date from date.now() to valid date datetime.strptime('')
test_6 = {'input':{'start_date':datetime.strptime('20241217185010','%Y%m%d%H%M%S'), 
                    'end_date':datetime.strptime('20250117235959','%Y%m%d%H%M%S'),
                    'current_date':datetime.strptime('20250107235959','%Y%m%d%H%M%S')},
          'output': True
          }
# 7. A date between a start date in one year and an end date in the next year.
#   The date should also be in current year. Expected True
# Modify and change date from date.now() to valid date datetime.strptime('')
test_7 = {'input':{'start_date':datetime.strptime('20241217185010','%Y%m%d%H%M%S'), 
                    'end_date':datetime.strptime('20250117235959','%Y%m%d%H%M%S'),
                    'current_date':datetime.strptime('20241231235959','%Y%m%d%H%M%S')},
          'output': True
          }
# 8. A date after the end date in the next year.
#   The date should also be in the next year. Expected False
# Modify and change date from date.now() to valid date datetime.strptime('')
test_8 = {'input':{'start_date':datetime.strptime('20241217185010','%Y%m%d%H%M%S'), 
                    'end_date':datetime.strptime('20250117235959','%Y%m%d%H%M%S'),
                    'current_date':datetime.strptime('20250118235959','%Y%m%d%H%M%S')},
          'output': False
          }
# Test with date within a year

# Test with date within a week
test_cases = [test_1, test_2, test_3, test_4, test_5, test_6, test_7, test_8]


def test_is_date_valid():
    all(is_date_valid(**test_case['input'])==test_case['output'] for test_case in test_cases)

def test_is_card_valid():
    pass