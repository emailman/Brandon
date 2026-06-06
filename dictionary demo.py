from statistics import mean

"""
Store students' grades in a dictionary
Report grades by student and grades by exercise

grades dictionary:
key is the student id
value is a dictionary of student's name and grade on each exercise

exercises dictionary:
key is the exercise id
value is the percent weight of the exercise
"""

grades = {
    101: {'name': 'Bob Smith', 'test 1': 85, 'test 2': 90,
          'mid-term exam': 92.5, 'final exam': 95},
    103: {'name': 'George Jones', 'test 1': 88, 'test 2': 90.5,
          'mid-term exam': 92, 'final exam': 90},
    104: {'name': 'Bridget Jones', 'test 1': 85, 'test 2': None,
          'mid-term exam': 92, 'final exam': 87},
}

exercises = {'test 1': 15, 'test 2': 15,
             'mid-term exam': 30, 'final exam': 40}

# Print grades for each student and calculate the final grade
for student_id, student_data in grades.items():
    print(f"Student: {student_data['name']} (ID: {student_id})")
    print("-" * 40)

    # Print individual grades and calculate the weighted final grade
    total_weight = 0
    weighted_sum = 0

    for exercise, weight in exercises.items():
        grade = student_data.get(exercise)
        if grade is not None:
            print(f"  {exercise:14s}: {grade}")
            weighted_sum += grade * weight
            total_weight += weight
        else:
            print(f"  {exercise:14s}: Missing")

    # Calculate final grade (only from completed exercises)
    if total_weight > 0:
        final_grade = weighted_sum / total_weight
        print(f"\n  {'Final Grade':14s}: {final_grade:.1f}")
    else:
        print(f"\n  {'Final Grade':14s}: N/A (no grades)")

    print()

# Print results for each exercise
print("=" * 50)
print("Exercise Results")
print("=" * 50)

for exercise, weight in exercises.items():
    # Collect all grades for this exercise (excluding None)
    exercise_grades = []
    for student_id, student_data in grades.items():
        grade = student_data.get(exercise)
        if grade is not None:
            exercise_grades.append(grade)

    print(f"\n{exercise} (Weight: {weight}%)")
    print("-" * 40)

    if exercise_grades:
        low_grade = min(exercise_grades)
        high_grade = max(exercise_grades)
        average = mean(exercise_grades)
        print(f"  Low:     {low_grade}")
        print(f"  High:    {high_grade}")
        print(f"  Average: {average:.1f}")
    else:
        print("  No grades available")
