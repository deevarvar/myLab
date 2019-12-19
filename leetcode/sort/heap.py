#! /usr/bin/python

def heapify(array):
    # first non-leaf node
    nlnode = (len(array) - 1)/2
    for i in reversed(range(nlnode)):
        siftdown(array, i, len(array) - 1)
        print "index {} {}".format(i, array)

def siftdown(array, start, end):
    root = start
    while (2*root + 1) <= end:  # at lease one left child
        anchor = root
        lefti = 2*root +1
        righti = lefti + 1
        if array[lefti] > array[anchor]:
            anchor = lefti 
        if righti <= end and array[righti] > array[anchor]:
            anchor = righti
        if anchor == root:
            return
        else:
            tmp = array[root]
            array[root] = array[anchor]
            array[anchor] = tmp
            root = anchor


def heapsort(array):
    heapify(array)
    print "after heapify is {}".format(array)
    count = len(array) - 1
    while count > 0:
        tmp = array[0]
        array[0] = array[count]
        array[count] = tmp
        count = count - 1
        siftdown(array, 0, count)

    print "after heapifysort is {}".format(array)

if __name__ == '__main__':
    array = [6, 2, 8, 0, 4, 7, 10]
    barray = array[:]
    barray.sort()
    print "standard array is {}".format(barray)
    heapsort(array)
