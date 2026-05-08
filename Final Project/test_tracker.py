import unittest
from Terp_Tracker import (Course, Semester, check_credit_milestones,
                         finals_calculator, display_summary,
                         calculate_cumulative_gpa, save_data, load_data)


class TestTerpTracker(unittest.TestCase):
    """
    Test cases for the GPA and Degree Tracker classes.
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

        self.assertEqual(len(test_semester.courses), 1)
        self.assertEqual(test_semester.courses[0].name, "INST326")

    def test_finals_calculator(self):
        result = finals_calculator(3.0, 60, 3.5, 30)
        self.assertIsNone(result)

        result = finals_calculator(3.8, 60, 3.5, 30)
        self.assertEqual(result, 0.0)

        # Achievable target GPA — assert the computed value matches expected
        expected = round(((3.2 * 60) - (3.0 * 45)) / 15, 2)
        self.assertEqual(finals_calculator(3.0, 45, 3.2, 15), expected)

    def test_check_credit_milestones(self):
        # No milestone reached
        self.assertIsNone(check_credit_milestones(20))

        # Sophomore milestone
        self.assertEqual(
            check_credit_milestones(30),
            "Congratulations! You've reached 30 credits - you're a sophomore!"
        )

        # Junior milestone
        self.assertEqual(
            check_credit_milestones(60),
            "Congratulations! You've reached 60 credits - you're a junior!"
        )

        # Senior milestone
        self.assertEqual(
            check_credit_milestones(90),
            "Congratulations! You've reached 90 credits - you're a senior!"
        )

        self.assertEqual(
            check_credit_milestones(120),
            "Congratulations! You've reached 120 credits - you've completed your degree requirements!"
        )


def run_demo():
    """Runs a live demo of TerpTracker functions and prints results to the terminal."""
    print("Welcome to the Terp Tracker!\n")

    # --- Build some sample semesters ---
    sem1 = Semester("Fall 2024")
    sem1.add_course(Course("INST126", 3, "A"))
    sem1.add_course(Course("MATH140", 4, "B+"))
    sem1.add_course(Course("ENGL101", 3, "A-"))
    sem1.add_course(Course("HIST200", 3, "B"))

    sem2 = Semester("Spring 2025")
    sem2.add_course(Course("INST201", 3, "A"))
    sem2.add_course(Course("CMSC131", 4, "B+"))
    sem2.add_course(Course("PSYC100", 3, "A-"))
    sem2.add_course(Course("COMM107", 3, "B+"))

    semesters = [sem1, sem2]

    # --- Display full academic summary ---
    display_summary(semesters)

    # --- Credit milestone check ---
    total_credits = sum(s.get_total_credits() for s in semesters)
    milestone = check_credit_milestones(total_credits)
    if milestone:
        print(milestone)
    else:
        print(f"No milestone reached yet ({total_credits} credits so far).")

    # --- Finals calculator ---
    print("\n--- Finals Calculator ---")
    current_gpa = calculate_cumulative_gpa(semesters)
    target_gpa = 3.5
    remaining_credits = 30

    needed = finals_calculator(current_gpa, total_credits, target_gpa, remaining_credits)
    if needed is not None:
        print(f"To reach a {target_gpa} GPA, you need a {needed} GPA over your next {remaining_credits} credits.")

    # --- Save and reload data ---
    print("\n--- Saving Data ---")
    save_data(semesters)

    print("\n--- Loading Data ---")
    loaded_semesters = load_data()
    print(f"Successfully loaded {len(loaded_semesters)} semester(s).")

    print("\n--- Now Running Unit Tests ---\n")


if __name__ == "__main__":
    run_demo()
    unittest.main(verbosity=2)

