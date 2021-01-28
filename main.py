
import app
import csv
import datetime as dt

#Task: You have data about flights (segments).
# Your task is to find all combinations of flights for:
# passengers with no bags, one bag or two bags are able to travel, having 1 to 4 hours for each transfer between flights.
# The columns in table of input data are explained bellow:

#Example of data
#source,destination,departure,arrival,flight_number,price,bags_allowed,bag_price
#USM,HKT,2017-02-11T06:25:00,2017-02-11T07:25:00,PV404,24,1,9
#USM,HKT,2017-02-12T12:15:00,2017-02-12T13:15:00,PV755,23,2,9


def automatic(file):
    x = app.do_list(app.start((file))) #loading csv file, transfoming flights data into list
    y = app.sort(x) #sort flights by date&time
    z = app.making_pair(y) #making 1+1 combination
    zz = app.making_triples(z)
    result = app.format_pairs(z,0) #1+1 combinations with zero baggage
    result1 = app.format_pairs(z,1) #1+1 combinations with 1 baggage
    result2 = app.format_triples(zz,0) #1+1+1 combinations with zero baggage
    result3 = app.format_triples(zz,1) #1+1+1 combinations with one baggage
    header = ["src", "stop", "dst", "flight1", "flight2", "dep_time", "arr_time", "duration", "bags", "price"] #output format of 1+1combinations
    header1 = ["src", "stop", "stop1", "dst", "flight1", "flight2", "flight3","dep_time", "arr_time", "duration", "bags", "price"]
    f = open("combinations.csv", "w") # 1+1 combiantions into csv
    f_writer = csv.writer(f)
    f_writer.writerow(header)
    f_writer.writerows(result) #zero baggage itineraries first
    f_writer.writerows(result1)
    f.close()
    g = open("triple_combnations.csv", "w") #
    g_writer = csv.writer(g)
    g_writer.writerow(header1)
    g_writer.writerows(result2) #zero baggage itineraries first
    g_writer.writerows(result3)
    g.close()
    return(result, result1, result2, result3)

#result check - print(automatic("PY_entry_task.csv"))






