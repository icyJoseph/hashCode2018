import math

filename = "e_high_bonus.in"


def print_output(filename, rides):
    outputname = filename.split('.')
    output_file = open(outputname[0]+'.out', 'w')
    for vehicle in rides:
        s = str(len(vehicle))
        for ride in vehicle:
            s = s+' ' + str(ride['ride_number'])
        output_file.write(s)
        output_file.write('\n')
    output_file.close()


def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def choose_destinations(destinations, limit, overload):
    step = 0
    start = [0, 0]
    rides = []
    flag = True
    while step <= limit and flag:
        progress = "simulation progress " + \
            str(step)+" with "+str(len(destinations))+" left"
        print(progress)
        doable_destinations = [destination for destination in destinations if doable_destination(
            destination, start, step, limit)]
        print("doable_destinations: "+str(len(doable_destinations)))
        if(len(doable_destinations) > 1):
            startable_destinations = [
                destination for destination in doable_destinations if startable_destination(destination, start, step)]
            print("startable_destinations: "+str(len(startable_destinations)))
            if(len(startable_destinations) > 1):
                closest = closest_destination(
                    startable_destinations, start)
                print("closest destination "+str(closest))
                step = step + closest["distance"] + \
                    distance(start, closest['start_point'])
                start = closest["end_point"]
                rides.append(closest)
                destinations.remove(closest)
            else:
                reasonable_destination = doable_destinations[0]
                step = step + reasonable_destination["distance"] + \
                    distance(start, reasonable_destination['start_point'])
                start = reasonable_destination["end_point"]
                print("reasonable destination "+str(reasonable_destination))
                rides.append(reasonable_destination)
                destinations.remove(reasonable_destination)
        else:
            better_than_nothing = destinations[0]
            step += better_than_nothing["distance"] + \
                distance(start, better_than_nothing['start_point'])
            start = better_than_nothing["end_point"]
            rides.append(better_than_nothing)
            print("just a destination "+str(better_than_nothing))
            destinations.remove(better_than_nothing)
        if len(rides) >= overload:
            flag = False
            break
    return rides, destinations


def doable_destination(destination, start, step, limit):
    return step + distance(destination["start_point"], start) + destination["distance"] < limit


def startable_destination(destination, start, step):
    return step + distance(destination["start_point"], start) >= destination['start_time']


def closest_destination(destinations, start):
    min_distance = 0
    distances_to_start = [distance(start, destination["start_point"])
                          for destination in destinations]
    min_distance = min(distances_to_start)
    return [destination for destination in destinations if distance(start, destination["start_point"]) == min_distance][0]


with open(filename) as file:
    input = file.readlines()
    inputArr = [i.replace("\n", "").split() for i in input]
    rows, columns, vehicles, number_of_rides, bonus, steps = [
        int(par) for par in inputArr[0]]
    individual_rides = inputArr[1:]
    destinations = []
    i = 0
    for ride in individual_rides:
        start_x, start_y, end_x, end_y, start_time, end_time = [
            int(par) for par in ride]
        destinations.append({
            'start_point': [start_x, start_y],
            'end_point': [end_x, end_y],
            'start_time': start_time,
            'end_time': end_time,
            'ride_number': i,
            'wiggle': end_time - start_time,
            'distance': abs(start_x - end_x) + abs(start_y - end_y)
        })
        i = i+1
    #sorted_destinations = sorted(destinations, key=lambda k: k['start_point'])
    rides = []
    # run simulation
    overload = math.floor(number_of_rides / vehicles)
    for vehicle in range(0, vehicles):
        progress = "processing vehicle number: "+str(vehicle)
        print(progress)
        ride, destinations = choose_destinations(
            destinations, steps, overload)
        rides.append(ride)
    result = str(vehicles) + ' vehicles assigned to ' + str(len(rides)) + ' rides ' + \
        'with ' + str(len(destinations)) + ' destinations left unused'
    print(result)
    print_output(filename, rides)
