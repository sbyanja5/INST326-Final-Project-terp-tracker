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
    
    try:
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
        return semesters 
    except(json.JSONDecodeError, KeyError):
        print("Error reading data file. Starting fresh.")
        return []

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
        Converts this Course to a dictionary for JSON serialization.

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
        total_credits = 0.0                          
        for course in self.courses:
            grade_point = Grades.calculate_grade([course.grade])  
                                                                  
            total_points += grade_point * course.credits
            total_credits += course.credits  

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
        return {
            'term_name': self.term_name,
            'courses': [course.to_dict() for course in self.courses]
        }
        
class Grades:
    @staticmethod
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
    print("\n" + "="*30)
    print("\nCumulative GPA:", cumulative_gpa)
    print("Total Credits Earned:", total_credits)
    print("="*30+"\n")

def add_semester_ui():
    """
    Command line interface for creating a Semester and adding courses to it.
    
    Returns:
        Semester: A completed Semester object.
    """
    term_name = input("Enter semester name (example: Fall 2026): ")
    semester = Semester(term_name)

    while True:
        name = input("Enter course name: ")

        try:
            credits = float(input("Enter course credits: "))
            grade = input("Enter letter grade: ").upper()
            semester.add_course(Course(name, credits, grade))
        except ValueError:
            print("Invalid input. Course not added.")

        another = input("Add another course? (yes/no): ").lower()     
        if another != "yes":
            break
    return semester 
 

def main():
    """Main execution logic for the GPA and Degree Tracker."""
    print("Welcome to the Terp Tracker!")
    semesters = load_data()

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new semester")
        print("2. View academic summary")
        print("3. Final's GPA Calculator")
        print("4. Save and Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            semester = add_semester_ui()
            semesters.append(semester)
        elif choice == "2":
            display_summary(semesters)
        elif choice == "3":
            current_gpa = float(input("Enter your current cumulative GPA: "))
            current_credits = float(input("Enter your total completed credits: "))
            target_gpa = float(input("Enter your target cumulative GPA: "))
            remaining_credits = float(input("Enter the number of credits you have left to complete:"))
            result = finals_calculator(current_gpa, current_credits, target_gpa, remaining_credits)
            if result is not None:
                print(f"You need to earn a GPA of {result} in your remaining credits to reach your target GPA.")
        elif choice == "4":
            save_data(semesters)
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
