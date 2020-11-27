def date_format(value):
    months = ("January","February","March","May","Juny","July",
    "August","September","Octover","November","December")
    month = months[value.month-1]
    return "{} de {} del {}".format(value.day,month,value.year)