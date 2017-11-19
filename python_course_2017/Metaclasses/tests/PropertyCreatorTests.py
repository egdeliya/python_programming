from propcreator import PropertyCreator
import unittest

# --------------simple property creator tests-----------------------
class SimplePropertyCreator(metaclass=PropertyCreator):
        def __init__(self, lo):
            self.__x = None
            self.lo = lo
            
        def get_x(self):
            return self.__x
        
        def set_x(self, value):
            if value < self.lo:
                raise ValueError("Value must in condition: {} <= value".format(self.lo))
            self.__x = value

        def del_x(self):
            self.__x = "No more"
            
class TestSimplePropertyCreator(unittest.TestCase):
    
    def setUp(self):
        self.testingClass = SimplePropertyCreator(4)
        
    def test_set_property(self):
        self.testingClass.x = 5
        self.assertEqual(self.testingClass.x, 5,
                         'Set does not work!')
        with self.assertRaises(ValueError):
            self.testingClass.x = self.testingClass.lo - 1
            
    def test_del_property(self):
        del self.testingClass.x
        self.assertEqual(self.testingClass.x, "No more",
                         "Deleter does not work properly!")
        

# --------------inheritance property creator tests-----------------------
class A(metaclass=PropertyCreator):
        pass

class TestPropertyCreatorInheritance(A):
    def __init__(self):
        self._secret_list = []

    def get_x(self):
        self._secret_list.append("get")
        return 0

    def set_x(self, value):
        self._secret_list.append("set")
            
class TestWithInheritance(unittest.TestCase):
               
    def setUp(self):
        self.testingClass = TestPropertyCreatorInheritance()
        
    def test_set_property(self):
        self.testingClass.x = 5
        self.assertEqual(self.testingClass._secret_list, ["set"],
                         'Set does not work!')
        
    def test_get_property(self):
        self.assertEqual(self.testingClass.x, 0,
                         'Get does not work!')
        self.assertEqual(self.testingClass._secret_list, ["get"],
                         'Get does not work!')
        
# --------------partially defined property creator tests-----------------------
class TestPropertyCreatorPartial(metaclass=PropertyCreator):
        def __init__(self):
            self._secret_list = []

        def get_x(self):
            self._secret_list.append("get")
            return 0

        def set_y(self, value):
            self._secret_list.append("set")
            self._y = value
            
class TestPartiallyDefined(unittest.TestCase):
    
            
    #-------test_body-----------        
    def setUp(self):
        self.testingClass = TestPropertyCreatorPartial()
        
    def test_set_property(self):
        self.testingClass.y = 5
        self.assertEqual(self.testingClass._secret_list, ["set"],
                         'Set does not work!')
        
    def test_get_property(self):
        self.assertEqual(self.testingClass.x, 0,
                         'Get does not work!')
        self.assertEqual(self.testingClass._secret_list, ["get"],
                         'Get does not work!')
    
    
    

def suite():
    print('hello')
    suite = unittest.TestSuite()
    suite.addTest(TestSimplePropertyCreator('test_set_property'))
    suite.addTest(TestSimplePropertyCreator('test_del_property'))
    suite.addTest(TestWithInheritance('test_set_property'))
    suite.addTest(TestWithInheritance('test_get_property'))

    #return suite

if __name__ == '__main__':
    #pass
    runner = unittest.TextTestRunner()
    #runner.run(suite())
            
