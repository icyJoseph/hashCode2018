import math

filename = "d_metropolis.in"
score = 0


def calculate_center_of_mass(destinations):
    center_gravity_x = sum([destination['start_point'][0]
                            for destination in destinations]) / len(destinations)
    center_gravity_y = sum([destination['start_point'][1]
                            for destination in destinations]) / len(destinations)
    return [center_gravity_x, center_gravity_y]

# Given a list of destinations, a limit, an overload per vehicle and a bonus for starting trips on time
# Return the most effective set of destinations per vehicle


def choose_destinations(destinations, limit, bonus, avg):
    step = 0
    start = [0, 0]
    rides = []
    flag = True
    finishable = 0
    points = 0
    on_time = 0
    error = 0
    while step <= limit and flag:
        center_of_mass = calculate_center_of_mass(destinations)
        doable_destinations = [destination for destination in destinations if doable_destination(
            destination, start, step, limit)]
        if(len(doable_destinations) > 0):
            rides_with_bonus = on_start_on_time(
                doable_destinations, start, step)
            if (len(rides_with_bonus) == 0):
                earliest = earliest_destination(
                    doable_destinations, start, center_of_mass, step, avg)
            else:
                earliest = shortest_connection(
                    rides_with_bonus, start, center_of_mass, step, avg)
            if step + distance(start, earliest['start_point']) <= earliest['start_time']:
                # print("Will start on time")
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
            start = earliest['end_point']
            # the ones we can finish on time add points
            points += earliest['distance']
            rides.append(earliest)
            destinations.remove(earliest)
        else:
            break
    return rides, destinations, step, finishable, points, on_time, error


# Print Result
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


# Retun the distance between point A and B
def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


# Given the current step, is it posible to travel to the start point and then to the end before the simulation ends
def doable_destination(destination, start, step, limit):
    can_be_finished_before_end_time = step + \
        distance(start, destination["start_point"]) + \
        destination["distance"] <= destination['end_time']

    can_be_done_on_time = step + \
        distance(start, destination['start_point']
                 ) + destination['distance'] <= limit
    return can_be_done_on_time and can_be_finished_before_end_time


# Return the destination with the smallest start_time, and greatest distance
def earliest_destination(destinations, start, center_of_mass, step, avg):
    start_times = [destination['start_time'] for destination in destinations]
    earliest = min(start_times)
    earliest_destinations = [
        destination for destination in destinations if destination['start_time'] == earliest]
    return shortest_connection(earliest_destinations, start, center_of_mass, step, avg)


# shortest connections
def shortest_connection(destinations, start, center_of_mass, step, avg):
    average = average_destinations(
        destinations, start, center_of_mass, step, avg)
    return sorted(average, key=lambda k: distance(start, k['start_point']))[0]


# Return an average destination
def average_destinations(destinations, start, center_of_mass, step, avg):
    factor = 0
    average = [destination for destination in destinations if destination['distance']
               >= avg * (1.8 - factor) and destination['distance'] <= (1.8 - factor) * avg]
    while len(average) == 0:
        factor += 0.1
        average = [destination for destination in destinations if destination['distance']
                   >= avg * (1.8 - factor) and destination['distance'] <= (1.8 + factor) * avg]
    return average

# Return the destination with the greatest distance and earliest finish


def greatest_distance(destinations, start, center_of_mass, step, avg):
    # distances = sorted(destinations, key=lambda k: k['distance'], reverse=True)
    # return distances[0]
    # distances = [destination['distance'] for destination in destinations]
    # max_distance = max(distances)
    factor = 1.5
    greatest = [
        destination for destination in destinations if destination['distance'] >= factor * avg]
    while len(greatest) == 0:
        factor = factor - 0.01
        greatest = [
            destination for destination in destinations if destination['distance'] >= factor * avg]
    # return closest_destination(greatest, start, center_of_mass, step, avg)
    return greatest


# Return the destination with the shortest distance and earliest finish
def shortest_distance(destinations, start, step):
    distances = sorted(destinations, key=lambda k: k['distance'])
    return distances[0]
    # on_time = on_start_on_time(destinations, start, step)
    # if (len(on_time) > 0):
    #     return on_time[0]
    # answer = sorted(destinations, key=lambda k: distance(
    #     start, k['start_point']))
    # return answer[0]


# Return the destination with the earliest finish
def earliest_finish(destinations, start, center_of_mass, step):
    # on_time = on_start_on_time(destinations, start, step)
    # if (len(on_time) > 0):
    #     return on_time[0]
    # earliest_end_time = sorted(destinations, key=lambda k: k['end_time'])
    # # return earliest_end_time[0]
    # on_time = on_start_on_time(destinations, start, step)
    # if (len(on_time) > 0):
    #     return on_time[0]
    # answer = sorted(destinations, key=lambda k: k['end_time'])
    # return answer[0]
    distances_to_center_of_mass = [distance(center_of_mass, destination["end_point"])
                                   for destination in destinations]
    min_distance = min(distances_to_center_of_mass)
    closest = [destination for destination in destinations if distance(
        center_of_mass, destination["end_point"]) == min_distance]
    answer = sorted(closest, key=lambda k: k['distance'], reverse=True)
    return answer[0]


# Return destinations that can be started with bonus
def on_start_on_time(destinations, start, step):
    on_time = [destination for destination in destinations if (
        step + distance(start, destination['start_point']) <= destination['start_time'])]
    return on_time


# Return distances closest to the the start point and greatest distance
def closest_destination(destinations, start, center_of_mass, step, avg):
    distances_to_start = [distance(start, destination["start_point"])
                          for destination in destinations]
    min_distance = min(distances_to_start)
    closest = [destination for destination in destinations if distance(
        start, destination["start_point"]) == min_distance]
    return earliest_finish(closest, start, center_of_mass, step)


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

    center_gravity_x = sum([destination['start_point'][0]
                            for destination in destinations]) / len(destinations)
    center_gravity_y = sum([destination['start_point'][1]
                            for destination in destinations]) / len(destinations)
    center_gravity = [center_gravity_x, center_gravity_y]

    overload = math.floor(number_of_rides / vehicles)
    avg_distance = sum([destination['distance']
                        for destination in destinations]) / (number_of_rides)
    print("AVG Points per ride: " + str(avg_distance))
    avg_vehicle = sum([destination['distance']
                       for destination in destinations]) / (vehicles)
    print("AVG Points per vehicle: " + str(avg_vehicle))
    # run simulation
    for vehicle in range(0, vehicles):
        progress = "Processing vehicle number: "+str(vehicle)
        print(progress)
        ride, destinations, step_end, f, points, on_time, error = choose_destinations(
            destinations, steps, bonus, avg_distance)
        score += points
        print("PARTIAL SCORE " + str(score) + " added with: "+str(points))
        err += error
        accurate += on_time
        rides.append({'ride': ride,
                      'points': points})
        stats = "Result finished in " + str(step_end) + " f: " + str(f)
        print(stats)

    print("TOTAL possible points :" + str(total_points))
    print("Total score: "+str(score))
    print("Started on time: "+str(accurate))
    print("Error: "+str(err))

    extra_score = 0
    should_continue = True
    if len(destinations) != 0:
        while len(destinations) > 0 and should_continue:
            partial_len = len(destinations)
            extra_ride, destinations, extra_step_end, extra_f, extra_points, extra_on_time, extra_error = choose_destinations(
                destinations, steps, bonus, avg_distance)
            if len(destinations) == partial_len or extra_points == 0:
                should_continue = False
            else:
                rides.append({'ride': extra_ride, 'points': extra_points})
            extra_score += extra_points
    print("Extra_score: " + str(extra_score))

    best_rides = sorted(rides, key=lambda k: k['points'], reverse=True)

    # Calculate final score
    final_score = 0
    for vehicle in range(0, vehicles):
        final_score += best_rides[vehicle]['points']
    print("Final Score: " + str(final_score))

    final_rides = [ride['ride'] for ride in best_rides][:vehicles]

    print(str(vehicles) + ' vehicles assigned to ' + str(len(final_rides)) +
          ' rides with ' + str(len(destinations)) + ' destinations left unused')

    print("Mass Center : [" +
          str(center_gravity[0]) + "," + str(center_gravity[1])+"]")
    print_output(filename, final_rides)
