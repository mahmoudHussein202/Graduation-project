"""
Directional test
import car

up_dir = (0, -1)
bottom_dir = (0, 1)
left_dir = (-1, 0)
right_dir = (1, 0)
directions = [up_dir, right_dir, bottom_dir, left_dir]
words = ["up", "right", "bottom", "left"]
if __name__ == '__main__':
    for i in range(4):
        for j in range(3):
            if i == j:
                continue
            else:
                isOpposite = car.Directions.isOpposite(directions[i], directions[j])
                isPerpendicular = car.Directions.isPerpendicular(directions[i], directions[j])
                if isOpposite:
                    print(f"{words[i]} direction is Opposite to {words[j]} direction\n")
                if isPerpendicular:
                    print(f"{words[i]} direction is Perpendicular to {words[j]} direction\n")

"""

