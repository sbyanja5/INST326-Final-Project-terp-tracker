"""
Interactive GPA and Degree Tracker for University of Maryland students. 
This program allows users to input their courses, credits, and grades to calculate their GPA and track their progress in the semester. 
It provides a user-friendly interface for managing academic records and planning future coursework.
"""

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
            total_points = 0
            total_credit = 0

            for course in self.courses:
                grade_point = Grade.calcualate_grade(course.grade)
                total_points += grade_points * course.credits
                total_credits += course.credits

            if total_credit == 0:
                return 0

            return total_points / total_credits
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
                'courses': [course.to__dict_() for course in self.courses]
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

      
    

def main():
    """Main execution logic for the GPA and Degree Tracker."""   
    print("Welcome to the Terp Tracker!")
    # TODO: add persistent storage and user input logic

if __name__ == "__main__":
    main()
