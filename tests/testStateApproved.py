import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateApproved(COBAInternshipTestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.COBAInternshipworkflow = self.portal.portal_workflow['COBAInternshipWorkflow']
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        self.createUsers()

    def approved(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")
        
        app = self.portal['testapplication']
        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'submitFromPendingCollegeApproval')
        self.logout()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'submitFromPendingSupervisorApproval')
        self.logout()
        
        return app


    def test_application_should_be_in_approved_state(self):
        app = self.approved()
        
        self.assertEquals("approved", self.getState(app))



    def test_should_be_able_to_revoke(self):
        app = self.approved()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'revokeInternship')
        self.assertEquals("revoked", self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_archive(self):
        app = self.approved()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'archiveInternship')
        self.assertEquals("archived", self.getState(app))
        self.logout()
        
        
    def test_other_should_not_be_able_to_approve(self):
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'submitFromPendingCollegeApproval')
        self.logout()
        
        
        return app
        
        for user in self._all_users:
            if user != 'InternshipDirector' and user != 'Manager' and user != 'ValidSupervisor':
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'submitFromPendingSupervisorApproval')
                self.logout()     
 


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateApproved))

    return suite
    
if  __name__ == '__main__':
    framework()
