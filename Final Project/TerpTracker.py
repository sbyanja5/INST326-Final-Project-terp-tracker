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
    def calculate_grade(grade):

        total_grade = 0
        grade = grade.upper()
        if grade == "A+" or grade == "A":
            total_grade += 4.0
        elif grade == "A-":
            total_grade += 3.7
        elif grade == "B+":
            total_grade += 3.3
        elif grade == "B":
            total_grade += 3.0
        elif grade == "B-":
            total_grade += 2.7
        elif grade == "C+":
            total_grade += 2.3
        elif grade == "C":
            total_grade += 2.0
        elif grade == "C-":
            total_grade += 1.7
        elif grade == "D+":
            total_grade += 1.3
        elif grade == "D":
            total_grade += 1
        elif grade == "D-":
            total_grade += 0.7
        elif grade == "F":
            total_grade += 0
        else:
            raise ValueError("This grade is not a grade, please try again")

        return total_grade    
    
def main():
    """Main execution logic for the GPA and Degree Tracker."""   
    print("Welcome to the Terp Tracker!")
    # TODO: add persistent storage and user input logic

if __name__ == "__main__":
    main()
