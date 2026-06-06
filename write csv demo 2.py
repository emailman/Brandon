import csv

# Simple dictionary with student data
students = {
    1: {'name': 'Alice', 'grade': 90},
    2: {'name': 'Bob', 'grade': 85},
    3: {'name': 'Carol', 'grade': 92},
}
print(students)

# Get fieldnames from the dictionary keys
first_student = None
for first_student in students.values():
    print(first_student)
    break
fieldnames = ['id'] + list(first_student.keys())
print(fieldnames)

# Write dictionary to CSV file
with open('students.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for student_id, data in students.items():
        row = {'id': student_id, **data}
        writer.writerow(row)
