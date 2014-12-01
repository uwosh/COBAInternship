import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase
from Products.CMFCore.WorkflowCore import WorkflowException

class TestCOBAInternshipProgram(COBAInternshipTestCase):
    """Ensure product is properly installed"""

    def create_program(self):
        self.login()
        self.setRoles(('Manager', 'Owner'))
    
        programId = self.portal.invokeFactory(  type_name='COBAInternshipProgram', 
                                                        id=self.portal.generateUniqueId(), 
                                                        title="test", 
                                                        )
    

        self.logout()
        
        return self.portal[programId]
        


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCOBAInternshipProgram))

    return suite
    
if  __name__ == '__main__':
    framework()