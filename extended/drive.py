import math

filename = "b_should_be_easy.in"


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


def compose(destination, start, key='start_point'):
    return distance(destination['end_point'], start)


def choose_destinations(destinations, limit, overload):
    step = 0
    start = [0, 0]
    rides = []
    flag = True
    counter_reasonables = 0
    counter_forced = 0
    counter_closests = 0
    while step <= limit and flag:
        startable_destinations = [
            destination for destination in destinations if startable_destination(destination, start, step)]
        if(len(startable_destinations) > 0):
            doable_destinations = [destination for destination in startable_destinations if doable_destination(
                destination, start, step, limit)]
            if(len(doable_destinations) > 0):
                earliest = closest_destination(
                    startable_destinations, start)
                counter_closests += 1
                if step + distance(start, earliest['start_point']) < earliest['start_time']:
                    step = earliest['distance'] + earliest['start_time']
                if step + distance(start, earliest['start_point']) >= earliest['start_time']:
                    step += distance(
                        start, earliest['start_point']) + earliest['distance']
                start = earliest["end_point"]
                rides.append(earliest)
                destinations.remove(earliest)
            else:
                reasonable_destination = earliest_destination(
                    startable_destinations, start)
                if step + distance(start, reasonable_destination['start_point']) < reasonable_destination['start_time']:
                    step = reasonable_destination['distance'] + \
                        reasonable_destination['start_time']
                if step + distance(start, reasonable_destination['start_point']) >= reasonable_destination['start_time']:
                    step += + distance(
                        start, reasonable_destination['start_point']) + reasonable_destination['distance']
                start = reasonable_destination["end_point"]
                counter_reasonables += 1
                rides.append(reasonable_destination)
                destinations.remove(reasonable_destination)
        else:
            break
        # else:
        #     better_than_nothing = greatest_distance(destinations, start)
        #     step += compose(better_than_nothing, start)
        #     start = better_than_nothing["end_point"]
        #     rides.append(better_than_nothing)
        #     counter_forced += 1
        #    destinations.remove(better_than_nothing)

        if(step > limit):
            print("WRONG")
        print("new step " + str(step) + " new start: " +
              str(start[0]) + ":" + str(start[1]))
        if len(rides) > 0:
            print(" start by: " + str(rides[len(rides) - 1]['start_time']) + " finish by: " + str(
                rides[len(rides) - 1]['end_time']) + " finished at: " + str(rides[len(rides) - 1]['distance'] + step))
        if len(rides) >= overload:
            flag = False
            break
    return rides, destinations, [counter_closests, counter_reasonables, counter_forced], step


# Given the current step, is it posible to travel to the start point and then to the end before the simulation ends
def doable_destination(destination, start, step, limit):
    return step + distance(start, destination["start_point"]) + destination["distance"] < destination['end_time']

# Given the current step, if we move to a start_point, will it be startable when we arrive? - NO dead time


def startable_destination(destination, start, step):
    return step + distance(start, destination["start_point"]) >= destination['start_time']


# Introduce tolerance in favor of not having to take forced rides
def waitable_destination(destination, start, step, tolerance):
    return step + distance(start, destination["start_point"]) + tolerance == destination['start_time']


def earliest_destination(destinations, start):
    start_times = [destination['start_time'] for destination in destinations]
    earliest = min(start_times)
    earliest_destinations = [
        destination for destination in destinations if destination['start_time'] == earliest]
    if len(earliest_destinations) > 0:
        return greatest_distance(earliest_destinations, start)
    return earliest_destinations[0]


def greatest_distance(destinations, start):
    distances = [destination['distance'] for destination in destinations]
    max_distance = max(distances)
    greatest = [
        destination for destination in destinations if destination['distance'] == max_distance]
    if (len(greatest) > 1):
        return closest_destination(greatest, start, True)
    return greatest[0]


def closest_destination(destinations, start, flag=False):
    min_distance = 0
    distances_to_start = [distance(start, destination["start_point"])
                          for destination in destinations]
    min_distance = min(distances_to_start)
    closest = [destination for destination in destinations if distance(
        start, destination["start_point"]) == min_distance]
    if (len(closest) > 1):
        if(flag):
            lowest_end_point = min([destination['end_point']
                                    for destination in closest])
            return [destination for destination in closest if destination['end_point'] == lowest_end_point][0]
        return greatest_distance(closest, start)
    return closest[0]


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
    rides = []
    # run simulation
    overload = math.floor(number_of_rides / vehicles)
    for vehicle in range(0, vehicles):
        progress = "Processing vehicle number: "+str(vehicle)
        print(progress)
        ride, destinations, [closest, reasonable, forced], step_end = choose_destinations(
            destinations, steps, overload)
        rides.append(ride)
        stats = "Result: \n closest: " + str(closest) + " reasonable: " + \
            str(reasonable)+" forced: "+str(forced) + \
            " finished in "+str(step_end)
        print(stats)
    result = str(vehicles) + ' vehicles assigned to ' + str(len(rides)) + ' rides ' + \
        'with ' + str(len(destinations)) + ' destinations left unused'
    print(result)
    print_output(filename, rides)
