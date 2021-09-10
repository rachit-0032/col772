# !/usr/bin/python
# -*- coding: utf-8 -*-

# Rachit Jain | 2018ME10032 | COL772 | A1 | Prof. Mausam | Deadline: 11th September 2021
# Creating a rule-based model used to convert written speech to spoken text


## Importing necessary libraries
import json
import re
import argparse


# ------------------------------------
# Reading Command Line Inputs (CLI)
# ------------------------------------

def read_cli():

    ## Argument Parser.
    parser = argparse.ArgumentParser(description='Code Run.')
    
    ## Input File.
    parser.add_argument(
        '--input_path',
        help='Input File Path', 
        required=True, type=str, default='input.json'
    )

    ## Solution File.
    parser.add_argument(
        '--solution_path', 
        help='Solution File Path',
        required=True, type=str, default='solution.json'
    )

    args = parser.parse_args()

    return args


# ------------------------------------
# Defining some Dictionaries
# ------------------------------------

## Dictionary of roman numerals.
roman_numerals = {
    'I': '1',
    'II': '2',
    'III': '3',
    'IV': '4',
    'V': '5',
    'VI': '6',
    'VII': '7',
    'VIII': '8',
    'IX': '9',
    'X': '10',
    'XI': '11',
    'XII': '12',
    'XIII': '12',
    'XIV': '12',
    'XV': '12',
    'XVI': '12',
    'XVII': '12',
    'XVIII': '12',
    'XIX': '12',
    'XX': '12',
    'XXI': '12',
    'XXII': '12', 
    }


## Dictionary of common abbreviations.
full_form = {
    # Length
    'm': 'meter', 
    'mm': 'millimeter',
    'cm': 'centimeter',
    'km': 'kilometer',
    'mi': 'mile',

    # Speed
    'kmph': 'kilometers per hour',
    'mph': 'miles per hour',

    # Weight
    'g': 'gram',
    'kg': 'kilogram',
    'mg': 'milligram',

    # Area
    'm2': 'square meters',
    'm²': 'square meters',
    'mm2': 'square millimeters',
    'mm²': 'square millimeters',
    'cm2': 'square centimeters',
    'cm²': 'square centimeters',
    'km2': 'square kilometers',
    'km²': 'square kilometers',
    'mi2': 'square miles',
    'mi²': 'square miles',
    'sq': 'squares',
    'sqm': 'square meter',
    'sqcm': 'square centimeter',
    'sqkm': 'square kilometer',
    'sqmi': 'square mile',
    'ha': 'hectare',
    'ac': 'acre',

    # Volume
    'm3': 'cubic meter',
    'mm3': 'cubic millimeter',
    'cm3': 'cubic centimeter',
    'km3': 'cubic kilometer',
    'cc': 'cubic centimeter',

    # Time
    's': 'second',
    'min': 'minute',
    'rpm': 'revolutions per minute',

    # Timing
    'a.m.': 'a m',
    'p.m.': 'p m',
    'am': 'a m',
    'pm': 'p m',
    'AM': 'a m',
    'PM': 'p m',

    # Currency
    'M': 'million',
    'mn': 'million',
    'Mn': 'million',
    'B': 'billion',
    'b': 'billion',
    'bn': 'billion',
    'Bn': 'billion',
    'cr': 'crore',

    # Storage
    'KB': 'kilobyte',
    'MB': 'megabyte',
    'GB': 'gigabyte',
    'TB': 'terabyte',
    'PB': 'petabyte',
    'Kb': 'kilobit',
    'Mb': 'megabit',
    'Gb': 'gigabit',
    'Tb': 'terabit',
    'TB': 'petabit',
    'Pb': 'petabit',

    # Storage Speeds
    'Kbps': 'kilobits per second',
    'Mbps': 'megabits per second',
    'Gbps': 'gigabits per second',
    'Tbps': 'terabits per second',

    # Current
    'mA': 'milliampere',

    # Direction
    'N': 'North',
    'E': 'East',
    'W': 'West',
    'S': 'South',
    'NE': 'North East',
    'NW': 'North West',
    'SW': 'South East',
    'SE': 'South West'
    }

## List of common uncapitalised full forms.
full_form_uncapitalised = [
        'tv', 'ac', 'iirc', 'lol', 'smh', 'rofl', 'brb', 'gn'
]

## Dictionary of number representation.
numbers = {
    '-': 'minus',
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    '10': 'ten',
    '11': 'eleven',
    '12': 'twelve',
    '13': 'thirteen',
    '14': 'fourteen',
    '15': 'fifteen',
    '16': 'sixteen',
    '17': 'seventeen',
    '18': 'eighteen',
    '19': 'nineteen',
    '20': 'twenty',
    '30': 'thirty',
    '40': 'forty',
    '50': 'fifty',
    '60': 'sixty',
    '70': 'seventy',
    '80': 'eighty',
    '90': 'ninety'
}

## Dictionary of extended numericals.
extended_nums = {
    '0': 'ieth',         # y is replaced by this if the last numeric is 0
    '1': 'first',
    '2': 'second',
    '3': 'third',
    '4': 'fourth',
    '5': 'fifth',
    '6': 'sixth',
    '7': 'seventh',
    '8': 'eighth',
    '9': 'ninth'
}

## Dictionary of abbreaviated months.
month = {
    'jan': 'january',
    'feb': 'february',
    'mar': 'march',
    'apr': 'april',
    'may': 'may',
    'jun': 'june',
    'jul': 'july',
    'aug': 'august',
    'sept': 'september',
    'oct': 'october',
    'nov': 'november',
    'dec': 'december',
}

## Dictinary of numbers representing months.
month_num = {
    '01': 'january',
    '02': 'february',
    '03': 'march',
    '04': 'april',
    '05': 'may',
    '06': 'june',
    '07': 'july',
    '08': 'august',
    '09': 'september',
    '10': 'october',
    '11': 'november',
    '12': 'december',
}


# ------------------------------------
# Defining Functions for all utilities
# ------------------------------------

# CURRENCY ------------------

## Checks for currency symbol in the input string and outputs T/F, currency and its sub-currency.
def has_symbol(input_string):
    if bool(re.search(r'\$', input_string)):
        return True, 'dollar', 'cent'
    elif bool(re.search(r'\£', input_string)):
        return True, 'pound', 'pounce'
    elif bool(re.search(r'\€', input_string)):
        return True, 'euro', 'cent'
    elif bool(re.search(r'R\.{0,1}[Ss][ \.]{1}', input_string)):
        return True, 'rupee', 'paise'
    else:
        return False, '', ''


## Returns output for input string having currency symbol
def get_symbol(input_string, currency, small_currency):
    res = ''
    plural = False
    smaller_currency_used = False

    if currency == 'rupee':
        input_string = re.sub('\.', '', input_string[:3]) + input_string[3:]         # 'Rs.32.34' --> 'Rs32.34'
        input_string = input_string[2:].lstrip(' ').lstrip('.')
    else:
        input_string = input_string[1:].lstrip(' ')

    currency_list = input_string.split(' ')

    for curr in currency_list:
        key_list = re.findall('([0-9.,]+|[a-zA-Z].*)', curr)
        for key in key_list:
            # print(key)
            if has_decimal(key):
                num_list = key.split('.')
                
                # If the number of decimal places is two, then need to use the smaller currency; ex: 12.22 dollars is 12 dollars and 22 cents
                if len(key_list) == 1 and len(currency_list) == 1 and len(num_list[1]) <= 2 and bool(re.search(r'^\d+\.*\d+$', key)):     # if there is any other unit involved, then we do not have to use the smaller currency utility
                    smaller_currency_used = True
                    num_list = key.split('.')
                    ## '$12.100' --> 'twelve point one o o dollars' since cents can only be till 100!
                    
                    res += get_onlydigits(num_list[0]) + ' ' + currency
                    if (int(num_list[0]) != 1):
                        res += 's'
                    if len(num_list[1]) == 1:
                        num_list[1] = str(int(num_list[1])*10)
                    if len(num_list[1]) == 2:
                        res += ' and ' + get_onlydigits(num_list[1]) + ' ' + small_currency
                        # print(num_list[1])
                        if (int(num_list[1]) != 1):
                            print(num_list[1])
                            if currency == 'rupee':
                                res = res[:-1] + 'e'            # 'paisa' to be converted to 'paise'
                            else:
                                res += 's'
                        # else:
                        #     res += 's'
                else:
                    if float(key) != 1.0:
                        plural = True
                        res += get_decimal(key) + ' '
                    
            elif has_onlydigits(key):
                if len(key) != 1:
                    plural = True
                res += get_onlydigits(key) + ' '
            elif key in full_form.keys():
                if key == 'm':
                    res += ' million '
                else:
                    res += full_form[key] + ' '
                plural = True                       # since it might be 1 million euros
                
            else:
                plural = True
                res += key + ' '
    
    # If there was no unit attached and we have processed it using smaller currency as well, then the complete string creation has already been done
    if not smaller_currency_used:
        if plural:
            res += currency + 's'
        else:
            res += currency                     # to remove making the currency plural
    return ' '.join(res.split())


# PUNCTUATIONS ------------------

## Checks for punctuations in the input string and outputs T/F
def has_punc(input_string):
    return bool(re.search(r'[^\w\s]', input_string))

## Returns output for keyword being punctuations
def get_punc(input_string):
    return 'sil'


# NUMERICALS ONLY ------------------

# ## Checks for only numericals being present inside input string
# def has_numeric(input_string):
#     return bool(re.search(r'\d', input_string))


# FOUR NUMERICALS ONLY (for years) ------------------

## Checks for input string consisting of four numerics
def has_fournumeric(input_string):
    return bool(re.search(r'^\d{4}s{0,1}$', input_string))

## Returns output for four numerics (especially for years)
def get_fournumeric(input_string):
    if len(input_string) == 4:
        if input_string[1:3] == '00':               # handles 2007 --> 'two thousand seven'
            return get_onlydigits(input_string)
        else:                                       # handles 1906 --> 'nineteen o six'; but 2012 --> 'twenty twelve'
            first_two = input_string[0:2]
            last_two = input_string[-2:]
            if get_onlydigits(first_two) != 'zero':
                if last_two == '00':                    # handles 1200 --> 'twelve hundred'
                    return get_onlydigits(first_two) + ' hundred'
                elif input_string[2] == '0':            # handles 1906 --> 'nineteen o six';
                    return get_onlydigits(first_two) + ' o ' + get_onlydigits(last_two)
                else:                                   # handles 2012 --> 'twenty twelve';
                    return get_onlydigits(first_two) + ' ' + get_onlydigits(last_two)
            else:                                       # handles 0002 --> 'two';
                return get_onlydigits(last_two)

    elif len(input_string[:-1]) == 4 and input_string[-1] == 's':
        res = get_fournumeric(input_string[:-1])
        if res[-1] == 'y':
            res = res[:-1] + 'ies'                  # 1940s --> 'nineteen forties'
        else:
            res += 's'
        return res

    else:
        return ''                                   # for some cases in dates which use this function


# NUMERICALS WITH COMMAS (for quantities) ------------------

## Checks for input string consisting of numericals allowed with commas
def has_onlydigits(input_string):
    # sid 110 can tell that the first digit has to be greater than 0
    return bool(re.search(r'^(-|[1-9])\d*[,\d]*\d*$', input_string))   

## Returns output for numericals that allow commas to separate numerical values
def get_onlydigits(input_string):
    input_string = str(input_string)
    
    # To ensure that no empty strings give any issue
    if input_string.strip() == '':
        return ''

    res = ''
    input_string = re.sub(r'[^\d-]', '', input_string)      # negative numbers can also exist
    int_string = int(input_string)
    
    if int_string < 0:
        res += 'minus '                     # there would surely be something in front of the negative sign here.
        input_string = input_string[1:]
        int_string *= -1

    # The case with only 4 digits needs to be incorporated; 1991 --> nineteen ninety one; the first two numerals are separated from the other two

    # Handling numbers directly from dictionary
    if int_string <= 20:
        res += numbers[str(int_string)]     # for example: '07' means '7' and thus has to be looked this way in the dictionary
        return res                          # since we do not need to do anything further from here


    # Handling two digit numbers not in dictionary
    if int_string < 100:
        if str(int_string) in numbers.keys():       # '30' --> 'thirty'
            res += numbers[str(int_string)]
            return res
        else:
            tenth_place = (int_string//10) * 10     # '35' --> 'thirty five'
            unit_place = (int_string % 10)
            res += numbers[str(tenth_place)] + ' ' + numbers[str(unit_place)]
            return res

    t = 1000
    # Handling hundreds
    if int_string < t:
        hundred_place = int_string // 100
        if int_string % 100 == 0:                   # '900' --> 'nine hundred'
            res += numbers[str(hundred_place)] + ' hundred'
            return res
        else:
            res += numbers[str(hundred_place)] + ' hundred ' + get_onlydigits(str(int_string % 100))
            return res

    # Handling thousands
    # As the number increases, the number of zeroes becomes over-whelming! Better to convert it into a variable
    m = t*t
    if int_string < m:
        thousand_place = int_string // t
        if int_string % t == 0:                   
            res += get_onlydigits(str(thousand_place)) + ' thousand' # '72000' --> 'seventy two thousand'; and 72 is not in the main dictionary and thus recursion needs to be done
            return res
        else:
            res += get_onlydigits(str(thousand_place)) + ' thousand ' + get_onlydigits(str(int_string % t))
            return res

    # Handling millions
    b = m*t
    if int_string < b:
        million_place = int_string // m
        if int_string % m == 0:                   
            res += get_onlydigits(str(million_place)) + ' million' # '72000' --> 'seventy two thousand'; and 72 is not in the main dictionary and thus recursion needs to be done
            return res
        else:
            res += get_onlydigits(str(million_place)) + ' million ' + get_onlydigits(str(int_string % m))
            return res

    # Handling billions
    tr = b*t
    if int_string < tr:
        billion_place = int_string // b
        if int_string % b == 0:                   
            res += get_onlydigits(str(billion_place)) + ' billion' # '72000' --> 'seventy two thousand'; and 72 is not in the main dictionary and thus recursion needs to be done
            return res
        else:
            res += get_onlydigits(str(billion_place)) + ' billion ' + get_onlydigits(str(int_string % b))
            return res

    # Handling trillions | ref: GDP is also only in trillions!
    pr = tr*t
    if int_string < pr:
        prillion_place = int_string // tr
        if int_string % tr == 0:                   
            res += get_onlydigits(str(prillion_place)) + ' trillion' # '72000' --> 'seventy two thousand'; and 72 is not in the main dictionary and thus recursion needs to be done
            return res
        else:
            res += get_onlydigits(str(prillion_place)) + ' trillion ' + get_onlydigits(str(int_string % tr))
            return res

    return res


# ISBN CODES ------------------

## Checks for input string consisting of ISBN code structure
def has_isbncode(input_string):
    # If the first digit is zero, then the number can probably be for isbn; sid 110
    return bool(re.search(r'^\d+[ )(|-]{1,2}\d+', input_string))        # Since we want to find a repeating pattern, either the start or the end fixer has to be relaxed

## Returns output for ISBN Codes
def get_isbncode(input_string):
    res = ''
    prev = ''

    for char in input_string:
        # Punctuation case needs to be handled first, else '-' would be taken as 'minus' from the numbers dictionary
        if has_punc(char) or char == ' ':
            if res[-3:] == 'sil':
                continue
            res += ' ' + get_punc(char)
            continue
        
        # '0' case needs to be handled before other numerals since this is converted to 'o' rather than 'zero'
        if char == '0':
            res += ' o'
        
        else:
            res += ' ' + numbers[char]
    
    res = ' '.join(res.split())             # to remove extra spaces at the front or end
    return res


# DECIMAL VALUES ------------------

## Checks for input string consisting of numericals with decimals
def has_decimal(input_string):
    return bool(re.search(r'^\d+[,]{0,1}\d*[.]\d+$', input_string))      # ending on a digit is justified since period (.) is a different token in the corpus

## Returns output for floating numbers i.e. with decimals
def get_decimal(input_string):
    res = ''
    num_list = input_string.split('.')
    # For ex: '90.0' --> 'ninety point zero' and not 'ninety point o'
    if bool(re.search(r'^0+$', num_list[1])):
        res = res + get_onlydigits(num_list[0]) + ' point ' + 'zero '*len(num_list[1])
    else:
        res = res + get_onlydigits(num_list[0]) + ' point ' + get_isbncode(num_list[1])
    return ' '.join(res.split())


# UNCAPITALIZED FULL FORMS ------------------

## Checks for input string consisting of some special keywords that represent abbreviations but are uncapitalized
def has_specialfullform(input_string):
    return bool(input_string in full_form_uncapitalised)

## Returns output for special, uncapitalized abbreviations
def get_specialfullform(input_string):
    return get_allcaps(input_string)


# UNITS ------------------

## Checks for input string consisting of common units indicative of the nature of the numerical it suceeds
def has_units(input_string):
    return bool(re.search(r'^\d+.*[a-zA-Z]+', input_string))

## Returns output for unit carrying input string
def get_units(input_string):
    res = ''
    plural = False
    
    # '50.0Kb Gb/s' --> ['50.0Kb', 'Gb/s']
    words_list = input_string.split(' ')

    for word in words_list:
        # Separating the number; for ex: '50.0Kb' --> ['50.0', 'Kb']
        key_list = re.findall('([0-9.,/]+|[a-zA-Z].*)', word)
        for key in key_list:
            if bool(re.search(r'/', key)):
                temp_list = key.split('/')
                left = True
                for temp in temp_list:
                    if not left:
                        res += 'per '
                    if has_decimal(temp):
                        res += get_decimal(temp) + ' '
                    elif has_onlydigits(temp):
                        res += get_onlydigits(temp) + ' '
                    elif temp in full_form.keys():
                        if plural and left and ((temp != 'a.m.') and (temp != 'p.m.')):
                            res += full_form[temp] + 's '        # won't affect am, pm, etc.
                        else:
                            res += full_form[temp] + ' '
                    else:
                        res += temp + ' '
                    left = False
            
            elif has_decimal(key):
                # Since it can also be '8 a.m.' where 'a.m.' --> 'a m'
                if key in full_form.keys():
                    res += full_form[key] + ' '
                # Otherwise, we are talking about floating point number, for ex: 80.3
                else:
                    res += get_decimal(key) + ' '
                    if (int(key[0]) > 1) or (len(key) > 1):
                        plural = True                       # 5 kilometers
            
            elif has_onlydigits(key):
                res += get_onlydigits(key) + ' '  
                if (int(key[0]) > 1) or (len(key) > 1):
                    plural = True                       # 5 kilometers
                             
            elif key in full_form.keys():
                if plural and ((re.sub('\.', '', key.lower()) != 'am') and (re.sub('\.', '', key.lower()) != 'pm')):
                    res += full_form[key] + 's '        # won't affect am, pm, etc.
                else:
                    res += full_form[key] + ' '
            
            else:
                res += key + ' '

    res = ' '.join(res.split())
    
    # if the final result has accidently placed two 'ss' due to plurality, we can remove it
    if res[-2:] == 'ss':
        res = res[:-2] + 's'
    return res


# EXTENDED NUMERICALS ------------------

## Checks for input string consisting of special keywords that are indicative of numericals to represented with extended forms
def has_extendednums(input_string):
    return bool(re.search(r'\d+[ ]*(st|nd|rd|th)', input_string))

## Returns output for numericals needing extended representation; # Handles the cases of extended numerals; for ex: '100th' --> 'one hundredth'
def get_extendednums(input_string):
    # Getting the last numeric digit present in the string
    numeric = re.sub(r'[^\d]', '', input_string)
    numeric = numeric.lstrip('0')         # to remove initial zeroes in the string
    numeric_string = str(numeric)
    non_unit_numeric = (int(numeric) // 10) * 10

    # Extended form of 12 is different than expected
    if numeric_string == '12':
        return 'twelfth'

    # For ex: 02nd --> 2, then this only has one digit
    if numeric_string in extended_nums.keys():
        if numeric_string == '0':
            return 'zeroth'
        return extended_nums[numeric_string]
    
    # The last unit plays the determining role for creating extended forms
    unit_numeric = numeric[-1]

    # If the last two digits are between 10 and 20 (both inclusive), then we have to get its direct form
    last_two_digits = int(numeric[-2:])
    if len(numeric) == 2 and (last_two_digits >= 10) and (int(last_two_digits) < 20):
        return get_onlydigits(str(last_two_digits)) + 'th'
    elif len(numeric) > 2 and (last_two_digits >= 10) and (int(last_two_digits) < 20):
        return get_onlydigits((int(numeric) // 100) * 100) + ' ' + get_extendednums(str(last_two_digits))
    else:
        # Getting the translation for the non-last digit
        non_unit_string = get_onlydigits(str(non_unit_numeric))
        # Handling case with last two digits as 0; for ex: 100th --> 'one hundreth' and not 'one hundreith'
        if last_two_digits == 0:
            return get_onlydigits((int(numeric) // 100) * 100) + 'th'
        # Handling case with last two digits as 0; for ex: 130th --> 'one hundred thirieth' and not 'one hundred thirtyth'
        elif unit_numeric == '0':
            return non_unit_string[:-1] + extended_nums[unit_numeric]
        else:
            return non_unit_string + ' ' + extended_nums[unit_numeric]


# ALL CAPS ------------------

## Checks for input string consisting of all capital letters (abbreviations in general)
def has_allcaps(input_string):
    return ((len(input_string) > 2) and bool(re.search(r'^[A-Z]{2,}[a-z]{1,2}\.*$', input_string))) or (bool(re.search(r'^[A-Z]+\.*$', input_string))) or (bool(re.search(r'[A-Z][\.-]$', input_string)))

## Returns output for input string having capitalized abbreviations
def get_allcaps(input_string):                          # ref: sid 202
    # Converts the abbreviated version to a spaced version as per output format
    input_string = re.sub(r'[\.-]', '', input_string)
    
    # sid: 162 where MEPs --> 'm e p's
    if input_string[-1] == 's' and bool(re.search(r'[A-Z]', input_string[-2])):
        res = ((' '.join(input_string[:-1])).lower()) + "'s"
    else:
        res = ((' '.join(input_string)).lower())
    return ' '.join(res.split())


# ABBREVIATIONS ------------------

## Returns output for input string having abbreviations that have a full form present in the corpus
def get_abbr(input_string):
    if input_string in full_form.keys():
        return full_form[input_string]


# COLON SEPARATED NUMERICALS (generally time or ref numbers) ------------------

## Checks for input string consisting of colon separated numericals
def has_time(input_string):
    return bool(re.search(r'^\d{1,2}: *\d{1,2}', input_string))
    
## Returns output for input string having colon separated numericals
def get_time(input_string):
    res = ''
    hour_24 = False
    count = 0
    time_suffix = False
    
    input_string = re.sub(r'\.', '', input_string)
    input_string = re.sub(r' ', '', input_string)
    
    time_list = input_string.split(' ')

    for time in time_list:
        key_list = re.findall('([0-9.,:/]+|[a-zA-Z].+)', time)
        for key in key_list:
            # Handles '5:30' --> 'five thirty'
            if bool(re.search(r':', key)):
                temp_list = key.split(':')
                
                for temp in temp_list:
                    if temp == '00':
                        count += 1
                    
                ## 00:00 --> zero hundred
                if count == 2:
                    res = 'zero hundred'
                    return res

                ## Checking through the string to find if we have am or pm, which would mean that "o'clock" would not exist
                for key_temp in key_list:
                    # print('Yay!', key_temp)
                    if key_temp.lower() == 'am' or key_temp.lower() == 'pm':
                        time_suffix = True          # There is am or pm in the input string
                        # print('time suf')
                        break
                    

                # Handling sid 201 that for 2:27:07 --> 'two hours twenty seven minutes and seven seconds
                if len(temp_list) == 3:
                    # print("hello")
                    counter = 1
                    for temp in temp_list:
                        temp = temp.lstrip('0')             # to remove initial zeroes in the string
                        temp = temp.lstrip(' ')             # to remove initial empty spaces in the string
                        if has_onlydigits(temp):
                            if counter == 1:
                                res += get_onlydigits(temp) + ' hours '
                            elif counter == 2:
                                res += get_onlydigits(temp) + ' minutes '
                            elif counter == 3:
                                res += ' and ' + get_onlydigits(temp) + ' seconds '
                            counter += 1                        # indicating that the next time term comes
                else:
                    for temp in temp_list:
                        # 24 hour clock means that 19:00 -> 'nineteen hundrd'
                        if len(temp) >= 1 and int(temp) > 12:   
                            hour_24 = True
                        
                        # sid 118: 19:00 --> 'nineteen hundred'
                        if temp == '00':
                            if hour_24:
                                res += 'hundred '
                            ## as per Piazza query, we need to write '7:00' as 'seven o'clock'
                            elif not time_suffix:
                                res += "o'clock "
                        
                        # to remove initial zeroes in the string; except for the case when it is '00'
                        elif has_onlydigits(temp.lstrip('0')):
                            res += get_onlydigits(temp.lstrip('0')) + ' '
            
            # ' 30' --> '30' --> 'thirty'
            elif has_onlydigits(key.lstrip()):
                res += get_onlydigits(key.lstrip()) + ' '

            elif bool(re.search(r'^[a-zA-Z]+$', key)):
                res += get_allcaps(key) + ' '
            else:
                res += key + ' '
    return ' '.join(res.split())


# DATE (generally time or ref numbers) ------------------

## Checks for input string consisting of dates
def has_date(input_string):
    month_day = bool(re.search(r'Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sept|September|Oct|October|Nov|November|Dec|December', input_string))
    ddmmyyyy = bool(re.search(r'^\d{1,2}[ ,-]+([0]\d{1}|1[012])[ ,-]\d{4}$', input_string))     # no control on daters
    mmddyyyy = bool(re.search(r'^([0]\d{1}|1[012])[ ,-]\d{1,2}[ ,-]+\d{4}$', input_string))
    yyyymmdd = bool(re.search(r'^\d{4}[ ,-]+([0]\d{1}|1[012])[ ,-]\d{1,2}$', input_string))
    
    # Starting with year
    if yyyymmdd:
        year = True
    else:
        year = False

    # Starting with month
    if mmddyyyy:
        month = True
    else:
        month = False
    
    # Starting with day
    if ddmmyyyy:
        day = True
    else:
        day = False
    
    # Has a day component
    if yyyymmdd or mmddyyyy or ddmmyyyy or month_day:
        return True, [day, month, year, month_day]
    else:
        return False, [False, False, False, False]

## Returns output for input string having dates
def get_date(input_string, order):
    # order is of the form [day, month, year, month_day]

    def has_month(input_string):
        return bool(re.search(r'^\D+$', input_string))

    def get_month(input_string):
        if input_string.lower() in month.keys():
            return month[input_string.lower()]
        else:
            return input_string.lower()

    res = ''
    keyword_list = re.split(r'\s+|[,.-]\s*', input_string)
    # Back-filling day, month or year number with 0s; for ex: October 1, 2021 --> October 01, 2021
    for i in range(len(keyword_list)):
        if len(keyword_list[i]) == 1:
            keyword_list[i] = '0' + keyword_list[i]
        elif has_onlydigits(keyword_list[i][:-2]) and (keyword_list[i][-2:] == 'nd' or keyword_list[i][-2:] == 'th' or keyword_list[i][-2:] == 'st' or keyword_list[i][-2:] == 'rd'):
            keyword_list[i] = keyword_list[i][:-2]
            if len(keyword_list[i]) == 1:
                keyword_list[i] = '0' + keyword_list[i]

    # for key in keyword_list:
    #     print(type(key))

    # January 14, 2008 --> january fourteenth two thousand eight
    # 20 January 2010 --> the twentieth of january twenty ten
    # January 2010 --> january twenty ten

    if order[3]:
        # Handles if input string only has the month name like 'January'
        if bool(re.search(r'^\D+$',input_string)):
            return '<self>'                 # since it has no numeral to tell us that we are talking about a specific date
        else:
            # If first keyword is a month name
            if bool(re.search(r'^\D+$', keyword_list[0])):
                if has_month(keyword_list[0]):
                    res += get_month(keyword_list[0])
                
                # If the next keyword is a date, then push its extended form                  
                if bool(re.search(r'^\d{2}$', keyword_list[1])):
                    res += ' ' + get_extendednums(keyword_list[1])
                    date_inlcuded = True

                    # If there exists an year to process
                    if len(keyword_list) > 2:
                        res += ' ' + get_fournumeric(keyword_list[2])
                    
                    return ' '.join(res.split())

                # If the next keyword is a year
                elif bool(re.search(r'^\d{4}$', keyword_list[1])):
                    res += ' ' + get_fournumeric(keyword_list[1])
                    return ' '.join(res.split())


            # If the keyword is a date, then its extended form needs to be used; 20 --> the twentieth
            elif bool(re.search(r'^\d{2}$', keyword_list[0])):
                # print(keyword_list[0])
                res = 'the ' + get_extendednums(keyword_list[0]) + ' of '
                date_included = True

                # if has_month(keyword_list[1]):
                res += get_month(keyword_list[1])
                month_included = True

                # If there exists an year to process
                if len(keyword_list) > 2:
                    res += ' ' + get_fournumeric(keyword_list[2])
                    year_included = True
                
                return ' '.join(res.split())
    
    # If the date is presented in mmddyyyy format; this case needs to be handled before ddmmyyyy as mentioned by instructor
    elif order[1]:
        res += 'the ' + get_extendednums(keyword_list[1].lstrip('0')) + ' of ' + month_num[keyword_list[0]] + ' ' + get_fournumeric(keyword_list[2])
        return res

    # If the date is presented in ddmmyyyy format
    elif order[0]:
        res += 'the ' + get_extendednums(keyword_list[0].lstrip('0')) + ' of ' + month_num[keyword_list[1]] + ' ' + get_fournumeric(keyword_list[2])
        return res

    # If the date is presented in yyyymmdd format
    elif order[2]:
        res += 'the ' + get_extendednums(keyword_list[2].lstrip('0')) + ' of ' + month_num[keyword_list[1]] + ' ' + get_fournumeric(keyword_list[0])
        return res

    else:
        return '<self>'


# FRACTIONS ------------------

## Checks for input string consisting of fractions
def has_division(input_string):
    return bool(re.search(r'-*(\d+)\s*/\d+$', input_string))

## Returns output for input string having fractions
def get_division(input_string):
    res = ''
    input_string = ' '.join(input_string.split(' ')).lstrip(' ')
    number_list = re.split(r'[/ ]', input_string)

    def get_num_by_den(num, den):
        str_num = get_onlydigits(num) + ' '
        str_den = get_extendednums(den)
        if den == '4':
            str_num += ' quarters'
        elif den == '2':
            str_num += ' halves'
        else:
            str_num += str_den + 's'
        return str_num


    # Handling two numbers present in the same 'number' separated by space i.e. '1 1/2'
    if len(number_list) == 3:
        res += get_onlydigits(number_list[0]) + ' and '
        if number_list[1] == '1' and number_list[2] == '2':
            res += ' a half'
        else:
            res += get_num_by_den(number_list[1], number_list[2])

    # Handling types of '7/8'
    elif len(number_list) == 2:
        if number_list[0] == '1' and number_list[1] == '2':
            res += 'half'
        elif number_list[0] == '1' and number_list[1] == '4':
            res += 'quarter'
        else:
            res = get_num_by_den(number_list[0], number_list[1])

    return ' '.join(res.split())


# PERCENTAGES ------------------

## Checks for input string consisting of percentages
def has_percent(input_string):
    return bool(re.search(r'%', input_string)) or bool(re.search(r'\d(pc)+$', input_string))

## Returns output for input string having percentages
def get_percent(input_string):
    res = ''
    input_string = input_string[:-1]            # removing the % or c symbol first
    
    if type(input_string[-1]) == 'str':
        input_string = input_string[:-1]            # removing the p symbol then

    if has_decimal(input_string):
        res += get_decimal(input_string)
    else:
        res += get_onlydigits(input_string)

    return res + ' percent'


# ----------------------------------------------------------
# Defining function for getting the solutions
# ----------------------------------------------------------

## Returns complete output for input sentences having all kinds of nuances
def solution(input_tokens):
    sol = []
    flag = False
    # left_is_isbn = False
    prev_token = ''

    for token in input_tokens:

        # All the extra spaces at the start and end of the token should be trimmed since the tokenisation may have a problem (for ex: sid 85 --> "21 ")
        token = ' '.join(token.split())

        if prev_token == 'ISBN' and has_onlydigits(token.lstrip('0')) and not flag:
            sol.append(get_isbncode(token))
            flag = True
            # left_is_isbn = False          # the immediate numerical instance after 'ISBN' has been handled

        # Handling Punctuation.
        if((has_punc(token) and (len(token) == 1)) and not flag):
            sol.append(get_punc(token))
            flag = True

        # Handling roman numerals.
        if token in roman_numerals.keys() and not flag:
            # If the previous token's first letter is capital, then we can be 'somewhat more certain' about using extended form of the roman numeral
            if bool(re.search(r'^[A-Z]', prev_token)):
                # sid 11 --> Chapter 'IV' --> 'four' and not 'the fourth'; notion of proper noun can be developed although sid 49 seems incorrectly labelled
                if prev_token not in ['Chapter', 'Page', 'Section', 'Set', 'Game', 'Match', 'Mark']:
                    sol.append('the ' + get_extendednums(roman_numerals[token]))
                else:
                    sol.append(get_onlydigits(roman_numerals[token]))
            else:
                sol.append(get_onlydigits(roman_numerals[token]))
            flag = True

        # Handling currency symbols.
        if has_symbol(token)[0] and not flag:
            sol.append(get_symbol(token, has_symbol(token)[1], has_symbol(token)[2]))
            flag = True

        # Handling percentage symbols.
        if has_percent(token) and not flag:
            sol.append(get_percent(token))
            flag = True

        # Handling time units; for ex: '5:30pm PST' --> 'five thirty p m p s t'
        if has_time(token) and not flag:
            sol.append(get_time(token))
            flag = True

        # Handling all capital tokens (not as abbreviations though).
        if has_allcaps(token) and (len(token) > 1) and not flag:
            # if token == 'ISBN':
            #   left_is_isbn = True
            sol.append(get_allcaps(token))
            flag = True              # because we are directly continuing ahead

        # Handling common abbreviations not capitalized
        if has_specialfullform(token):
            sol.append(get_specialfullform(token))
            flag = True

        # Handling dates.
        if has_date(token)[0] and not flag:
            res = get_date(token, has_date(token)[1])
            sol.append(res)
            flag = True

        # Handling 4 digits of numerals; years in general, if there are no symbols, before other numerical strings.
        if has_fournumeric(token) and not flag:
            sol.append(get_fournumeric(token))
            flag = True

        # Handling pure numericals (numbers).
        # if has_onlydigits(token.lstrip('0')) and not flag and not left_is_isbn:
        if has_onlydigits(token.lstrip('0')) and not flag:
            sol.append(get_onlydigits(token))
            flag = True

        # Handling division of numbers.
        if has_division(token) and not flag:
            sol.append(get_division(token))
            flag = True

        # Handling extended numericals, for ex: 21st --> 'twenty first'; has to be handled before units.
        if has_extendednums(token) and not flag:
            sol.append(get_extendednums(token))
            flag = True

        # Handling tokens having numeric character with units (has to be done before ISBN; for ex: 823.05 KB).    
        if has_units(token) and not flag:
            sol.append(get_units(token))
            flag = True

        # Handling decimal values.
        if has_decimal(token) and not flag:
            sol.append(get_decimal(token))
            flag = True

        # Handling ISBN Code.
        # if not flag and left_is_isbn or has_isbncode(token):
        if (has_isbncode(token) and not flag):
            sol.append(get_isbncode(token))
            flag = True
            # left_is_isbn = False          # the immediate numerical instance after 'ISBN' has been handled

        # If nothing else, then the token should be <self>.
        if not flag:
            if token in ['Nahr', 'Yai', 'Phrao', 'mes']:
                sol.append(get_allcaps(token))
            else:
                sol.append('<self>')

        prev_token = token          # prev_token is used to has information about the just previous token and this information can extensively be used for ISBN codes
        flag = False                # preparing for the next iteration.
        # left_is_isbn = False        

    return sol

## Saves the solutions in a the file name sent as input argument
def solution_dump(input_data, solution_file_path):
  solution_data = []
  for input_sentence in input_data:
    solution_sid = input_sentence['sid']
    # print(solution_sid)
    solution_tokens = solution(input_sentence['input_tokens'])
    solution_data.append({'sid':solution_sid,
                          'output_tokens':solution_tokens})

  with open(solution_file_path,'w', encoding='utf-8') as solution_file:
    json.dump(solution_data, solution_file, indent=2, ensure_ascii=False)
    solution_file.close()


if __name__ == '__main__':

    ## Argument Parser
    args = read_cli()

    ## Importing input data.
    with open(args.input_path, 'r', encoding='utf-8') as input_file:
        input_data = json.load(input_file)
        input_file.close()

    ## Saving the outputs to this file
    solution_dump(input_data, args.solution_path)