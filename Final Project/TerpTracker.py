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
            """Adds a course to the semester.
            """ 

            self.courses.append(course)

        
    
    
    
    
    
def main():
    """Main execution logic for the GPA and Degree Tracker."""   
    print("Welcome to the Terp Tracker!")
    # TODO: add persistent storage and user input logic

if __name__ == "__main__":
    main()