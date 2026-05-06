import unittest
from TerpTracker import Course, Semester, check_credit_milestones, finals_calculator

class TestTerpTracker(unittest.TestCase):
    """
 Test cases for the Gpa and Degree Tracker classes.
    """

    def test_course_initialization(self):
        """Test that a Course object is stored correctly."""
        
        # Create a test course
        test_course = Course("INST326", 3, "A")
        
        # Check that the attributes are stored correctly
        self.assertEqual(test_course.name, "INST326")
        self.assertEqual(test_course.credits, 3)
        self.assertEqual(test_course.grade, "A")


    def test_add_course_to_semester(self):
        """Tests if courses can be added to a Semester correctly."""
        test_semester = Semester("Fall 2024")
        test_course = Course("INST326", 3, "A")

        # Add the course
        test_semester.add_course(test_course)

        # Check if the list now has exactly 1 course
        self.assertEqual(len(test_semester.courses), 1)
        self.assertEqual(test_semester.courses[0].name, "INST326")

def test_finals_calculator():
    # Normal case - need a specific GPA
    assert finals_calculator(3.0, 60, 3.5, 30) == 4.5 # not possible

    # Already at target GPA
    assert finals_calculator(3.8, 60, 3.5, 30) == 3.5 is None
    
    # Achievable target GPA
    assert finals_calculator(3.0, 45, 3.2, 15) == round(((3.2 * 60) - (3.0 * 45)) / 15, 2)

def test_check_credit_milestones():
    # No milestone reached
    assert check_credit_milestones(20) is None

    # Sophomore milestone
    assert check_credit_milestones(30) == "Congratulations! You've reached 30 credits - you're a sophomore!"

    # Junior milestone
    assert check_credit_milestones(60) == "Congratulations! You've reached 60 credits - you're a junior!"

    # Senior milestone
    assert check_credit_milestones(90) == "Congratulations! You've reached 90 credits - you're a senior!"


if __name__ == "__main__":
    unittest.main()

