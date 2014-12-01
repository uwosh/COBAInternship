import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase
from Products.CMFCore.WorkflowCore import WorkflowException
import transaction

class TestCOBAInternship(COBAInternshipTestCase):
    """Ensure product is properly installed"""

    def createApp(self):
        self.login(self._default_user)

        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        transaction.commit()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCOBAInternship))

    return suite
    
if  __name__ == '__main__':
    framework()