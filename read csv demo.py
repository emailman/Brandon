import csv


def load_grades(filename):
    """Read a CSV file and load the data into a dictionary."""
    grades = {}

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            print(row)
            student_id = row['StudentID']
            grades[student_id] = {}
            for key, value in row.items():
                if key != 'StudentID':
                    if value:
                        grades[student_id][key] = value
                    else:
                        grades[student_id][key] = None

    return grades


def main():
    grades_data = load_grades('grades.csv')

    for student_id, info in grades_data.items():
        print(f"Student {student_id}: {info}")

    # Print grades for each student and calculate the final grade
    for student_id, student_data in grades_data.items():
        print()
        print(f"Student: {student_data['Name']} (ID: {student_id})")
        print("-" * 40)

        for exercise, grade in student_data.items():
            if exercise == 'Name':
                continue
            if grade:
                print(f"  {exercise:14s}: {grade}")
            else:
                print(f"  {exercise:14s}: Missing")

if __name__ == '__main__':
    main()
