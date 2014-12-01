
# Import the base test case classes
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFCore.utils import getToolByName

from Testing import ZopeTestCase as ztc
from Products.CMFPlone.tests import PloneTestCase
from Products.PloneTestCase.layer import onsetup

from AccessControl import Unauthorized
from mechanize._mechanize import LinkNotFoundError


import Products.COBAInternship
from Products.COBAInternship.content import COBAInternship

from smtplib import SMTPRecipientsRefused
from DateTime import DateTime

from unittest import TestCase, TestSuite, makeSuite, main
from Products.CMFCore.WorkflowCore import WorkflowException


@onsetup
def setup_COBAInternship():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.COBAInternship)
    fiveconfigure.debug_mode = False
  #  ztc.installProduct('ATVocabularyManager')   #### no vocab used for the COBAInternship
    ztc.installProduct('COBAInternship')
    
setup_COBAInternship()
PloneTestCase.setupPloneSite(products=['ATVocabularyManager', 'COBAInternship'])



class MockTransition:
    id = 'testTransition'

    def __init__(self, id=None):
        if id is not None:
            self.id = id


class MockEvent:
    transition = MockTransition()

    def __init__(self, transitionId=None):
        if transitionId is not None:
            self.transition = MockTransition(id=transitionId)


class MockMailHost(object):
    
    def __init__(self):
        self.messages = []
        self.smtp_host = "smtp.uwosh.edu"
        
    def send(self, message, mto=None, mfrom=None, subject=None, encode=None):
        pass


class COBAInternshipTestCase(PloneTestCase.PloneTestCase):
    """
    Base
    """
    _COBA_users = {'InternshipDirector':['InternshipDirector'],  'Student':['Member'], 
                    'Supervisor':['Supervisor'], 'ValidSupervisor':['ValidSupervisor'], 'Enrollment':['Enrollment']}
                    
    _default_user = 'Student'
    
    
    _all_users = _COBA_users.keys() + [_default_user]
    _default_program = None
    
    
    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.portal.MailHost = MockMailHost()
    
    
    def afterSetUp(self):
        self.acl_users = self.portal.acl_users
        self.portal_workflow = self.portal.portal_workflow
        self.portal_registration = self.portal.portal_registration
        
        self.setDefaultProgram()
        self.createUsers()
        
        self.login()
        self.setRoles(('Manager','Member', 'Owner', 'Supervisor', 'ValidSupervisor', 'InternshipDirector', 'Enrollment'))
        self.logout()
        
    def setDefaultProgram(self):
        self.login()
        self.setRoles(('Manager','Member', 'Owner', 'Supervisor', 'ValidSupervisor', 'InternshipDirector', 'Enrollment'))
        
        programId = self.portal.invokeFactory(  type_name='COBAInternship', 
                                                            id=self.portal.generateUniqueId(), 
                                                            title="testapplication")
        
        self._default_program = self.portal[programId]
        self.logout()
    
       
    
    def createUsers(self):
        self.login()
        self.setRoles(('Manager', 'Owner', 'Member', 'Owner', 'Supervisor', 'ValidSupervisor', 'InternshipDirector', 'Enrollment'))
         
        self.portal.acl_users._doAddUser(self._default_user, 'password', ['Manager', 'Owner', 'Member', 'Owner', 'Supervisor', 'InternshipDirector', 'ValidSupervisor', 'Enrollment'], []) 
        self.portal.portal_membership.getMemberById(self._default_user).setMemberProperties({'email': self._default_user + '@COBA.com'})
        
        for user, roles in self._COBA_users.iteritems():
            self.portal.acl_users._doAddUser(user, 'password', roles, [])
            self.portal.portal_membership.getMemberById(user).setMemberProperties({'email': user + '@COBA.com'})
        	
        self.logout()
        
         
        
        
        
    def mockMailHost(self):
        self.portal.MailHost = MockMailHost()
         
         
    def assertHasTheseRoles(self, transition, roles):
        map(lambda role: self.failUnless(role in roles ), transition.getGuard().roles)
        self.failUnless(len(roles) == len(transition.getGuard().roles))
        
    def hasTheseTransitions(self, state, desiredTransitions):
        map(lambda transition: self.failUnless(transition in desiredTransitions ), state.getTransitions())
        self.failUnless(len(desiredTransitions) == len(state.getTransitions()))

    def hasPermissionRoles(self, state, permission, desired_roles):
        for role in state.getPermissionInfo(permission)['roles']:
            self.failUnless(role in desired_roles)
    
    def fill_out_application(self, app):
		app.setCreditOption("Bus 492, 0 Credits (Business Internship)") 
		app.setSemesterToEnroll("Fall") 
		app.setYearToEnroll("2009") 
		app.setStartDate("2009-01-01") 
		app.setCompletionDate("2009-12-30") 
		app.setPayRate("$15.00 an hour")
		
		
		app.setOrganizationName("Grindhouse Cinema") 
		app.setOrganizationPhoneNumber("(920) 777-7777")
		app.setOrganizationAddress("1251 E 110th Street") 
		app.setOrganizationCity("Neenah") 
		app.setOrganizationState("WI") 
		app.setOrganizationZip("54956")
		
		
		app.setSupervisorFirstName("Bill") 
		app.setSupervisorLastName("Klop") 
		app.setSupervisorPhoneNumber("(920) 123-4567")
		app.setSupervisorEmail("aschultz86@hotmail.com")
		app.setSupervisorJobTitle("Director of Sales")
		app.setSupervisorTitle("Mr.")
	   
		
		app.setStudentName("John Doe") 
		app.setStudentID("1234567")
		app.setStudentAddress("1042 Oak Street")
		app.setStudentPhoneNumber("(920) 987-6543")
		app.setStudentEmail("schula15@uwosh.edu")
		app.setStudentCity("Neenah")
		app.setStudentState("WI")
		app.setStudentZip("54956")
		app.setStudentDeclareMajor("Marketing")
		app.setStudentGraduationSemester("Fall")
		app.setStudentGraduationYear("2010")
		app.setStudentCOBSemester("Fall")
		app.setStudentCOBYear("2007")
		app.setStudent384Semester("Spring")
		app.setStudent384Year("2007")
		app.setStudentJobPosition("Marketing Intern")
		
		
		app.setPositionDescriptionQuestion1("a a a a a a a a a a a a a a a a aa a a a a a a a a a a a a a a a aa a a a a a a a a  a aa a a a a a a aa a a a a a a a a a a a a a a a a a a a a a a a a a a")
		app.setPositionDescriptionQuestion2("a a a a a a a a")
		app.setPositionDescriptionQuestion3("a a a a a a a a")
		app.setPositionDescriptionQuestion4("a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a")
                app.setPositionDescriptionQuestion5("a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a")
   
   
   
    def getState(self, obj):
        return self.portal_workflow.getInfoFor(obj, 'review_state', None)
             
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(COBAInternshipTestCase))
    return suite
    
if __name__ == '__main__':
    framework()
