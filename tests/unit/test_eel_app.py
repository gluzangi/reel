import unittest
import eel
from eel import EelApplication

class TestEelApplication(unittest.TestCase):
    def setUp(self):
        self.app = EelApplication()

    def test_expose(self):
        @self.app.expose
        def test_func():
            return "hello"
        
        self.assertIn("test_func", self.app._exposed_functions)
        self.assertEqual(self.app._exposed_functions["test_func"](), "hello")

    def test_expose_with_name(self):
        @self.app.expose("custom_name")
        def test_func():
            return "world"
        
        self.assertIn("custom_name", self.app._exposed_functions)
        self.assertEqual(self.app._exposed_functions["custom_name"](), "world")

    def test_expose_duplicate_error(self):
        @self.app.expose("dup")
        def f1(): pass

        with self.assertRaises(ValueError):
            @self.app.expose("dup")
            def f2(): pass

    def test_default_app_proxy(self):
        # Reset default app state for test safety if needed, 
        # but here we just test if the proxy works
        if "global_test" in eel._exposed_functions:
            del eel._exposed_functions["global_test"]
            
        @eel.expose("global_test")
        def g_func(): pass
        
        self.assertIn("global_test", eel._exposed_functions)

if __name__ == '__main__':
    unittest.main()
