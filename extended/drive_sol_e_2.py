import math

filename = "e_high_bonus.in"
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


def compose(destination, start, key='start_point'):
    return distance(destination['end_point'], start)


def choose_destinations(destinations, limit, overload, bonus):
    step = 0
    start = [0, 0]
    rides = []
    flag = True
    finishable = 0
    close = 0
    reasonable = 0
    points = 0
    on_time = 0
    error = 0
    while step <= limit and flag:
        doable_destinations = [destination for destination in destinations if doable_destination(
            destination, start, step, limit)]
        if(len(doable_destinations) > 0):
            # earliest = closest_destination(
            #     doable_destinations, start)
            sorted_by_start_time = sorted(
                doable_destinations, key=lambda k: distance(k['start_point'], start))
            # sorted_by_start_point = sorted(
            #     sorted_by_start_time, key=lambda k: k['start_point'])
            # sorted_by_distance = sorted(
            #     sorted_by_start_point, key=lambda k: k['distance'])
            earliest = greatest_distance(sorted_by_start_time, start)
            if step + distance(start, earliest['start_point']) <= earliest['start_time']:
                print("Will start on time")
                on_time += 1
                points += bonus
            if step + distance(start, earliest['start_point']) <= earliest['start_time']:
                # Will have to wait and then be free at 'start_time' + distance
                step = earliest['start_time'] + earliest['distance']
            elif step + distance(start, earliest['start_point']) > earliest['start_time']:
                # late to the party, start right away and finish at step + distance + time to get to start
                step = step + distance(
                    start, earliest['start_point']) + earliest['distance']
            finishable += 1

            # the ones we can finish on time add points
            points += earliest['distance']
            rides.append(earliest)
            destinations.remove(earliest)
        else:
            break

        if(step > limit):
            print("WRONG")
        # if len(rides) > overload:
        #     flag = False
        #     break
    return rides, destinations, step, finishable, close, reasonable, points, on_time, error


# Given the current step, is it posible to travel to the start point and then to the end before the simulation ends
def doable_destination(destination, start, step, limit):
    can_be_finished_before_end_time = step + \
        distance(start, destination["start_point"]) + \
        destination["distance"] <= destination['end_time']

    can_be_done_on_time = step + \
        distance(start, destination['start_point']
                 ) + destination['distance'] <= limit
    return can_be_done_on_time and can_be_finished_before_end_time


# Check if the ride can be finished before its own specified end_time
def finishable_destination(destination, start, step):
    return step + distance(start, destination['start_point'])+destination["distance"] <= destination["end_time"]


def earliest_destination(destinations, start):
    start_times = [destination['start_time'] for destination in destinations]
    earliest = min(start_times)
    earliest_destinations = [
        destination for destination in destinations if destination['start_time'] == earliest]
    return shortest_distance(earliest_destinations, start)


def greatest_distance(destinations, start):
    distances = [destination['distance'] for destination in destinations]
    max_distance = max(distances)
    greatest = [
        destination for destination in destinations if destination['distance'] == max_distance]
    return earliest_finish(greatest, start)


def shortest_distance(destinations, start):
    distances = [destination['distance'] for destination in destinations]
    min_distance = min(distances)
    shortest = [
        destination for destination in destinations if destination['distance'] == min_distance]
    return earliest_finish(shortest, start)


def earliest_finish(destinations, start):
    end_times = [destination['end_time'] for destination in destinations]
    min_end_time = min(end_times)
    early_finish = [
        destination for destination in destinations if destination['end_time'] == min_end_time]
    answer = sorted(early_finish, key=lambda k: distance(
        start, k['start_point']))
    return answer[0]


def closest_destination(destinations, start, flag=False):
    distances_to_start = [distance(start, destination["start_point"])
                          for destination in destinations]
    min_distance = min(distances_to_start)
    closest = [destination for destination in destinations if distance(
        start, destination["start_point"]) == min_distance]
    return earliest_destination(closest, start)


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
    # sorted_destinations = sorted(destinations, key=lambda k: k['distance'])
    # run simulation
    overload = math.floor(number_of_rides / vehicles)
    for vehicle in range(0, vehicles):
        progress = "Processing vehicle number: "+str(vehicle)
        print(progress)
        ride, destinations, step_end, f, c, r, points, on_time, error = choose_destinations(
            destinations, steps, overload, bonus)
        score += points
        err += error
        accurate += on_time
        rides.append(ride)
        stats = "Result finished in " + \
            str(step_end) + " f: " + str(f) + " c: " + str(c) + " r: " + str(r)
        print(stats)
    result = str(vehicles) + ' vehicles assigned to ' + str(len(rides)) + ' rides ' + \
        'with ' + str(len(destinations)) + ' destinations left unused'

    print(result)
    print("Total score: "+str(score))
    print("Started on time: "+str(accurate))
    print("Error: "+str(err))
    print_output(filename, rides)
