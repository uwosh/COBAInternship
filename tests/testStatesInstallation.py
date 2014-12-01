import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.COBAInternship.tests.COBAInternshipTestCase import COBAInternshipTestCase, MockMailHost
from Products.CMFCore.WorkflowCore import WorkflowException

class TestStatesInstalled(COBAInternshipTestCase):
    """Test all workflows"""
    
    def afterSetUp(self):
        self.states = self.portal.portal_workflow['COBAInternshipWorkflow']['states']
 
############################################################# 
            
    def test_private_workflow(self):
        self.failUnless('private' in self.states.objectIds())
        state = self.states['private']

        self.hasTheseTransitions(state, ['submit', 'archiveInternship'])
        
    def test_private_permissions(self):
        state = self.states['private']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['Owner', 'InternshipDirector', 'Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])

#############################################################
    
    def test_pendingCollegeApproval_workflow(self):
        self.failUnless('pendingCollegeApproval' in self.states.objectIds())
        state = self.states['pendingCollegeApproval']

        self.hasTheseTransitions(state, ['submitFromPendingCollegeApproval', 'denyFromPendingCollegeApproval', 'revokeInternship', 'archiveInternship', 'sendToShortcut'])
        
    def test_pendingCollegeApproval_permissions(self):
        state = self.states['pendingCollegeApproval']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])    
        
#############################################################
    
    def test_deniedByCollege_workflow(self):
        self.failUnless('deniedByCollege' in self.states.objectIds())
        state = self.states['deniedByCollege']

        self.hasTheseTransitions(state, ['submitFromDeniedByCollege', 'revokeInternship', 'archiveInternship'])
        
    def test_deniedByCollege_permissions(self):
        state = self.states['deniedByCollege']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector', 'Owner','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])        
 
 #############################################################
 
    def test_pendingSupervisorApproval_workflow(self):
        self.failUnless('pendingSupervisorApproval' in self.states.objectIds())
        state = self.states['pendingSupervisorApproval']

        self.hasTheseTransitions(state, ['submitFromPendingSupervisorApproval', 'denyFromPendingSupervisorApproval', 'revokeInternship', 'emailToSupervisorFromPendingSupervisorApproval', 'archiveInternship'])
        
    def test_pendingSupervisorApproval_permissions(self):
        state = self.states['pendingSupervisorApproval']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector', 'ValidSupervisor','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector', 'ValidSupervisor','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector', 'ValidSupervisor','Manager'])        
 
 #############################################################
  
    def test_deniedBySupervisor_workflow(self):
        self.failUnless('deniedBySupervisor' in self.states.objectIds())
        state = self.states['deniedBySupervisor']

        self.hasTheseTransitions(state, ['submitFromDeniedBySupervisor', 'revokeInternship', 'archiveInternship'])
        
    def test_deniedBySupervisor_permissions(self):
        state = self.states['deniedBySupervisor']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector', 'Owner','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector', 'ValidSupervisor','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector', 'ValidSupervisor','Manager'])        
 
 ############################################################# 
    
    def test_pendingCollegeReapproval_workflow(self):
        self.failUnless('pendingCollegeReapproval' in self.states.objectIds())
        state = self.states['pendingCollegeReapproval']

        self.hasTheseTransitions(state, ['denyFromPendingCollegeRepproval', 'backToPendingSupervisorApproval', 'revokeInternship', 'archiveInternship'])
        
    def test_pendingCollegeReapproval_permissions(self):
        state = self.states['pendingCollegeReapproval']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])        
 
 ############################################################# 

    def test_deniedByCollegeReapproval_workflow(self):
        self.failUnless('deniedByCollegeReapproval' in self.states.objectIds())
        state = self.states['deniedByCollegeReapproval']

        self.hasTheseTransitions(state, ['submitFromDeniedByCollegeReapproval', 'revokeInternship', 'archiveInternship'])
        
    def test_deniedByCollegeReapproval_permissions(self):
        state = self.states['deniedByCollegeReapproval']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector', 'Owner','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])        
 
 ############################################################# 
   
    def test_approved_workflow(self):
        self.failUnless('approved' in self.states.objectIds())
        state = self.states['approved']

        self.hasTheseTransitions(state, ['revokeInternship', 'archiveInternship'])
        
    def test_approved_permissions(self):
        state = self.states['approved']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector', 'ValidSupervisor','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector', 'ValidSupervisor','Manager'])        
 
 ############################################################# 

    def test_revoked_workflow(self):
        self.failUnless('revoked' in self.states.objectIds())
        state = self.states['revoked']

        self.hasTheseTransitions(state, ['sendBackToPrivate', 'sendBackToPendingCollegeApproval', 'sendBackToDeniedByCollege', 'sendBackToPendingSupervisorApproval', 'sendBackToDeniedBySupervisor', 'sendBackToPendingCollegeReapproval', 'sendBackToDeniedByCollegeReapproval', 'sendBackToApproved', 'archiveInternship'])
        
    def test_revoked_permissions(self):
        state = self.states['revoked']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'View', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Owner', 'Enrollment', 'InternshipDirector','Manager'])        
 
 ############################################################# 

    def test_archived_workflow(self):
        self.failUnless('archived' in self.states.objectIds())
        state = self.states['archived']

        self.hasTheseTransitions(state, ['sendBackToPrivate', 'sendBackToPendingCollegeApproval', 'sendBackToDeniedByCollege', 'sendBackToPendingSupervisorApproval', 'sendBackToDeniedBySupervisor', 'sendBackToPendingCollegeReapproval', 'sendBackToDeniedByCollegeReapproval', 'sendBackToApproved', 'sendBackToRevoked'])
        
    def test_archived_permissions(self):
        state = self.states['archived']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'View', ['Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Enrollment', 'InternshipDirector','Manager'])        
 
 #############################################################

    def test_shortcut_workflow(self):
        self.failUnless('shortcut' in self.states.objectIds())
        state = self.states['shortcut']

        self.hasTheseTransitions(state, ['sendBackToPendingCollegeApproval', 'submitFromPendingSupervisorApproval'])
        
    def test_shortcut_permissions(self):
        state = self.states['shortcut']
        
        self.hasPermissionRoles(state, 'Modify portal content', ['InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'View', ['Enrollment', 'InternshipDirector','Manager'])
        self.hasPermissionRoles(state, 'Access contents information', ['Enrollment', 'InternshipDirector','Manager'])        
 
 #############################################################
 
 
 
 
 
 

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStatesInstalled))

    return suite

if  __name__ == '__main__':
    framework()