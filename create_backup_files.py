#!/usr/bin/env python3

import datetime

for days_ago in range(1300):
    that_day = datetime.date.today() - datetime.timedelta(days=days_ago)
    file_name = 'backup_'+str(that_day.year)+'-'+str(that_day.month)+'-'+str(that_day.day)+'.dat'
    with open(file_name, 'w') as fil_handle:
        fil_handle.write("hello")
