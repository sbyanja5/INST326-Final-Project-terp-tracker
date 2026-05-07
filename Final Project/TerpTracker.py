"""
Interactive GPA and Degree Tracker for University of Maryland students. 
This program allows users to input their courses, credits, and grades to calculate their GPA and track their progress in the semester. 
It provides a user-friendly interface for managing academic records and planning future coursework.
"""
import json
import os

def save_data(semesters, filename="terp_tracker_data.json"):
    """
    Saves the list of Semester objects to a JSON file.
    Args:
        semesters (list of Semester): The data to save.
        filename (str): The name of the file to save to.
    Returns:
        None
    """
    data = [semester.to_dict() for semester in semesters]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}.")

def load_data(filename="terp_tracker_data.json"):
    """
    Loads Semester data from a JSON file and reconstructs the Semester and Course objects.
    Args:
        filename (str): The name of the file to load from.
        Defaults to "terp_tracker_data.json".
    Returns:
        list of Semester: A list of Semester objects reconstructed from the file,
        or an empty list if the file does not exist or is invalid.
    """
    if not os.path.exists(filename):
        print(f"No data file found at {filename}. Starting with an empty dataset.")
        return []
    with open(filename, 'r') as f:
        data = json.load(f)

    semesters = []
    for semester_data in data:
        semester = Semester(semester_data['term_name'])
        for course_data in semester_data['courses']:
            course = Course(course_data['name'], 
                            course_data['credits'], 
                            course_data['grade'])
            semester.add_course(course)
        semesters.append(semester)
    return semesters  # BUG FIX: was indented inside the for-loop, returning after the first semester only


class Course:
    """
    Represents a single course with its name, credits, and grade.
    """

    def __init__(self, name, credits, grade):
        self.name = name
        self.credits = credits
        self.grade = grade

    def to_dict(self):
        """
        Convert this Course to a dictionary for JSON serialization.
        BUG FIX: method was missing from Course entirely; Semester.to_dict() called
        course.to__dict_() which had the wrong name AND pointed here, so it needed to exist.
        Returns:
            dict: A dictionary with 'name', 'credits', and 'grade'.
        """
        return {
            "name": self.name,
            "credits": self.credits,
            "grade": self.grade
        }


class Semester:
    """
    Represents a semester containing multiple courses.
    """

    def __init__(self, term_name):
        self.term_name = term_name
        self.courses = []

    def add_course(self, course):
        """
        Adds a course object to the semester's internal list of courses.
        Args:
            course (Course): An instance of the Course class.
        """
        self.courses.append(course)

    def calculate_gpa(self):
        """
        Calculates the GPA for this semester.
        Returns:
            float: The semester GPA rounded to two decimal places.
        """
        total_points = 0.0
        total_credits = 0.0  # BUG FIX: was 'total_credit' (missing 's'), causing a NameError
                              # when the variable was later referenced as 'total_credits'

        for course in self.courses:
            grade_point = Grades.calculate_grade([course.grade])  # BUG FIX 1: was Grades.calcualate_grade (typo)
                                                                   # BUG FIX 2: pass grade as a list — calculate_grade expects one
            total_points += grade_point * course.credits
            total_credits += course.credits  # BUG FIX: was 'total_credit' (missing 's')

        if total_credits == 0:
            return 0.0

        return round(total_points / total_credits, 2)

    def get_total_credits(self):
        """
        Sum all credit hours for courses in this semester.
        Returns:
            float: Total credit hours for the semester.
        """
        return sum(course.credits for course in self.courses)

    def is_full_time(self):
        """
        Determines if the student is enrolled full time (12+ credits).
        Returns:
            bool: True if credits >= 12, False otherwise.
        """
        return self.get_total_credits() >= 12

    def get_academic_standing(self):
        """
        Evaluates the semester GPA to determine academic standing.
        Returns:
            str: Dean's List, Good Standing, or Academic Probation.
        """
        current_gpa = self.calculate_gpa()
        if current_gpa >= 3.5:
            return "Dean's List"
        elif current_gpa >= 2.0:
            return "Good Standing"
        else:
            return "Academic Probation"

    def to_dict(self):
        """
        Convert this Semester and all its courses to a dictionary for JSON serialization.
        Returns:
            dict: A dictionary with 'term_name' and a list of course dicts.
        """
        # BUG FIX 1: was calling course.to__dict_() — double underscores, wrong method name
        # BUG FIX 2: was also referencing self.name / self.credits / self.grade,
        #            which Semester does not have (those belong on Course)
        return {
            'term_name': self.term_name,
            'courses': [course.to_dict() for course in self.courses]
        }


class Grades:

    def __init__(self, grade, gpa, num_of_classes):
        self.grade = grade
        self.gpa = gpa
        self.num_of_classes = num_of_classes  # BUG FIX: was accepted but never stored

    def calculate_grade(grades):
        """
        Returns the average GPA point value for a list of letter grades.
        Args:
            grades (list of str): Letter grades (e.g. ["A", "B+"]).
        Returns:
            float: The average GPA point value.
        """
        possible_grades = {
            "A+": 4.0, "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D+": 1.3, "D": 1.0, "D-": 0.7,
            "F": 0.0
        }

        if not grades:
            return 0

        total_grade = 0
        for grade in grades:
            grade = grade.upper()
            if grade not in possible_grades:
                raise ValueError("This grade is not a possible grade, please try again.")
            total_grade += possible_grades[grade]

        return total_grade / len(grades)


def calculate_cumulative_gpa(semesters):
    """
    Calculates the cumulative GPA across multiple semesters.
    Args:
        semesters (list of Semester): a list of Semester objects to include in the calculation.
    Returns:
        float: The cumulative GPA rounded to two decimal places,
               or 0.0 if there are no credits.
    """
    total_points = 0.0
    total_credits = 0.0

    for semester in semesters:
        for course in semester.courses:
            grade_point = Grades.calculate_grade([course.grade])
            total_points += grade_point * course.credits
            total_credits += course.credits

    if total_credits == 0:
        return 0.0

    return round(total_points / total_credits, 2)

def finals_calculator(current_gpa, current_credits, target_gpa, remaining_credits):
    # BUG FIX: parameter was spelled 'current_creddits' (double 'd'), causing a NameError
    # when the function body referenced 'current_credits'
    """
    Calculates the GPA needed in remaining credits to achieve a target cumulative GPA.

    Args:
        current_gpa (float): The student's current cumulative GPA.
        current_credits (float): Total credits completed so far.
        target_gpa (float): The desired cumulative GPA.
        remaining_credits (float): Credits left to complete.
    Returns:
        float: GPA needed in remaining credits to reach the target, rounded to two decimal places,
               or None if the target is not achievable.
    """
    total_credits = current_credits + remaining_credits
    needed_points = (target_gpa * total_credits) - (current_gpa * current_credits)
    needed_gpa = needed_points / remaining_credits

    if needed_gpa > 4.0:
        print("Target GPA is not achievable with the remaining credits.")
        return None

    if needed_gpa < 0.0:
        print("Target GPA is already achieved with the current GPA!")
        return 0.0

    return round(needed_gpa, 2)

def check_credit_milestones(total_credits):
    """
    Checks if the student has reached a credit milestone and notifies them.

    Args:
        total_credits (float): Total credits the student has completed.
    Returns:
        str: A congratulatory message if a milestone has been reached,
             or None if no milestone is reached.
    """
    milestones = {
        30: "Congratulations! You've reached 30 credits - you're a sophomore!",
        60: "Congratulations! You've reached 60 credits - you're a junior!",
        90: "Congratulations! You've reached 90 credits - you're a senior!",
        120: "Congratulations! You've reached 120 credits - you've completed your degree requirements!"
    }

    # BUG FIX 1: 'if total_credits >= 30' and 'return None' were both indented inside
    #             the for-loop body, so the loop never ran past the first milestone check.
    # BUG FIX 2: was returning 'highest_milestone' (an int key) instead of the message string.
    highest_message = None
    for milestone, message in milestones.items():
        if total_credits >= milestone:
            highest_message = message

    return highest_message

def display_summary(semesters):
    """
    Prints a full summary of all semesters, GPAs, and credits.
    Args:
        semesters (list of Semester): All semesters to summarize.
    """
    if len(semesters) == 0:
        print("No semesters recorded yet.")
        return

    print("\n===== ACADEMIC SUMMARY =====")
    for semester in semesters:
        print(f"\n{semester.term_name}")
        print(f" Courses:")
        for course in semester.courses:
            print(f"     {course.name}  |  {course.credits} credits | {course.grade}")
        print(f"  Semester GPA: {semester.calculate_gpa()}")
        print(f"  Total Credits: {semester.get_total_credits()}")
        print(f"  Academic Standing: {semester.get_academic_standing()}")
        print(f"  Full-Time Status: {'Full-Time' if semester.is_full_time() else 'Part-Time'}")

    total_credits = 0.0
    for semester in semesters:
        total_credits += semester.get_total_credits()

    cumulative_gpa = calculate_cumulative_gpa(semesters)
    print("\nCumulative GPA:", cumulative_gpa)
    print("Total Credits Earned:", total_credits)
    print("===========================\n")

def add_course_ui():
    """
    Command line interface for creating a Course object.
    Returns:
        Course: A new Course object created from user input.
    """
    name = input("Enter course name: ")
    credits = float(input("Enter course credits: "))
    grade = input("Enter letter grade: ")
    return Course(name, credits, grade)

def add_semester_ui():
    """
    Command line interface for creating a Semester and adding courses to it.
    Returns:
        Semester: A completed Semester object.
    """
    term_name = input("Enter semester name (example: Fall 2026): ")
    semester = Semester(term_name)

    while True:
        print("\nAdd a course")
        course = add_course_ui()
        semester.add_course(course)
        another = input("Add another course? (yes/no): ").lower()
        if another != "yes":
            break
    return semester

def main():
    """Main execution logic for the GPA and Degree Tracker."""
    print("Welcome to the Terp Tracker!")
    # TODO: add persistent storage and user input logic

if __name__ == "__main__":
    main()
