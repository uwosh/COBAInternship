import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStatePendingSupervisorApproval(COBAInternshipTestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        
        self.createUsers()

    def pendingSupervisorApproval(self):

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



    def test_should_be_able_to_approve_supervisor_internship_director(self):
        app = self.pendingSupervisorApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'submitFromPendingSupervisorApproval')
        self.assertEquals('approved', self.getState(app))
        self.logout()



    def test_should_be_able_to_approve_supervisor(self):
        app = self.pendingSupervisorApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'submitFromPendingSupervisorApproval')
        self.assertEquals('approved', self.getState(app))
        self.logout()


    def test_should_be_able_to_deny_internship_director(self):
        app = self.pendingSupervisorApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'denyFromPendingSupervisorApproval')
        self.assertEquals('deniedBySupervisor', self.getState(app))
        self.logout()
        


    def test_should_be_able_to_deny_supervisor(self):
        app = self.pendingSupervisorApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'denyFromPendingSupervisorApproval')
        self.assertEquals('deniedBySupervisor', self.getState(app))
        self.logout()



    def test_should_be_able_to_send_second_email_to_supervisor(self):
        app = self.pendingSupervisorApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'emailToSupervisorFromPendingSupervisorApproval')
        self.assertEquals('pendingSupervisorApproval', self.getState(app))
        self.logout()



    def test_should_be_able_to_revoke(self):
        app = self.pendingSupervisorApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'revokeInternship')
        self.assertEquals('revoked', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_archive(self):
        app = self.pendingSupervisorApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'archiveInternship')
        self.assertEquals('archived', self.getState(app))
        self.logout()
        
        
   
        
    def test_other_should_not_be_able_to_submit_for_supervisor_approval(self):
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        
        
        return app

        
        for user in self._all_users:
            if user != 'InternshipDirector' and user != 'Manager':
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'submitFromPendingCollegeApproval')
                self.logout()           
        
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatePendingSupervisorApproval))

    return suite
    
if  __name__ == '__main__':
    framework()