import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import *

class TestWorkflowsInstalled(COBAInternshipTestCase):
    """Test all workflows"""
    
    def afterSetUp(self):
        self.workflow = self.portal.portal_workflow['COBAInternshipWorkflow']
    
    def test_added_permissions(self):
        permissions = [ 'Modify portal content', 
                        'View', 
                        'Access contents information', 
                      ]
        for permission in permissions:
            self.failUnless(permission in self.workflow.permissions)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowsInstalled))

    return suite

if  __name__ == '__main__':
    framework()
