__author__ = 'Jonas'

def remove_sublist(mainlist, sublist):
    """
    given a main list and a sub list, returns an alteration of the main list where only the first occurance of the sub
    list has been removed from the original main list
    :param mainlist:(list) the list to be altered
    :param sublist:(list) the sub list to be removed
    :return:(list) the main list without the sub list in it
    """
    # determining the index borders of the sublist within the main list
    start_index = search_sublist(mainlist, sublist)
    end_index = start_index + len(sublist)
    new_list = []
    # adding everything, that is not within the defined borders to the new list, effectively removing the items of
    # the given sublist
    if start_index is not False:
        for index in range(0,len(mainlist)):
            if index < start_index and index > end_index:
                new_list.append(mainlist[index])
        return new_list
    else:
        return mainlist

def replace_sublist(mainlist, sublist, replacement):
    """
    given a main list and a sub list, returns an alteration of the main list where only the first occurance of the sub
    list has been replaced by the given replacement
    :param mainlist:(list) the list to be altered
    :param sublist:(list) the sub list to be removed
    :param replacement: (?) the item to replace the sublist
    :return:(list) the main list without the sub list in it
    """
    # determining the index borders of the sublist within the main list
    start_index = search_sublist(mainlist, sublist)
    end_index = start_index + len(sublist)
    new_list = []
    # adding everything, that is not within the defined borders to the new list, effectively removing the items of
    # the given sublist
    if start_index is not False:
        for index in range(0,len(mainlist)):
            if index < start_index and index > end_index:
                new_list.append(mainlist[index])
            if index == start_index + 1:
                if type(replacement) is list:
                    for item in replacement:
                        new_list.append(item)
                else:
                    new_list.append(replacement)
        return new_list
    else:
        return mainlist

def search_sublist(mainlist, sublist):
    """
    given a mainlist and a sublist, returns the startindex of the given sublist within the main list if possible.
    In case there are multiple occurances of the given sub list within the main list, uses the first one. Returns False
    in case no sub list has been found within the main list.
    :param mainlist:(list) the main list to be searched in
    :param sublist:(list) the sub list to be searched for
    :return:(int) the starting index of the sublist sequence within the main list
    """
    start_index = 0
    found = True
    # going through the mainlist and searching for the first matching item
    for index in range(0, len(mainlist)):
        if mainlist[index] == sublist[0]:
            # assuming since the first variable is matching, the full sublist has been found unitl proven wrong
            found = True
            start_index = index
            # checking every item after the first match with the items of the sublist
            for j in range(1, len(sublist)):
                # as soon as one item doesnt match the found variable will be switched
                if not(mainlist[index + j] == sublist[j]):
                    found = False
            # breaking so that the first occurance of possibly multiple sublists will be used in the search
            if found:
                break
    # in case found is still true, meaning there is not a single false item in the sequence, returning the startindex
    # of this found sublist within the main list
    if found == True:
        return start_index
    else:
        return False