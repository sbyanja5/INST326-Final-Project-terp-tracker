import unittest
from TerpTracker import Course, Semester

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

if __name__ == "__main__":
    unittest.main()

