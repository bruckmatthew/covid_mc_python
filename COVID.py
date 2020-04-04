import matplotlib.pyplot as plt
import random
import time

#if 1, then infected. If 0, not indected
time1 = time.time()
#GLOBAL CONSTANTS
number_days = 50
n_people = 20
starting_percent_infected = 0.2
infectious_rate = 0.2
interaction_per_day = round(1*n_people)
dropout_rate = 0.05
n_iterations = 20
recovery_lower_bound = 5
recovery_high_bound = 10

def to_recovery(lowest, highest):
    return random.randint(lowest,highest)

def will_infect(infectious_rate):
    if random.random() < infectious_rate:
        return 1
    else:
        return 0

def will_die(dropout_rate):
    if random.random() < dropout_rate:
        return -1
    else:
        return 1

def pick_random_person(population):
    return random.randint(0,population-1)
    

def interaction(people,n_people,infectious_rate):
    #pick two people to simulate an interaction. Try and predict what the outcome would be. 
    first_person_index = pick_random_person(n_people)
    second_person_index = pick_random_person(n_people)
    human1 = people[first_person_index]
    human2 = people[second_person_index]
    #Result of interation must be a function of the infectious rate
    #if a 0 and 0 meet result is always 0
    #if both are 1, then both stay as 1
    # if a 1 and 0 meet, the 1 stays as a 1; and the 0 might be converted to a 1
    if human1 != human2:
        if human1 == 0:
            human1 = will_infect(infectious_rate)
            people[first_person_index] = human1
        elif human2 == 0:
            human2 = will_infect(infectious_rate)
            people[second_person_index] = human2
    
def percent_infected(people):
    infected = people.count(1)
    healthy = people.count(0)
    if healthy == 0:
        return 1
    else:
        return infected/(healthy+infected)

def daily_interactions(people,interaction_per_day,n_people,infectious_rate):
    for i in range(interaction_per_day):
        interaction(people,n_people,infectious_rate)

def daily_counter(days_infected,people,days_to_recovery,day):
    if len(days_infected) == len(people):
        for i in range(len(people)-1):
            if people[i] == 1:
                days_infected[i] += 1
            if days_infected[i] > days_to_recovery:
                days_infected[i] = 0
                people[i] = 0
                #print("someone recovered")
    else:
        print("ERROR with day counter")

def mortality(people, dropout_rate):
    for i in range(len(people)-1):
        if people[i] == 1 and will_die(dropout_rate) == -1:
            people[i] = -1
            #print("someone died")
            

def days(days_infected,people,number_days,interaction_per_day,n_people,infectious_rate):
    per_infected_on_each_day = []
    days_to_recovery = to_recovery(recovery_lower_bound,recovery_high_bound)
    for i in range(number_days):
        daily_interactions(people,interaction_per_day,n_people,infectious_rate)
        daily_counter(days_infected,people,days_to_recovery,i)
        mortality(people, dropout_rate)
        per_infected_on_each_day.append(percent_infected(people))
    return per_infected_on_each_day

def iterations(n_iterations,starting_percent_infected,number_days,interaction_per_day,n_people,infectious_rate):
    #Create population list
    #For each person, simulate an interation
    #Set starting population
    for n in range(n_iterations):
        infected_number = round(n_people*starting_percent_infected)
        people= []
        days_infected = [0] * n_people
        for i in range(n_people):
            if i < infected_number:
                people.append(1)
            else:
                people.append(0)
        each_iter = days(days_infected,people,number_days,interaction_per_day,n_people,infectious_rate)
        each_day = list(range(0, number_days))
        plt.plot(each_day,each_iter)


iterations(n_iterations,starting_percent_infected,number_days,interaction_per_day,n_people,infectious_rate)
time2 = time.time()
print(time2 - time1)
plt.show()
