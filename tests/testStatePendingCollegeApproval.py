import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStatePendingCollegeApproval(COBAInternshipTestCase):
    """Ensure product is properly installed"""


    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        self.createUsers()


    def pendingCollegeApproval(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        
       
        return app


    def test_should_be_able_to_approve_internship(self):
        app = self.pendingCollegeApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'submitFromPendingCollegeApproval')
        self.assertEquals('pendingSupervisorApproval', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_deny_internship(self):
        app = self.pendingCollegeApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'denyFromPendingCollegeApproval')
        self.assertEquals('deniedByCollege', self.getState(app))
        self.logout()
        

    def test_should_be_able_send_the_internship_to_shortcut(self):
        app = self.pendingCollegeApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendToShortcut')
        self.assertEquals('shortcut', self.getState(app))
        self.logout()
        
    
    def test_should_be_able_to_send_back_to_archive(self):
        app = self.pendingCollegeApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'revokeInternship')
        self.assertEquals('revoked', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_revoke(self):
        app = self.pendingCollegeApproval()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'archiveInternship')
        self.assertEquals('archived', self.getState(app))
        self.logout()
        
        
       
    def test_other_should_not_be_able_to_submit_to_college(self):
        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        self.logout()
           
        return app
        
        
        for user in self._all_users:
            if user != 'InternshipDirector' and user != 'Manager' and user != self._default_user:
                self.login(user)
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'submit')
                self.logout()      
       
       
          
    
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatePendingCollegeApproval))

    return suite
    
if  __name__ == '__main__':
    framework()