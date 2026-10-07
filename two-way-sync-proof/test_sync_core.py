import unittest
from sync_core import SyncState, Task

class SyncCoreTests(unittest.TestCase):
    def test_new_craft_task_creates_todoist_once_mapping_missing(self):
        s=SyncState()
        a=s.from_craft(Task("c1","Call supplier"))
        self.assertEqual(len(a),1)
        self.assertEqual(a[0].kind,"CREATE_TODOIST")
        self.assertEqual(a[0].source_id,"c1")

    def test_repeat_run_is_idempotent_after_pair_registered(self):
        s=SyncState()
        s.register_pair("c1","t1")
        a=s.from_craft(Task("c1","Call supplier",False),
                       Task("t1","Call supplier",False))
        self.assertEqual(a,[])

    def test_craft_completion_updates_todoist_only_when_state_differs(self):
        s=SyncState(); s.register_pair("c1","t1")
        a=s.from_craft(Task("c1","Call supplier",True),
                       Task("t1","Call supplier",False))
        self.assertEqual([x.kind for x in a],["SET_TODOIST_COMPLETED"])
        self.assertTrue(a[0].completed)

    def test_todoist_completion_updates_craft_only_when_state_differs(self):
        s=SyncState(); s.register_pair("c1","t1")
        a=s.from_todoist(Task("t1","Call supplier",True),
                         Task("c1","Call supplier",False))
        self.assertEqual([x.kind for x in a],["SET_CRAFT_COMPLETED"])
        self.assertTrue(a[0].completed)

    def test_same_title_different_craft_ids_are_not_deduplicated(self):
        s=SyncState()
        a1=s.from_craft(Task("c1","Review"))
        a2=s.from_craft(Task("c2","Review"))
        self.assertEqual(a1[0].kind,"CREATE_TODOIST")
        self.assertEqual(a2[0].kind,"CREATE_TODOIST")
        self.assertNotEqual(a1[0].source_id,a2[0].source_id)

    def test_mapping_collision_is_rejected(self):
        s=SyncState(); s.register_pair("c1","t1")
        with self.assertRaises(ValueError):
            s.register_pair("c1","t2")
        with self.assertRaises(ValueError):
            s.register_pair("c2","t1")

    def test_missing_mapped_counterpart_requests_repair_not_recreation(self):
        s=SyncState(); s.register_pair("c1","t1")
        a=s.from_craft(Task("c1","Review"),None)
        self.assertEqual(a[0].kind,"FETCH_TODOIST_FOR_REPAIR")
        self.assertEqual(a[0].target_id,"t1")

if __name__=="__main__":
    unittest.main()
