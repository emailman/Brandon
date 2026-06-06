import csv

grades = {
    101: {'name': 'Bob Smith', 'test 1': 85, 'test 2': 90,
          'mid-term exam': 92.5, 'final exam': 95},
    103: {'name': 'George Jones', 'test 1': 88, 'test 2': 90.5,
          'mid-term exam': 92, 'final exam': 90},
    104: {'name': 'Bridget Jones', 'test 1': 85, 'test 2': None,
          'mid-term exam': 92, 'final exam': 87},
}

# Get column headings from the first student's dictionary keys
first_student = None
for first_student in grades.values():
    print(first_student)
    break
fieldnames = ['student_id'] + list(first_student.keys())
print(fieldnames)

with open('grade report.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for student_id, student_data in grades.items():
        row = {'student_id': student_id, **student_data}
        writer.writerow(row)
