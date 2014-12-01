import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStateArchived(COBAInternshipTestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration

        self.createUsers()

    def archived(self):

        self.login(self._default_user)
        self.portal.invokeFactory(type_name="COBAInternship", id="testapplication")

        app = self.portal['testapplication']

        self.fill_out_application(app)
        self.portal_workflow.doActionFor(app, 'submit')
        self.logout()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'archiveInternship')
        self.logout()

        return app

    def test_should_be_able_to_send_back_to_private(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToPrivate')
        self.assertEquals('private', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_send_back_to_pendingCollegeApproval(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToPendingCollegeApproval')
        self.assertEquals('pendingCollegeApproval', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_send_back_to_deniedByCollege(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToDeniedByCollege')
        self.assertEquals('deniedByCollege', self.getState(app))
        self.logout()
    
    
    def test_should_be_able_to_send_back_to_pendingSupervisorApproval(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToPendingSupervisorApproval')
        self.assertEquals('pendingSupervisorApproval', self.getState(app))
        self.logout()
        
       
        
    def test_should_be_able_to_send_back_to_deniedBySupervisor(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToDeniedBySupervisor')
        self.assertEquals('deniedBySupervisor', self.getState(app))
        self.logout()
    
    
    
    def test_should_be_able_to_send_back_to_pendingCollegeReapproval(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToPendingCollegeReapproval')
        self.assertEquals('pendingCollegeReapproval', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_send_back_to_deniedByCollegeReapproval(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToDeniedByCollegeReapproval')
        self.assertEquals('deniedByCollegeReapproval', self.getState(app))
        self.logout()
        
        
    def test_should_be_able_to_send_back_to_approved(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToApproved')
        self.assertEquals('approved', self.getState(app))
        self.logout()
    
    
    def test_should_be_able_to_send_back_to_revoked(self):
        app = self.archived()
        
        self.login()
        self.portal_workflow.doActionFor(app, 'sendBackToRevoked')
        self.assertEquals('revoked', self.getState(app))
        self.logout()
        
        
        
    def test_other_should_not_be_able_to_archive(self):
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
                self.assertRaises(WorkflowException, self.portal_workflow.doActionFor, app, 'archiveInternship')
                self.logout()     

    
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStateArchived))

    return suite
    
if  __name__ == '__main__':
    framework()