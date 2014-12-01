import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateDeniedByCollege(COBAInternshipTestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.createUsers()

    def deniedByCollege(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'denyFromPendingCollegeApproval')
        self.logout()

        return app

    def test_should_be_able_to_resubmit_application(self):
        app = self.deniedByCollege()
        
        self.login(self._default_user)
        self.portal_workflow.doActionFor(app, 'submitFromDeniedByCollege')
        self.assertEquals('pendingCollegeApproval', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_resubmit_application_internship_director(self):
        app = self.deniedByCollege()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'submitFromDeniedByCollege')
        self.assertEquals('pendingCollegeApproval', self.getState(app))
        self.logout()
        
        
    
    def test_should_be_able_to_send_back_to_archive(self):
        app = self.deniedByCollege()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'revokeInternship')
        self.assertEquals('revoked', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_revoke(self):
        app = self.deniedByCollege()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'archiveInternship')
        self.assertEquals('archived', self.getState(app))
        self.logout()
        
   
   
    def test_other_should_not_be_able_to_deny_by_college(self):
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
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'denyFromPendingCollegeApproval')
                self.logout()     
    
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateDeniedByCollege))

    return suite
    
if  __name__ == '__main__':
    framework()