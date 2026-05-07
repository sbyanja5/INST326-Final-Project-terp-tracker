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
        list of Semester: A list of Semester objects reconstructed from the file.
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
        return semesters
    
class Course:

    """
    Represents a single course with its name, credits, and grade.
    """

    def __init__(self, name, credits, grade):
        self.name = name
        self.credits = credits
        self.grade = grade


class Semester: 
        """
        Represents a semester containing multiple courses.
    
        """

        def __init__(self, term_name):
            self.term_name = term_name
            self.courses = []
        
        def add_course(self, course):
            """
            Adds a course object to the semester's interal list of courses. 
            Arguments are course (course): An instance of the Course class.
            """
            self.courses.append(course)

        def calculate_gpa(self):
            total_points = 0.0
            total_credit = 0.0

            for course in self.courses:
                grade_point = Grades.calcualate_grade(course.grade)
                total_points += grade_point * course.credits
                total_credits += course.credits

            if total_credit == 0:
                return 0.0

            return round(total_points / total_credits, 2)
        
        def get_total_credits(self):
            """
            Sum all credit hours for courses in this semester

            Returns:
                float: Total credit hours for the semester
            """
            return sum(course.credits for course in self.courses)
        def is_full_time(self):
            """
            Determines if the student is enrolled full time, which is 12+ credits.

            Returns:
                bool: True if credits >= 12, False otherwise.
            """
            return self.get_total_credits() >= 12

        def get_academic_standing(self):
            """
            Evaluates the semester GPA to determine academic standing.
            Returns:
                str: A message indicating if the student is on the Dean's List, in Good Standing, or on Academic Probation.
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
                And each course dict contains 'name', 'credits', and 'grade'.
            """
            return {
                'term_name': self.term_name,
                'courses': [course.to__dict_() for course in self.courses]
                "name": self.name,
                "credits": self.credits,
                "grade": self.grade
            }
        
class Grades:

    def __init__(self, grade, gpa, num_of_classes):

        self.grade = grade
        self.gpa = gpa

    """The calculate_grade method returns an integer based on an integer
    that is the number of classes the user took, and the string that the
    user provides. There will be a user_input that asks the user for the
    letter grade they received on a certain course. Then, the integer
    returned will be the gpa.
    """
    def calculate_grade(grades):

        possible_grades = {
            "A+": 4.0, "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D+": 1.3, "D": 1.0, "D-": 0.7,
            "F":0.0
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
    Calcuates the cumulative GPA across multiple semesters.
    Args:
        semesters (list of Semester): a list of Semester objects to include in the calculation.
    Returns:
        float: The cumulative GPA rounded to two decimal places.
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

def finals_calculator(current_gpa, current_creddits, target_gpa, remaining_credits):
    """
    Calucates the GPA needed in the remaining credits to achieve a target cumulative GPA.

    Args:
        current_gpa (float): The student's current cumulative GPA.
        current_credits (float): The total number of credits the student has completed.
        target_gpa (float): The desired cumulative GPA the student wants to achieve.
        remaining_credits (float): The number of credits the student has left to complete.
    Returns:
        float: The GPA needed in the remaining credits to reach the target GPA, rounded to two decimal places.
        or None if it's not possible to achieve the target GPA with the remaining credits.
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
        total_credits (float): The total number of credits the student has completed.
    Returns:
        str: A congratulatory message indicating the next milestone or if a milestone has been reached,    
             or None if no milestones are reached.
        """
    milestones = {
        30: "Congratulations! You've reached 30 credits - you're a sophomore!",
        60: "Congratulations! You've reached 60 credits - you're a junior!",
        90: "Congratulations! You've reached 90 credits - you're a senior!",
        120: "Congratulations! You've reached 120 credits - you've completed your degree requirements!"
    }

    for milestone, message in milestones.items():
        if total_credits >= milestone:
            highest_milestone = milestone

        if total_credits >= 30:
            return highest_milestone
        return None

def display_summary(semesters):
    """
    Prints a full summary of all semesters, GPAs, and credits.
    Args:
        semesters(list of Semester): All semesters to summarize.
    """
    if len(semesters) == 0:
        print("No semesters recorded yet.")
        return

    print ("\n===== ACADEMIC SUMMARY =====")
    for semester in semesters:
        print (f"\n{semester.term_name}")
        print (f" Courses:")
        for course in semester.courses:
            print (f"     {course.name}  |  {course.credits} credits | {course.grade}")
        print (f"  Semester GPA: {semester.calculate_gpa()}")
        print (f"  Total Credits: {semester.get_total_credits()}")
        print (f"  Academic Standing: {semester.get_academic_standing()}")
        print (f"  Full-Time Status: {'Full-Time' if semester.is_full_time() else 'Part-Time'}")
                                  
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
        Courses: A new Course object created from user input.
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
