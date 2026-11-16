import unittest
from datetime import date
from src.task_manager import Status, Task, TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = TaskManager()
        self.manager.create(
            Task(1, "Prepare the report", date(2026, 11, 20), tags=["study"])
        )
        self.manager.create(Task(2, "Check the results", date(2026, 11, 10)))

    def test_create_update_and_list_tasks(self) -> None:
        self.manager.update_title(1, "Update the report")
        self.assertEqual([task.task_id for task in self.manager.list_tasks()], [2, 1])
        self.assertEqual(self.manager.get(1).title, "Update the report")

    def test_reject_empty_title_and_duplicate_id(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.create(Task(3, "  ", date(2026, 11, 25)))
        with self.assertRaises(ValueError):
            self.manager.create(Task(1, "Duplicate", date(2026, 11, 25)))

    def test_status_delete_and_missing_task(self) -> None:
        self.manager.set_status(1, Status.DONE)
        self.assertIs(self.manager.get(1).status, Status.DONE)
        self.manager.delete(1)
        with self.assertRaises(KeyError):
            self.manager.get(1)

    def test_overdue_excludes_completed_and_future_tasks(self) -> None:
        self.manager.set_status(2, Status.DONE)
        self.assertEqual(self.manager.overdue(date(2026, 11, 15)), [])

    def test_set_tags_removes_duplicates_and_blank_values(self) -> None:
        task = self.manager.set_tags(1, [" study ", "", "study", "work"])
        self.assertEqual(task.tags, ["study", "work"])

    def test_invalid_status_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.set_status(1, "Unknown")

    def test_create_trims_title_whitespace(self) -> None:
        self.manager.create(Task(3, "  New task  ", date(2026, 11, 25)))
        self.assertEqual(self.manager.get(3).title, "New task")

    def test_filter_by_status(self) -> None:
        self.manager.set_status(2, Status.DONE)
        self.assertEqual(
            [task.task_id for task in self.manager.filter_by_status(Status.DONE)], [2]
        )

    def test_search_by_title_ignores_case_and_blank_query(self) -> None:
        self.assertEqual(
            [task.task_id for task in self.manager.search_by_title(" REPORT ")], [1]
        )
        self.assertEqual(self.manager.search_by_title("  "), [])

    def test_reject_invalid_status(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.set_status(1, "Unknown")


if __name__ == "__main__":
    unittest.main()
