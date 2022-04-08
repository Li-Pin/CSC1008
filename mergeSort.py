def mergeSort(edgeGraph):
    if len(edgeGraph) > 1:

        # Finding the mid of the array
        mid = len(edgeGraph) // 2

        # Dividing the array elements
        L = edgeGraph[:mid]

        # into 2 halves
        R = edgeGraph[mid:]

        # Sorting the first half
        mergeSort(L)

        # Sorting the second half
        mergeSort(R)

        i = j = o = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i][1] < R[j][1]:
                edgeGraph[o] = L[i]
                i += 1
            else:
                edgeGraph[o] = R[j]
                j += 1
            o += 1

        # Checking if any element was left
        while i < len(L):
            edgeGraph[o] = L[i]
            i += 1
            o += 1

        while j < len(R):
            edgeGraph[o] = R[j]
            j += 1
            o += 1
