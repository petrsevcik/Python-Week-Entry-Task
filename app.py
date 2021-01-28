
#packages
import os
import csv
import datetime as dt


#loading csv file and creating nested list
def start(file):
    f = open(file)
    f_reader = csv.reader(f)
    temp_flights = []
    for row in f_reader:
        temp_flights.append(row)
    f.close()
    temp_flights.pop(0)#here we will need to delete the first list - header from csv file
    return(temp_flights)

#making list from imported flights. Data about flights were imported as a string
def do_list(temp_flights):
    flights = []
    for flight in temp_flights:
        f_list = flight[0].split(",")
        flights.append(f_list)
    return flights

def sort(flights): #sorting by departure date
    flights.sort(key=lambda x: x[2])
    return flights

def route(f_list): #info about route from list - not needed in main
    f_route = f_list[0]+"-"+f_list[1]
    return f_route

def is_connecting(list1, list2): # detecting if two flights are connecting
    if list1[1] == list2[0]:
        return True
    else:
        return False

def is_connected(list1, list2): #detecting if two flights are connected - not needed in main
    if list2[0] == list1[1]:
        return True
    else:
        return False

def time_window(list1, list2): # counting time window between two flights
    td1 = dt.datetime.strptime(list1[3], '%Y-%m-%dT%H:%M:%S')
    td2 = dt.datetime.strptime(list2[2], '%Y-%m-%dT%H:%M:%S')
    delta = td2 - td1
    #print("delta is:", delta)
    if dt.timedelta(minutes=59) < delta < dt.timedelta(hours=4, minutes=1): #must be more than 1 hour, less than 4
        return True
    else:
        return False
def deltas(list1, list2): #comparing if pair combinations contain same flights
    t1 = dt.datetime.strptime(list1[6], '%Y-%m-%dT%H:%M:%S')
    t2 = dt.datetime.strptime(list2[4], '%Y-%m-%dT%H:%M:%S')
    if t1 == t2:
        return True
    else:
        return False

def count_flight_price(list1, list2): #counting price for 1+1 itinerary
    f_price = int(list1[5]) + int(list2[5])
    return f_price

def bags(f_list): #bag allowance - not needed in main
    if int(f_list[6]) == "0":
        return 0
    elif int(f_list[6]) == "1":
        return 1
    elif int(f_list[6]) == "2":
        return 2
    else:
        return False

def count_bag_price(f_list): #counting bag price - not needed in main
    b_price = int(f_list[6])*int(f_list[7])
    return b_price

def making_pair(flights): #creating 1+1 combinations
    combinations = []
    for flight_one in flights:
        for flight_two in flights:
            if is_connecting(flight_one,flight_two) and time_window(flight_one,flight_two):
                new_route = [flight_one[0],flight_one[1],flight_two[1],flight_one[2],flight_one[3],flight_two[2],flight_two[3],flight_one[4],flight_two[4],flight_one[5], flight_two[5], flight_one[6], flight_two[6], flight_one[7], flight_two[7]]
                combinations.append(new_route)
    return combinations

def making_triples(combinations): #creating 1+1+1 combinations from pairs (1+1)
    triples = []
    for combo_one in combinations:
        for combo_two in combinations:
            if deltas(combo_one, combo_two) and combo_one[0] != combo_two [1]:
                come = [combo_one[0], combo_one[1], combo_two[1], combo_two[2],combo_one[3],combo_two[6],combo_one[7],combo_one[8],combo_two[8],combo_one[9],combo_one[10],combo_two[10],combo_one[11],combo_one[12],combo_two[12],combo_one[13],combo_one[14],combo_two[14]]
                triples.append(come)
    return triples

def count_price_w_baggage(combination): #counting price for 1 baggage. Not counting for 2 bags - little bug - easy to fix.
    if combination[11] == "2" and combination[12] == "2":
        price = int(combination[9]) + int(combination[10]) + 2*int(combination[13]) + 2*int(combination[14])
    else:
        price = int(combination[9]) + int(combination[10]) + int(combination[13]) + int(combination[14])
    return price

def count_price(combination): #counting price for 0 baggage
    price = int(combination[9]) + int(combination[10])
    return price

def count_triples_w_baggage(combination): #counting price for 1 baggage. Not counting for 2 bags - little bug - easy to fix.
    if combination[12] == "2" and combination[13] == "2" and combination[14] == "2":
        price = int(combination[9]) + int(combination[10]) + int(combination[11]) + 2 * int(combination[15]) + 2 * int(combination[16]) + 2 * int(combination[17])
    else:
        price = int(combination[9]) + int(combination[10]) + int(combination[11]) + int(combination[15]) + int(combination[16]) + int(combination[17])
    return price


def count_triples(combination): #counting price for 0 baggage
    price = int(combination[9]) + int(combination[10]) + int(combination[11])
    return price

def format_pairs(combinations, baggage): #formatting pair combos (1+1) to be ready for csv = final outcome - src, sto, dst, flight1, flight2, dep_time, arr_time, duration, bags, price
    result = []
    for combination in combinations:
        src = combination[0]
        sto = combination[1]
        dst = combination[2]
        flight1 = combination[7]
        flight2 = combination[8]
        dep_time = combination[3]
        arr_time = combination[6]
        t1 = dt.datetime.strptime(combination[3], '%Y-%m-%dT%H:%M:%S')
        t2 = dt.datetime.strptime(combination[6], '%Y-%m-%dT%H:%M:%S')
        delta = t2 - t1
        h = delta.total_seconds() // 3600
        m = (delta.total_seconds() % 3600) // 60
        duration = "%d:%d" % (h, m)
        bags = baggage
        if baggage == 0:
            price = count_price(combination)
        else:
            price = count_price_w_baggage(combination)
        data = src, sto, dst, flight1, flight2, dep_time, arr_time, duration, bags, price
        result.append(list(data))
    return result

def format_triples(combinations, baggage): #formatting triple combos (1+1+1) to be ready for csv = final outcome - src, sto, sto1, dst, flight1, flight2, flight3, dep_time, arr_time, duration, bags, price
    result = []
    for combination in combinations:
        src = combination[0]
        sto = combination[1]
        sto1 = combination[2]
        dst = combination[3]
        flight1 = combination[6]
        flight2 = combination[7]
        flight3 = combination[8]
        dep_time = combination[4]
        arr_time = combination[5]
        t1 = dt.datetime.strptime(combination[4], '%Y-%m-%dT%H:%M:%S')
        t2 = dt.datetime.strptime(combination[5], '%Y-%m-%dT%H:%M:%S')
        delta = t2 - t1
        h = delta.total_seconds() // 3600
        m = (delta.total_seconds() % 3600) // 60
        duration = "%d:%d" % (h, m)
        bags = baggage
        if baggage == 0:
            price = count_triples(combination)
        else:
            price = count_triples_w_baggage(combination)
        data = src, sto, sto1, dst, flight1, flight2, flight3, dep_time, arr_time, duration, bags, price
        result.append(list(data))
    return result




