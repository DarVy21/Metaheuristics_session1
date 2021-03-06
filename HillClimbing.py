import random
import numpy as np
from tqdm import tqdm


def evaluateSolution(data, solution):
    routeLength = 0
    for i in range(len(solution)):
        routeLength += data[solution[i - 1]][solution[i]]
    return routeLength


def double_bridge_move(solution):
    # (4-opt) divide the whole permutation into four approx equal parts (a, b, c, d) and reconnect them to find new solution
    # a = [0...pos1], b = [pos1...pos2], c = [pos2...pos3], d = [pos3..perm.size]
    # originally: a --> b --> c --> d
    # after:      a --> d --> c --> b
    pos1 = 1 + random.randint(0, len(solution) // 4)  # get start and end points of segments
    pos2 = pos1 + 1 + random.randint(0, len(solution) // 4)
    pos3 = pos2 + 1 + random.randint(0, len(solution) // 4)
    p1 = np.concatenate((solution[0:pos1], solution[pos3:]))
    p2 = np.concatenate((solution[pos2:pos3], solution[pos1:pos2]))
    return np.concatenate((p1, p2))


def perturbation(solution):
    new_solution = double_bridge_move(solution)
    return new_solution


def getBestNeighbor(solution, data):
    # Get the neighbors
    neighbors = []
    l = len(solution)
    for i in range(l):
        for j in range(i + 1, l):
            n = solution.copy()
            n[i] = solution[j]
            n[j] = solution[i]
            neighbors.append(n)

    # Get the best neighbor
    bestNeighbor = neighbors[0]
    bestLength = evaluateSolution(data, bestNeighbor)
    for neighbor in neighbors:
        routeLength = evaluateSolution(data, neighbor)
        if routeLength < bestLength:
            bestLength = routeLength
            bestNeighbor = neighbor
    return bestNeighbor, bestLength


def getRandomSolution(data):
    l = len(data)
    solution = np.random.permutation(np.arange(l))
    routeLength = evaluateSolution(data, solution)
    return solution, routeLength


def hillClimbing(data):
    solutions = []
    routes = []
    iterations = 100
    solution, routeLength = getRandomSolution(data)
    for _ in tqdm(range(iterations)):
        print("Route 1: " + str(solution) + " Length: " + str(routeLength))
        neighbor = getBestNeighbor(solution, data)
        i = 1
        while neighbor[1] < routeLength:
            solution = neighbor[0]
            routeLength = neighbor[1]
            i = i + 1
            print("Route " + str(i) + ": " + str(solution) + " Length: " + str(routeLength))
            neighbor = getBestNeighbor(solution, data)
        solutions.append(solution)
        routes.append(routeLength)
        solution = perturbation(solution)
        routeLength = evaluateSolution(data, solution)
        print("---------------------")
    return solutions, routes


def main():
    data = [
        [0, 70, 635, 878, 994, 478, 560, 439, 295, 280, 465, 625, 122, 951, 240, 383, 827, 383, 949, 904, 863, 625, 943,
         135, 488, 567, 93, 943, 495, 137],
        [
            70, 0, 232, 627, 593, 262, 585, 849, 996, 246, 702, 161, 363, 815, 417, 553, 86, 760, 770, 53, 553, 225,
            780, 807, 858, 613, 646, 507, 709, 676],
        [
            635, 232, 0, 871, 484, 986, 224, 519, 213, 395, 430, 449, 753, 782, 860, 882, 296, 633, 691, 557, 391, 195,
            907, 295, 29, 162, 867, 764, 953, 519],
        [
            878, 627, 871, 0, 569, 28, 933, 699, 504, 579, 335, 600, 354, 50, 586, 792, 193, 914, 406, 782, 461, 500,
            249, 231, 471, 681, 114, 976, 719, 61],
        [
            994, 593, 484, 569, 0, 737, 983, 506, 839, 1000, 169, 556, 486, 886, 59, 69, 737, 914, 408, 86, 506, 422,
            361, 471, 973, 331, 960, 228, 147, 46],
        [
            478, 262, 986, 28, 737, 0, 222, 879, 145, 648, 467, 179, 117, 346, 480, 285, 212, 964, 633, 404, 76, 609,
            43, 754, 903, 483, 837, 802, 628, 84],
        [
            560, 585, 224, 933, 983, 222, 0, 573, 419, 478, 672, 191, 59, 696, 596, 259, 61, 643, 794, 178, 630, 637,
            854, 993, 729, 901, 407, 689, 170, 29],
        [
            439, 849, 519, 699, 506, 879, 573, 0, 197, 231, 485, 532, 834, 174, 277, 499, 139, 505, 585, 765, 257, 898,
            503, 199, 29, 668, 240, 142, 146, 919],
        [
            295, 996, 213, 504, 839, 145, 419, 197, 0, 301, 695, 906, 315, 649, 218, 803, 240, 988, 81, 618, 623, 615,
            821, 833, 279, 869, 984, 750, 788, 647],
        [
            280, 246, 395, 579, 1000, 648, 478, 231, 301, 0, 492, 215, 205, 339, 16, 618, 548, 449, 375, 27, 897, 100,
            589, 923, 67, 227, 158, 151, 50, 519],
        [
            465, 702, 430, 335, 169, 467, 672, 485, 695, 492, 0, 861, 974, 937, 561, 749, 377, 168, 247, 594, 118, 254,
            974, 151, 682, 470, 765, 415, 910, 130],
        [
            625, 161, 449, 600, 556, 179, 191, 532, 906, 215, 861, 0, 43, 929, 427, 55, 840, 737, 412, 476, 74, 886,
            512, 924, 613, 749, 671, 937, 800, 158],
        [
            122, 363, 753, 354, 486, 117, 59, 834, 315, 205, 974, 43, 0, 982, 396, 827, 948, 710, 919, 932, 498, 103,
            135, 384, 337, 550, 458, 239, 257, 336],
        [
            951, 815, 782, 50, 886, 346, 696, 174, 649, 339, 937, 929, 982, 0, 473, 50, 113, 494, 576, 316, 394, 761,
            302, 326, 113, 309, 973, 751, 299, 172],
        [
            240, 417, 860, 586, 59, 480, 596, 277, 218, 16, 561, 427, 396, 473, 0, 306, 509, 46, 83, 674, 980, 589, 185,
            712, 651, 553, 158, 894, 481, 198],
        [
            383, 553, 882, 792, 69, 285, 259, 499, 803, 618, 749, 55, 827, 50, 306, 0, 540, 911, 53, 356, 549, 536, 683,
            953, 217, 181, 974, 433, 352, 152],
        [
            827, 86, 296, 193, 737, 212, 61, 139, 240, 548, 377, 840, 948, 113, 509, 540, 0, 228, 560, 945, 390, 301,
            23, 116, 847, 801, 910, 883, 181, 548],
        [
            383, 760, 633, 914, 914, 964, 643, 505, 988, 449, 168, 737, 710, 494, 46, 911, 228, 0, 202, 660, 567, 563,
            977, 748, 210, 630, 529, 782, 282, 79],
        [
            949, 770, 691, 406, 408, 633, 794, 585, 81, 375, 247, 412, 919, 576, 83, 53, 560, 202, 0, 612, 399, 850,
            938, 373, 103, 249, 818, 333, 549, 432],
        [
            904, 53, 557, 782, 86, 404, 178, 765, 618, 27, 594, 476, 932, 316, 674, 356, 945, 660, 612, 0, 431, 710,
            144, 854, 154, 282, 800, 874, 482, 537],
        [
            863, 553, 391, 461, 506, 76, 630, 257, 623, 897, 118, 74, 498, 394, 980, 549, 390, 567, 399, 431, 0, 669,
            89, 315, 456, 300, 755, 801, 299, 958],
        [
            625, 225, 195, 500, 422, 609, 637, 898, 615, 100, 254, 886, 103, 761, 589, 536, 301, 563, 850, 710, 669, 0,
            131, 15, 342, 685, 384, 883, 421, 835],
        [
            943, 780, 907, 249, 361, 43, 854, 503, 821, 589, 974, 512, 135, 302, 185, 683, 23, 977, 938, 144, 89, 131,
            0, 598, 78, 110, 734, 606, 772, 559],
        [
            135, 807, 295, 231, 471, 754, 993, 199, 833, 923, 151, 924, 384, 326, 712, 953, 116, 748, 373, 854, 315, 15,
            598, 0, 758, 97, 806, 900, 44, 933],
        [
            488, 858, 29, 471, 973, 903, 729, 29, 279, 67, 682, 613, 337, 113, 651, 217, 847, 210, 103, 154, 456, 342,
            78, 758, 0, 328, 842, 836, 398, 296],
        [
            567, 613, 162, 681, 331, 483, 901, 668, 869, 227, 470, 749, 550, 309, 553, 181, 801, 630, 249, 282, 300,
            685, 110, 97, 328, 0, 520, 114, 197, 221],
        [
            93, 646, 867, 114, 960, 837, 407, 240, 984, 158, 765, 671, 458, 973, 158, 974, 910, 529, 818, 800, 755, 384,
            734, 806, 842, 520, 0, 707, 902, 554],
        [
            943, 507, 764, 976, 228, 802, 689, 142, 750, 151, 415, 937, 239, 751, 894, 433, 883, 782, 333, 874, 801,
            883, 606, 900, 836, 114, 707, 0, 350, 584],
        [
            495, 709, 953, 719, 147, 628, 170, 146, 788, 50, 910, 800, 257, 299, 481, 352, 181, 282, 549, 482, 299, 421,
            772, 44, 398, 197, 902, 350, 0, 228],
        [
            137, 676, 519, 61, 46, 84, 29, 919, 647, 519, 130, 158, 336, 172, 198, 152, 548, 79, 432, 537, 958, 835,
            559, 933, 296, 221, 554, 584, 228, 0],
    ]

    solutions, routes = hillClimbing(data)
    size = len(solutions)
    for i in range(size):
        print("Final solution: ", solutions[i])
        print("Final route length: ", routes[i])
        print("----------------------------------------")
    routes.sort()
    print("Best route length:", routes[0])


if __name__ == "__main__":
    main()
