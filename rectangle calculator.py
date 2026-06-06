def calc_perimeter(length, width):
    return (length + width) * 2


def calc_area(length, width):
    return length * width


def main():
    while True:
        try:
            side_1 = float(input('Enter length of side 1: '))
            if side_1 > 0:
                break
            else:
                print('Please enter a positive number for side 1')
        except ValueError:
            print('Please enter a number for side 1')

    while True:
        try:
            side_2 = float(input("Enter length of side 2: "))
            if side_2 > 0:
                break
            else:
                print('Please enter a positive number for side 2')
        except ValueError:
            print('Please enter a number for side 2')

    print(f'area of rectangle {side_1:g} by {side_2:g} = '
          f'{calc_area(side_1, side_2):g}')
    print(f'perimeter of rectangle {side_1:g} by {side_2:g} = '
          f'{calc_perimeter(side_1, side_2):g}')


if __name__ == '__main__':
    main()
