import random, time
def test(function, expected_result, *inputs):
    result = function(*inputs)
    print(result, expected_result, sep='\n\n\n')
    return result == expected_result

def get_first_element(iterable):
    return iterable[0]

def deep_b_search(left_index : int, right_index : int, iterable, target, key):
    """
    Does a binary search of the iterable. If the target is found, it will return the index of the last occurrence of the target in the iterable.
    If the target is not found, the function will return the index of the first occurrence of the smallest value that is bigger than the target.
    """
    if not iterable[left_index:right_index]:
        #If we come to a point that there's no more options available:
        if iterable:
            left_index -= 1
        return left_index
    middle =  ((right_index - left_index) //2) + left_index
    # if key == None:
    #     def key(value):
    #         return int(value)
    middle_value = key(iterable[middle]) 
    if middle_value == target:
        #Move to the right until we find the last occurrence of the target
        while middle_value == target and middle < right_index-1:
            middle_value = key(iterable[middle +1])
            if middle_value == target:
                middle +=1
        return middle
    elif middle_value < target:
        left_index = middle +1
    else:
        right_index = middle

    return deep_b_search(left_index, right_index, iterable, target, key)
def b_search(left_index : int, right_index : int, iterable, target, key):
    if not iterable[left_index:right_index]:
        return None
    middle =  ((right_index - left_index) //2) + left_index
    # if key: middle_value = key(iterable[middle]) 
    # else: middle_value = iterable[middle]
    middle_value = key(iterable[middle]) 
    if middle_value == target:
        return middle
    elif middle_value < target:
        left_index = middle +1
    else:
        right_index = middle 

    return b_search(left_index, right_index, iterable, target, key)

def get_second_element_as_int(iterable):
    return int(iterable[1])

def binary_search(iterable, target, key= int, uptoLast= False):

    if uptoLast:
        return deep_b_search(0, len(iterable), iterable, target, key)
    else:
        return b_search(0,len(iterable), iterable, target, key)

def add_friends_from_queue(queue : list[str],network : list[tuple[int, list[int]]], reverse = False) -> None:
    tmp_user = int(queue[0][1 - int(reverse)])
    tmp_friends = []
    looping = True
    while queue and looping:
        if int(queue[0][1 - int(reverse)]) == tmp_user:
            tmp_friends.append(int(queue.pop(0)[0 + int(reverse)]))
        else: looping = False
    destination = binary_search(network, tmp_user, key=get_first_element, uptoLast=True)
    network.insert(destination +1,(tmp_user, tmp_friends))
    
        
    

def create_network(file_name : str) -> list[tuple[int, list[int]]]:
    '''(str)->list of tuples where each tuple has 2 elements the first is int and the second is list of int

    Precondition: file_name has data on social netowrk. In particular:
    The first line in the file contains the number of users in the social network
    Each line that follows has two numbers. The first is a user ID (int) in the social network,
    the second is the ID of his/her friend.
    The friendship is only listed once with the user ID always being smaller than friend ID.
    For example, if 7 and 50 are friends there is a line in the file with 7 50 entry, but there is line 50 7.
    There is no user without a friend
    Users sorted by ID, friends of each user are sorted by ID
    Returns the 2D list representing the friendship nework as described above
    where the network is sorted by the ID and each list of int (in a tuple) is sorted (i.e. each list of friens is sorted).
    '''
    #From multiple tests, I realized my function can process huge.txt in 5 seconds!
    start_time = time.time()
    friends = (x.split() for x in open(file_name).read().splitlines())
    network=[]
    print(f"time elapsed: {time.time() - start_time}")
    # YOUR CODE GOES HERE
    start_time = time.time()
    network_lenght : int = friends.__next__()
    current_user : int = -1
    current_friends : list = []
    current_queue : list = []
    queue = []
    for connection  in friends:
        #If the user changed then update the current user variable
        #The goal is to only push the network on new users
        if int(connection[0]) > current_user:

            #First add the friends we found along the way
            if current_friends:
                network.append((current_user, current_friends))

            current_user : int = int(connection[0])
            current_friends : list[int] = []

            #If there is a current queue (from the previous user)
            if current_queue:
                queue.extend(current_queue)
                current_queue : list = []
                queue.sort(key=get_second_element_as_int)
            #Then unload the queue
            if queue:
                active_in_queue : bool = True
                while active_in_queue:
                    if int(queue[0][1]) <= current_user:
                        if int(queue[0][1]) == current_user:
                            current_friends.append(int(queue.pop(0)[0]))

                        else:
                            add_friends_from_queue(queue, network)
                            
                    else : active_in_queue = False
                    if not queue: active_in_queue = False


                    



        current_friends.append(int(connection[1]))
        current_queue.append(connection)
    if current_friends:
        network.append((current_user, current_friends))
        current_friends : list[int] = []
    #I had forgotten to add the queue from the last user to the definite queue
    if current_queue:
                queue.extend(current_queue)
                current_queue : list = []
                queue.sort(key=get_second_element_as_int)

    for reverse_connection in queue:
        if int(reverse_connection[1]) > current_user:
            if current_friends:
                network.append((current_user, current_friends))
            current_user : int = int(reverse_connection[1])
            current_friends : list[int] = []
        
        current_friends.append(int(reverse_connection[0]))

    network.append((current_user, current_friends))
    #debug printing
    # print(f"Queue: {queue}, Network: {network}, Current user: {current_user}, Current friends: {current_friends}, Current queue: {current_queue}, Network length: {network_lenght}", end=" \n\n")
    # print(queue)
    print(f"time elapsed: {time.time() - start_time}")
    return network

def getCommonFriends(user1 : int, user2 : int, network : list[tuple[int, list[int]]]) -> list:
    '''(int, int, 2D list) ->list
    Precondition: user1 and user2 IDs in the network. 2D list sorted by the IDs, 
    and friends of user 1 and user 2 sorted 
    Given a 2D-list for friendship network, returns the sorted list of common friends of user1 and user2
    '''
    common=[]
    
    # YOUR CODE GOES HERE
    user1_friends = network[binary_search(network, user1, key=get_first_element)][1]
    user2_friends = network[binary_search(network, user2, key=get_first_element)][1]

    left_pointer = 0
    right_pointer = 0
    #Using pointers akin to mergersort in order to solve easily in log(n) + k1 + k2 time as the bonus asks
    while left_pointer < len(user1_friends) and right_pointer < len(user2_friends):
        if user1_friends[left_pointer] == user2_friends[right_pointer]:
            common.append(user1_friends[left_pointer])
            left_pointer += 1
            right_pointer += 1
        elif user1_friends[left_pointer] < user2_friends[right_pointer]:
            left_pointer += 1
        else:
            right_pointer += 1

    return common

    
def recommend(user, network : list[tuple[int, list[int]]]) -> int | None:
    '''(int, 2Dlist)->int or None
    Given a 2D-list for friendship network, returns None if there is no other person
    who has at least one neighbour in common with the given user and who the user does
    not know already.
    
    Otherwise it returns the ID of the recommended friend. A recommended friend is a person
    you are not already friends with and with whom you have the most friends in common in the whole network.
    If there is more than one person with whom you have the maximum number of friends in common
    return the one with the smallest ID. '''

    # YOUR CODE GOES HERE
    pass

    


def k_or_more_friends(network : list[tuple[int, list[int]]], k : int) -> int:
    '''(2Dlist,int)->int
    Given a 2D-list for friendship network and non-negative integer k,
    returns the number of users who have at least k friends in the network
    Precondition: k is non-negative'''
    # YOUR CODE GOES HERE
    pass
 

def maximum_num_friends(network : list[tuple[int, list[int]]]) -> int:
    '''(2Dlist)->int
    Given a 2D-list for friendship network,
    returns the maximum number of friends any user in the network has.
    '''
    # YOUR CODE GOES HERE
    pass
    

def people_with_most_friends(network : list[tuple[int, list[int]]]) -> list[int]:
    '''(2Dlist)->1D list
    Given a 2D-list for friendship network, returns a list of people (IDs) who have the most friends in network.'''
    max_friends=[]
    # YOUR CODE GOES HERE
    return    max_friends


def average_num_friends(network : list[tuple[int, list[int]]]) -> float:
    '''(2Dlist)->number
    Returns an average number of friends overs all users in the network'''

    # YOUR CODE GOES HERE
    pass
    

def knows_everyone(network : list[tuple[int, list[int]]]) ->bool:
    '''(2Dlist)->bool
    Given a 2D-list for friendship network,
    returns True if there is a user in the network who knows everyone
    and False otherwise'''
    
    # YOUR CODE GOES HERE
    pass


####### CHATTING WITH USER CODE:

def is_valid_file_name() -> None | str:
    '''None->str or None'''
    file_name = None
    try:
        file_name=input("Enter the name of the file: ").strip()
        f=open(file_name)
        f.close()
    except FileNotFoundError:
        print("There is no file with that name. Try again.")
        file_name=None
    return file_name 

def get_file_name() -> str:
    '''()->str
    Keeps on asking for a file name that exists in the current folder,
    until it succeeds in getting a valid file name.
    Once it succeeds, it returns a string containing that file name'''
    file_name=None
    while file_name==None:
        file_name=is_valid_file_name()
    return file_name

def get_input_inrange(min : int, max : int, message : str = "") -> int:
    '''(int,int)->int
    Returns an int between min (inclusive) and max (inclusive).
    Keeps on asking for input until it is within min and max.
    Note that input returns a str so type casting is necessary
    '''
    custom_input = bool(message)
    smooth_run = False
    while not smooth_run:
        try:
            input_value = int(input("Enter an integer : \n" if not custom_input else message).strip())
            if min <= input_value <= max:
                smooth_run = True
            else:
                print(f"That number is out of range. Please try again.")
        except ValueError:
            print(f"That was not an integer. Please try again.")

    return input_value

def get_uid(network : list[tuple[int, list[int]]]) -> int:
    '''(2Dlist)->int
    Keeps on asking for a user ID that exists in the network
    until it succeeds. Then it returns it'''
    
    # YOUR CODE GOES HERE
    user_found = False
    while not user_found:
        uid = get_input_inrange(0, network[-1][0], f"Enter a user ID, the biggest one is {network[-1][0]}: ")
        if binary_search(network, uid, key=get_first_element) != None:
            user_found = True
        else:
            print("That user ID does not exist. Try again.")
    return uid
    
def tests():
    files = ["net1.txt", "net2.txt", "net3.txt", "huge.txt", "big.txt"]
    expected_outputs = [[(0, [1, 2, 3]), (1, [0, 4, 6, 7, 9]), (2, [0, 3, 6, 8, 9]), (3, [0, 2, 8, 9]), (4, [1, 6, 7, 8]),(5, [9]), (6, [1, 2, 4, 8]), (7, [1, 4, 8]), (8, [2, 3, 4, 6, 7]), (9, [1, 2, 3, 5])], [(0, [1, 2, 3, 4, 5, 6, 7, 8, 9]), (1, [0, 4, 6, 7, 9]), (2, [0, 3, 6,8, 9]), (3, [0, 2, 8, 9]), (4, [0, 1, 6, 7, 8]),
    (5, [0, 9]), (6, [0, 1, 2, 4, 8]), (7, [0, 1, 4, 8]), (8, [0, 2, 3, 4, 6, 7]), (9, [0, 1, 2, 3, 5])], [(0, [1, 2, 3, 4, 5, 6, 7, 8, 9]), (1, [0, 4, 6, 7, 9]), (2, [0, 3, 6,8, 9]), (3, [0, 2, 8, 9]), (4, [0, 1, 6, 7, 8]),
    (5, [0, 9]), (6, [0, 1, 2, 4, 8]), (7, [0, 1, 4, 8]), (8, [0, 2, 3, 4, 6, 7]), (9, [0, 1, 2, 3, 5]),
    (100, [112]), (112, [100, 114]), (114, [112])]]
    for i in range(3):
        pass
        print(test(create_network, expected_outputs[i], files[i]))
    print(create_network(files[4])[500:502] == [(500, [348, 353, 354, 355, 361, 363, 368, 373, 374, 376, 378, 382, 388, 391, 392, 396, 400, 402, 404, 408, 409, 410,
    412, 414, 416, 417, 421, 423, 428, 431, 438, 439, 444, 445, 450,
    452,455, 463, 465, 474, 475, 483, 484,487, 492, 493,
    497, 503, 506, 507, 513, 514, 517, 519, 520, 521, 524, 525, 527, 531, 537, 538, 542, 546, 547, 548, 553, 555, 556, 557,
    560, 563, 565, 566, 580, 591, 601, 604, 614, 637, 645, 651, 683]), (501, [198, 348, 364, 393, 399, 441, 476, 564])])

##############################
# main
##############################

# NOTHING FOLLOWING THIS LINE CAN BE REMOVED or MODIFIED

file_name=get_file_name()
    
net=create_network(file_name)

print("\nFirst general statistics about the social network:\n")
tests()
print("This social network has", len(net), "people/users.")
print("In this social network the maximum number of friends that any one person has is "+str(maximum_num_friends(net))+".")
print("The average number of friends is "+str(average_num_friends(net))+".")
mf=people_with_most_friends(net)
print("There are", len(mf), "people with "+str(maximum_num_friends(net))+" friends and here are their IDs:", end=" ")
for item in mf:
    print(item, end=" ")

print("\n\nI now pick a number at random.", end=" ")
k=random.randint(0,len(net)//4)
print("\nThat number is: "+str(k)+". Let's see how many people has at least that many friends.")
print("There is", k_or_more_friends(net,k), "people with", k, "or more friends")

if knows_everyone(net):
    print("\nThere at least one person that knows everyone.")
else:
    print("\nThere is nobody that knows everyone.")

print("\nWe are now ready to recommend a friend for a user you specify.")
uid=get_uid(net)
rec=recommend(uid, net)
if rec==None:
    print("We have nobody to recommend for user with ID", uid, "since he/she is dominating in their connected component")
else:
    print("For user with ID", uid,"we recommend the user with ID",rec)
    print("That is because users", uid, "and",rec, "have", len(getCommonFriends(uid,rec,net)), "common friends and")
    print("user", uid, "does not have more common friends with anyone else.")
        

print("\nFinally, you showed interest in knowing common friends of some pairs of users.")
print("About 1st user ...")
uid1=get_uid(net)
print("About 2st user ...")
uid2=get_uid(net)
print("Here is the list of common friends of", uid1, "and", uid2)
common=getCommonFriends(uid1,uid2,net)
for item in common:
    print(item, end=" ")










#Testing