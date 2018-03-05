import math

filename = "c_no_hurry.in"
score = 0


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


def choose_destinations(destinations, limit, bonus):
    step = 0
    start = [0, 0]
    rides = []
    flag = True
    finishable = 0
    points = 0
    on_time = 0
    error = 0
    while step <= limit and flag:
        doable_destinations = [destination for destination in destinations if doable_destination(
            destination, start, step, limit)]
        if(len(doable_destinations) > 0):
            closest = closest_destination(
                doable_destinations, start)
            if step + distance(start, closest['start_point']) <= closest['start_time']:
                #print("Will start on time")
                on_time += 1
                points += bonus
            if step + distance(start, closest['start_point']) <= closest['start_time']:
                # Will have to wait and then be free at 'start_time' + distance
                step = closest['start_time'] + closest['distance']
            elif step + distance(start, closest['start_point']) > closest['start_time']:
                # late to the party, start right away and finish at step + distance + time to get to start
                step = step + distance(
                    start, closest['start_point']) + closest['distance']
            finishable += 1
            start = closest['end_point']
            # the ones we can finish on time add points
            points += closest['distance']
            rides.append(closest)
            destinations.remove(closest)
        else:
            break
    return rides, destinations, step, finishable, points, on_time, error


# Given the current step, is it posible to travel to the start point and then to the end before the simulation ends
def doable_destination(destination, start, step, limit):
    can_be_finished_before_end_time = step + \
        distance(start, destination["start_point"]) + \
        destination["distance"] <= destination['end_time']

    can_be_done_on_time = step + \
        distance(start, destination['start_point']
                 ) + destination['distance'] <= limit

    return can_be_done_on_time and can_be_finished_before_end_time


def closest_destination(destinations, start):
    min_distance = 0
    distances_to_start = [distance(start, destination["start_point"])
                          for destination in destinations]
    min_distance = min(distances_to_start)
    return [destination for destination in destinations if distance(start, destination["start_point"]) == min_distance][0]


# Main loop
with open(filename) as file:
    input = file.readlines()
    inputArr = [i.replace("\n", "").split() for i in input]
    rows, columns, vehicles, number_of_rides, bonus, steps = [
        int(par) for par in inputArr[0]]
    individual_rides = inputArr[1:]
    destinations = []
    accurate = 0
    i = 0
    err = 0
    for ride in individual_rides:
        start_x, start_y, end_x, end_y, start_time, end_time = [
            int(par) for par in ride]
        destinations.append({
            'start_point': [start_x, start_y],
            'end_point': [end_x, end_y],
            'start_time': start_time,
            'end_time': end_time,
            'ride_number': i,
            'distance': abs(start_x - end_x) + abs(start_y - end_y)
        })
        i = i+1
    rides = []
    ride_points = [destination['distance'] for destination in destinations]
    total_points = sum(ride_points) + bonus * number_of_rides
    print("TOTAL possible points :" + str(total_points))
    # run simulation
    overload = math.floor(number_of_rides / vehicles)
    for vehicle in range(0, vehicles):
        progress = "Processing vehicle number: "+str(vehicle)
        print(progress)
        ride, destinations, step_end, f, points, on_time, error = choose_destinations(
            destinations, steps, bonus)
        score += points
        err += error
        accurate += on_time
        rides.append(ride)
        stats = "Result finished in " + \
            str(step_end) + " f: " + str(f)
        print(stats)
    result = str(vehicles) + ' vehicles assigned to ' + str(len(rides)) + ' rides ' + \
        'with ' + str(len(destinations)) + ' destinations left unused'

    print(result)
    print("TOTAL possible points :" + str(total_points))
    print("Total score: "+str(score))
    print("Started on time: "+str(accurate))
    print("Error: "+str(err))
    print_output(filename, rides)
