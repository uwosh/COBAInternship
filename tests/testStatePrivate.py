import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStatePrivate(COBAInternshipTestCase):
    """Test private state"""
    
    def afterSetUp(self):
        self.COBAInternshipworkflow = self.portal.portal_workflow['COBAInternshipWorkflow']
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        self.createUsers()
        
        
        
    def test_should_not_be_able_to_create_application_if_not_logged_in(self):
        try:
            self.portal.invokeFactory(type_name='COBAInternship', id='testapplication')
            self.fail()
        except Exception, inst:
            pass
        
        
        
        
    def createPrivateApplication(self):
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")
        app = self.portal['testapplication']
        self.fill_out_application(app)
        self.logout()

        return app
        
        
        
    def test_application_should_be_private_after_creation(self):
        app = self.createPrivateApplication()
        self.assertEquals("COBAInternshipWorkflow", self.portal_workflow.getWorkflowsFor(app)[0].id)
        self.assertEquals("private", self.getState(app))
    
    
    
    def test_should_be_able_to_submit(self):
        app = self.createPrivateApplication()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'submit')
        self.assertEquals('pendingCollegeApproval', self.getState(app))


    def test_should_be_able_to_archive(self):
        app = self.createPrivateApplication()
        self.assertEquals("COBAInternshipWorkflow", self.portal_workflow.getWorkflowsFor(app)[0].id)

        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'submit')
        self.assertEquals('pendingCollegeApproval', self.getState(app))
        self.logout()

        self.login()
        self.portal_workflow.doActionFor(app, "archiveInternship")
        self.assertEquals("archived", self.getState(app))

        self.assertEquals("COBAInternshipWorkflow", self.portal_workflow.getWorkflowsFor(app)[0].id)
        self.assertEquals("archived", self.getState(app))
      



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatePrivate))

    return suite

if  __name__ == '__main__':
    framework()
