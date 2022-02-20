from math import dist, inf


def kmeans(points, k, centers=None, number_of_iterations=1024):
    if centers is None:
        centers = [points[i] for i in range(k)]
    for iteration in range(number_of_iterations):
        clusters = [[] for _ in range(k)]
        for point in points:
            closest_center = None
            min_dist = inf
            for i, center in enumerate(centers):
                current_dist = dist(point, center)
                if current_dist < min_dist:
                    min_dist = current_dist
                    closest_center = i
            clusters[closest_center].append(point)
        for i, cluster in enumerate(clusters):
            closest_center = None
            if len(cluster) == 0:
                center[i] = points[(iteration + i) % len(points)]
                continue
            center = [0] * len(cluster[0])
            for point in cluster:
                center = [x + y for x, y in zip(center, point)]
            center = tuple(x / len(cluster) for x in center)
            centers[i] = center
    return centers
