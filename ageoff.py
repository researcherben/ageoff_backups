#!/usr/bin/env python3

import datetime
import glob
import os
import random

def remove_extra_backups_per_month(dict_of_backups, max_number_of_backups_per_month):
    """

    >>> dict_of_backups = {}
    >>> max_number_of_backups_per_month = 4
    >>> remove_extra_backups_per_month(dict_of_backups, max_number_of_backups_per_month)
    """
    #print('size of input dict =',len(dict_of_backups))
    number_of_files_removed = 0
    list_of_month_years = []
    for date_of_backup_as_datetime_object, filename in dict_of_backups.items():
        list_of_month_years.append((date_of_backup_as_datetime_object.month, date_of_backup_as_datetime_object.year))
    list_of_month_years = list(set(list_of_month_years))
    #print('list_of_month_years', list_of_month_years)
    for month_year in list_of_month_years:
        backups_per_month = {}
        for date_of_backup_as_datetime_object, filename in dict_of_backups.items():
            if (date_of_backup_as_datetime_object.month == month_year[0] and
                date_of_backup_as_datetime_object.year == month_year[1]):
                backups_per_month[date_of_backup_as_datetime_object] = filename
                #print("match found:",date_of_backup_as_datetime_object)
        #print('number of backups per month in ',month_year,'is',len(backups_per_month))
        number_removed_this_month = 0
        if len(backups_per_month)>max_number_of_backups_per_month:
            number_to_remove = len(backups_per_month) - max_number_of_backups_per_month

            which_to_remove = random.sample(list(backups_per_month.items()), number_to_remove)
            for backup_tuple in which_to_remove:
                #print('removed ',backup_tuple[1])
                os.remove(backup_tuple[1])
                number_of_files_removed+=1
                number_removed_this_month+=1
            #print(number_removed_this_month,"removed in",month_year)
    return number_of_files_removed

list_of_backup_files = glob.glob('backup_*.dat')

# more recent than months: keep the daily backup
two_months_ago = datetime.date.today() - datetime.timedelta(days=60)
# between two months old and one year old: keep 10 randomly selected backups per month

one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
# between one year old and two years old: keep 5 randomly selected backups per month
two_years_ago = datetime.date.today() - datetime.timedelta(days=365*2)
# older than two years old: keep 2 randomly selected backups per month

backups_between_two_months_and_one_year = {}
backups_between_one_year_and_two_years = {}
backups_older_than_two_years = {}

all_backups = {}
for filename in list_of_backup_files:
    date_of_backup_as_str = filename.replace('backup_','').replace('.dat','')
    #print(date_of_backup)
    date_of_backup_as_datetime_object = datetime.datetime.strptime(date_of_backup_as_str, '%Y-%m-%d') # https://strftime.org/
    #print(datetime_object.date())
    month_year_tuple = (date_of_backup_as_datetime_object.month, date_of_backup_as_datetime_object.year)

#    try:
#        all_backups[month_year_tuple].append(filename)
#    except KeyError:
#        all_backups[month_year_tuple]=[filename]

#for month_year_tuple, list_of_backup_files in all_backups.items():

    if date_of_backup_as_datetime_object.date()>=two_months_ago:
        #print('do nothing to '+filename)
        continue
    elif date_of_backup_as_datetime_object.date()<two_months_ago and date_of_backup_as_datetime_object.date()>=one_year_ago:
        backups_between_two_months_and_one_year[date_of_backup_as_datetime_object.date()] = filename
    elif date_of_backup_as_datetime_object.date()<one_year_ago and date_of_backup_as_datetime_object.date()>=two_years_ago:
        backups_between_one_year_and_two_years[date_of_backup_as_datetime_object.date()] = filename
    elif date_of_backup_as_datetime_object.date()<two_years_ago:
        backups_older_than_two_years[date_of_backup_as_datetime_object.date()] = filename
    else:
        raise Exception("date of backup unrecognized", date_of_backup_as_datetime_object)

#print('num of backups older than 2 years =', len(backups_older_than_two_years))

number_of_files_removed = remove_extra_backups_per_month(backups_between_two_months_and_one_year, max_number_of_backups_per_month=12)
print('number of files removed between 2 months and 1 year:', number_of_files_removed)
number_of_files_removed = remove_extra_backups_per_month(backups_between_one_year_and_two_years, max_number_of_backups_per_month=6)
print('number of files removed between 1 year and 2 years:', number_of_files_removed)
number_of_files_removed = remove_extra_backups_per_month(backups_older_than_two_years, max_number_of_backups_per_month=3)
print('number of files removed older than 2 years:', number_of_files_removed)
