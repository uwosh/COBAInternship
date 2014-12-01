# -*- coding: utf-8 -*-
#
# File: wfsubscribers.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andrew Schultz and Josh Klotz"""
__docformat__ = 'plaintext'
from Products.CMFCore.utils import getToolByName
import re
import time
import random
import string
from Products.COBAInternship.utils import *
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone.URLTool import URLTool
isZipCode = re.compile(r'(\d{5})$', re.VERBOSE)
isYear = re.compile(r'(\d{4})$', re.VERBOSE)
timeNow = time.time()



###### Must add the strings (Internship_Director_Email and Enrollment_Email) in the Plone root properties in the ZMI

def getInternshipDirectorEmail(self):
    root = getToolByName(self, 'portal_url')
    root = root.getPortalObject()
    internshipDirectorEmail = root.getProperty("Internship_Director_Email", "schula15@uwosh.edu")
    return internshipDirectorEmail 


def getEnrollmentEmail(self):
    root = getToolByName(self, 'portal_url')
    root = root.getPortalObject()
    enrollmentEmail = root.getProperty("Enrollment_Email", "schula15@uwosh.edu")
    return enrollmentEmail 

        #       'pondellj@uwosh.edu' Jesssie Pondell  Internship Director
        #       'benzm@uwosh.edu'   Micki Benz   Enrollment



###################################################################################

def sendEmailToCollege(obj, event):
    if not event.transition or \
       event.transition.id not in ['submit']:
        return

    validateFields(obj)     ## checks to see if all fields are filled in and filled in correctly
    
    mMsg ="""
Dear Jessie,


There is an internship to review for %s.

Please go to %s to review this internship.
"""

    fullname = obj.getStudentName()
    studentEmail = obj.getStudentEmail()  
    obj_url = obj.absolute_url()
        
    mTo = getInternshipDirectorEmail(obj)
    mFrom = obj.getStudentEmail()
    mSubj = 'Internship Review for %s' % (fullname)

    message = mMsg % (fullname, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)
    
    
    newTitle = '%s Internship' % (fullname)    #### Renames the internship from the generic "Unsubmitted COB Internship" to "[student's name] internship"
    obj.setTitle(newTitle)
    obj.reindexObject()
    

###################################################################################

def sendDenialByCollegeEmail(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition or \
       event.transition.id not in ['denyFromPendingCollegeApproval', 'denyFromPendingCollegeRepproval']:
        return


    mMsg="""
Dear %s,
    
    
Your internship with %s, has been denied by the College of Business Internship Director for the following reason(s):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Internship Director Comment:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If no reason(s) were listed, or if you have specific questions regarding this denial, please contact me immediately.  Feel free to correct or update your application and resubmit it for approval.  You can access your application at %s


For more information or clarification, please contact me immediately.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu
"""
         
    mTo = obj.getStudentEmail()
    mFrom = getInternshipDirectorEmail(obj)
    mSubj= 'Internship Denied by the College of Business'
    internshipTitle = obj.Title()
    
    organizationName = obj.getOrganizationName()    
    reason = obj.getReasonDeniedByCollege()
    otherReason = obj.getOtherReasonDeniedByCollege()
    fullname = obj.getStudentName()
    obj_url = obj.absolute_url()
    newReason = ''

    for x in xrange(len(reason)):
        value = reason[x]
        if x != len(reason) -1:
            value += '\n'
        newReason += value
        
    
    message = mMsg % (fullname, organizationName, newReason, otherReason, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)
    
###################################################################################

def sendRepeatEmailToCollege(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    
    if not event.transition or \
       event.transition.id not in ['submitFromDeniedByCollege']:
        return
       
    validateFields(obj)    ## checks to see if all fields are filled in and filled in correctly
        
    mMsg ="""
Dear Jessie,


%s has made corrections to an internship that was previously denied by the College of Business.

Please go to %s to review this internship.
     """

    mTo = getInternshipDirectorEmail(obj)
    mFrom = obj.getStudentEmail()
    fullname = obj.getStudentName()
    mSubj = 'Resubmitted Internship Review for %s' % (fullname)
    obj_url = obj.absolute_url()

    message = mMsg % (fullname, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)    

###################################################################################

def sendApprovedByCollegeEmail(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition or \
       event.transition.id not in ['submitFromPendingCollegeApproval']:
        return
    
    validateFields(obj)      ## checks to see if all fields are filled in and filled in correctly

    mMsg ="""
Dear %s,


Your %s internship with %s has been approved by the College of Business Internship Director.  
At this time, your internship is awaiting approval from your supervisor at %s.

If possible, please remind your supervisor to check his/her e-mail, so the process can be completed.

You can review your internship status at %s


You will be notified via email when your supervisor has approved your internship. As a reminder you cannot be enrolled in 'Bus 492'  until this has been approved.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu
     """
         
    fullname = obj.getStudentName()
    studentEmail = obj.getStudentEmail()
    studentJobPosition = obj.getStudentJobPosition()
    organizationName = obj.getOrganizationName()
    obj_url = obj.absolute_url()
    internshipTitle = obj.Title()
    
    mTo = studentEmail                                 
    mFrom = getInternshipDirectorEmail(obj)
    mSubj= 'COB Internship is Pending Supervisor Approval'

    message = mMsg % (fullname, studentJobPosition, organizationName,organizationName, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)

###################################################################################

def createSupervisorAccount(obj,event):
    if not event.transition or \
       event.transition.id not in ['submitFromPendingCollegeApproval']: 
        return
    
    
    validateFields(obj)      ## checks to see if all fields are filled in and filled in correctly
    
    
    supervisorTitle = obj.getSupervisorTitle()   
    supervisorFirstName = obj.getSupervisorFirstName()
    supervisorLastName = obj.getSupervisorLastName()
    supervisorName = supervisorFirstName + " " + supervisorLastName
    organizationName = obj.getOrganizationName()
    supervisorEmail = obj.getSupervisorEmail()
    fullname = obj.getStudentName()
    supervisorTitle = obj.getSupervisorTitle()
    obj_url = obj.absolute_url()
    
    
    mTo = getInternshipDirectorEmail(obj), supervisorEmail
    mFrom = getInternshipDirectorEmail(obj)
    mSubj = 'UW-Oshkosh COB Internship for %s' % fullname

    
    
    mMsgA ="""
Dear %s %s,


%s, a UW Oshkosh College of Business student, has submitted an internship for review to the College of Business 
and has given your information as his/her direct supervisor at %s. 

In order for %s to receive credit for this internship, your approval is needed. 

To review the internship:
Go to %s

This is your login information for approving or denying the internship:
Your username is: %s (username is case sensitive)
Your password is: %s (password is case sensitive)

If you would like to change your password, follow the link and click on "forgot your password?"

Please check the accuracy of the information, such as:
Position title
Description
Pay rate
Timeline

By approving this internship, you are verifying the accuracy of the information provided by %s.  In addition, you are agreeing to the responsibilities of an internship supervisor.

These responsibilities can be viewed at:
http://www.uwosh.edu/cob/community/corporate-partners/internships/supervisor-responsibilities


Thank you in advance for your willingness to serve as a supervisor for %s.  For more information or clarification, please contact me immediately.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu
      """  
    
    
    mMsgB ="""
Dear %s %s,


%s, a UW Oshkosh College of Business student, has submitted an internship for review to the College of Business and has given your information as his/her direct supervisor at %s.  In order for %s to receive credit for this internship, your approval is needed.

To review the internship:
Go to %s

Your login information is still stored in our system from a previous student that listed you as a supervisor at %s.

Your username is: %s (username is case sensitive)
If you forgot your password or if you would like to change it, follow the link and click on "forgot your password?"

Please check the accuracy of the information, such as:
Position title
Description
Pay rate
Timeline

By approving this internship, you are verifying the accuracy of the information provided by %s.  In addition, you are agreeing to the responsibilities of an internship supervisor.

These responsibilities can be viewed at:
http://www.uwosh.edu/cob/community/corporate-partners/internships/supervisor-responsibilities


Thank you in advance for your willingness to serve as a supervisor for %s.  For more information or clarification, please contact me immediately.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu
      """
     #emailRegistered = check_member_email(obj.portal_membership, obj.getSupervisorEmail(), registration = 0)
    studentSupervisor = obj.portal_membership.searchMembers('email', obj.getSupervisorEmail())
    if len(studentSupervisor) > 0:
        # found at least one matching user account so take the first one
                supervisorUserName = "%(username)s" % studentSupervisor[0]
 
                group = obj.portal_groups.getGroupById('UwoshSupervisors')     

                group.removeMember(supervisorUserName)   
                group.addMember(supervisorUserName)

                message = mMsgB % (supervisorTitle, supervisorLastName, fullname, organizationName, fullname, obj_url, organizationName, supervisorUserName, fullname, fullname)
                obj.MailHost.send(message, mTo, mFrom, mSubj)

                validateSupervisor(obj) ## calls the method at the bottom of the page to assign the local role

    else:
        
        #  Need to create a new user account for the supervisor
        firstPart = supervisorEmail.split('@')
        username = firstPart[0]

        #  Need to check if the username has a ' . ' (Period)
        if username.find('.') >=0:
            partBeforePeriod = username.split('.')
            username = partBeforePeriod[0] + partBeforePeriod[1]

        #  Need to check if the username has a ' - ' (Hyphen)
        if username.find('-') >=0:
            partBeforeHyphen = username.split('-')
            username = partBeforeHyphen[0] + partBeforeHyphen[0]

        #  Need to check if the username has an ' _ ' (Underscore)
        if username.find('_') >=0:
            partBeforeUnderscore = username.split('_') 
            username = partBeforeUnderscore[0] + partBeforeUnderscore[1]

        #  Need to check if the username starts with a digit
        if username[:1].isdigit():
            username = 'SUP' + username


        # Make username ALL CAPS for easy comparison
        username = username.upper()
        group = obj.portal_groups.getGroupById('UwoshSupervisors')

        # Checks only the users that are part of the 'UwoshSupervisors' group for uniqueness
        number = str(random.randrange(1,10))
        supervisorList = group.getGroupMembers()

        while(username in supervisorList):
            username = username + number

            if len(username) <6:
                username = username + 'Sup'
        ## while(obj.portal_membership.getMemberById(username) in group.getGroupMembers()):
        ##     username = username + number

        ##     if len(username) < 6 :
        ##         username =  username + 'SUP'
                

        # Then adds the user to the group
        group.addMember(username)

        password = obj.portal_registration.generatePassword()
        obj.portal_registration.addMember(id = username, password = password, roles = ['Supervisor'], 
        properties = {
            'fullname': obj.getSupervisorFirstName() + " " + obj.getSupervisorLastName(),
            'username': username,
            'email': obj.getSupervisorEmail(),
                    }
            )
        message = mMsgA % (supervisorTitle, supervisorLastName, fullname, organizationName, fullname, obj_url, username, password, fullname, fullname)
        obj.MailHost.send(message, mTo, mFrom, mSubj)

        validateSupervisor(obj) ## calls the method at the bottom of the page to assign the local role

###################################################################################

def checkResends(obj, event):
    if not event.transition or \
       event.transition.id not in ['emailToSupervisorFromPendingSupervisorApproval']:
        return
    
    IStatusMessage(obj.REQUEST).addStatusMessage('Second notification email sent to supervisor', type='info')  ### this gives a status box confirmation message when the email is sent

    obj_url = obj.absolute_url()
    studentSupervisor = obj.portal_membership.searchMembers('email', obj.getSupervisorEmail())
    supervisorUserName = "%(username)s" % studentSupervisor[0]
    fullname = obj.getStudentName()
    supervisorFirstName = obj.getSupervisorFirstName()
    supervisorLastName = obj.getSupervisorLastName()
    organizationName = obj.getOrganizationName()
    studentEmail = obj.getStudentEmail()
        
    mMsgToSupervisor ="""
Dear %s %s,


This is the second notification request for your approval of an internship for %s, a UW Oshkosh College of Business student, who has submitted an internship to the College of Business at the University of Wisconsin Oshkosh.  %s listed you as his/her direct supervisor at %s.

 %s will not receive credit for his/her internship until you go to %s and approve their submission.

Your username is: %s (username is case sensitive)
If you forgot your password or if you would like to change it, follow the link and click on "forgot your password?"

Please confirm the accuracy of the information provided, such as:
Position title
Description
Timeline
Compensation

By approving the internship, you are indicating your willingness to take on the responsibilities of an internship supervisor.

For more details on your responsibilities as the internship supervisor, please go to the following website: http://www.uwosh.edu/cob/community/corporate-partners/internships/supervisor-responsibilities


Thank you in advance for your willingness to serve as a supervisor for %s.  For more information or clarification, please contact me immediately.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu        
"""
    
    mTo = obj.getSupervisorEmail()
    mFrom = getInternshipDirectorEmail(obj)
    mSubj = 'Second Notification of UW-Oshkosh Internship for %s' % fullname

    message = mMsgToSupervisor % (supervisorFirstName, supervisorLastName, fullname, fullname, organizationName, fullname, obj_url, supervisorUserName, fullname)
    obj.MailHost.send(message, mTo, mFrom, mSubj)
        
        
###################################################################################

def sendDenialBySupervisorEmail(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition or \
       event.transition.id not in ['denyFromPendingSupervisorApproval']:
        return
        
    studentName = obj.getStudentName()
    otherReason = obj.getOtherReasonDeniedBySupervisor()
    supervisorFirstName = obj.getSupervisorFirstName()
    supervisorLastName = obj.getSupervisorLastName()
    supervisorName = supervisorFirstName + " " + supervisorLastName
    supervisorEmail = obj.getSupervisorEmail()
    studentEmail = obj.getStudentEmail()
    organizationName = obj.getOrganizationName()
    fullname = obj.getStudentName()
    obj_url = obj.absolute_url()
    
    validateSupervisor(obj)  ## calls the method at the bottom of the page to assign the local role
    
    mMsg ="""
Dear %s,


Your internship with %s, has been denied by your supervisor for the following reason(s):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Supervisor Comment:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
%s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If no reasons were listed, or if you have questions regarding the denial, please me immediately.

Feel free to make appropriate changes to your application at %s and then resubmit for review.


Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu    
"""
   
    reason = obj.getReasonDeniedBySupervisor()
    newReason = ""

    for x in xrange(len(reason)):
        value = reason[x]
        if x != len(reason) -1:
            value += '\n'
        newReason += str(value)        
        
    mTo =  studentEmail, getInternshipDirectorEmail(obj)
    mFrom = supervisorEmail
    mSubj = 'Internship Denied By Supervisor'
    internshipTitle = obj.Title()
    
    message = mMsg % (studentName, organizationName, newReason, otherReason, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)

###################################################################################

def sendEmailToCollegeAfterSupervisorDenied(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    
    if not event.transition or \
       event.transition.id not in ['submitFromDeniedBySupervisor']:
        return
       
    validateFields(obj)     ## checks to see if all fields are filled in and filled in correctly
        
    fullname = obj.getStudentName()
    obj_url = obj.absolute_url()
        
    mMsg ="""
Dear Jessie,


%s has made corrections to an internship that was denied by his/her supervisor.

Please go to %s to review this internship.
     """
          
    mTo = getInternshipDirectorEmail(obj)
    mFrom = obj.getStudentEmail()
    mSubj = 'Resubmitted Supervisor Denied Internship Review for %s' % (fullname)

    message = mMsg % (fullname, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)
    
###################################################################################

def sendRepeatEmailToCollegeDeniedReapproval(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    
    if not event.transition or \
       event.transition.id not in ['submitFromDeniedByCollegeReapproval']:
        return
       
    validateFields(obj)     ## checks to see if all fields are filled in and filled in correctly
        
    obj_url = obj.absolute_url()
    fullname = obj.getStudentName()
        
    mMsg ="""
Dear Jessie,


%s has made corrections to an internship that was denied by his/her supervisor and then denied by the College of Business.

Please go to %s to review this internship.
     """
         
    mTo = getInternshipDirectorEmail(obj)
    mFrom = obj.getStudentEmail()
    mSubj = 'Resubmitted Denied by College Re-Approval Internship Review for %s' % (fullname)

    message = mMsg % (fullname, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)

###################################################################################

def sendReapprovedByCollegeEmail(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition or \
       event.transition.id not in ['backToPendingSupervisorApproval']:
        return
    ##code-section sendApprovedByCollegeEmail 
    
    
    validateFields(obj)      ## checks to see if all fields are filled in and filled in correctly
    
    
    
    obj_url = obj.absolute_url()
    fullname = obj.getStudentName()
    studentEmail = obj.getStudentEmail()     
    studentJobPosition = obj.getStudentJobPosition()    
    organizationName = obj.getOrganizationName()
    internshipTitle = obj.Title()

    mMsg ="""
Dear %s,


Your %s internship with %s has been re-approved by the College of Business Internship Director.  At this time, your internship is awaiting re-approval from your supervisor at %s.  If possible, please remind your supervisor to check his/her e-mail, so the process can be completed.

You can review your internship status at %s


You will be notified via email when your supervisor has approved your internship. As a reminder, you cannot be enrolled in 'Bus 492' until this has been approved.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu
     """        
    
    mTo = studentEmail
    mFrom = getInternshipDirectorEmail(obj)
    mSubj= 'COB Internship is Pending Supervisor Re-Approval'
  
    message = mMsg % (fullname, studentJobPosition, organizationName,organizationName, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)

###################################################################################

def sendSupervisorSecondReview(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition or \
       event.transition.id not in ['backToPendingSupervisorApproval']:
        return
     
    supervisorTitle = obj.getSupervisorTitle()
    fullname = obj.getStudentName()
    studentEmail = obj.getStudentEmail()     
    supervisorFirst = obj.getSupervisorFirstName()
    supervisorLast = obj.getSupervisorLastName()         
    supervisorEmail = obj.getSupervisorEmail()
    studentSupervisor = obj.portal_membership.searchMembers('email', obj.getSupervisorEmail())
    supervisorUserName = "%(username)s" % studentSupervisor[0]
    internshipTitle = obj.Title()
    obj_url = obj.absolute_url()       
    

    mMsg ="""
Dear %s %s,


%s has made corrections to a University of Wisconsin Oshkosh College of Business internship that you had previously denied.

Your username is: %s (username is case sensitive)
If you forgot your password or if you would like to change it, follow the link and click on "forgot your password?"

Please go to %s to review the internship again.

Please confirm the accuracy of the information provided, such as:
Position title
Description
Timeline
Compensation

By approving the internship, you are indicating your willingness to take on the responsibilities of an internship supervisor.

For more details on your responsibilities as the internship supervisor, please go to the following website: http://www.uwosh.edu/cob/community/corporate-partners/internships/supervisor-responsibilities


If you have any questions about the internship program, please contact me immediately.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu 
     """
            
    mTo = supervisorEmail
    mFrom = getInternshipDirectorEmail(obj)
    mSubj= 'Resubmitted UW-Oshkosh COB Internship for %s' % (fullname)

    message = mMsg % (supervisorTitle, supervisorLast, fullname, supervisorUserName, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)

###################################################################################

def sendApprovalEmail(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    
    if not event.transition or \
        event.transition.id not in ['submitFromPendingSupervisorApproval']:
        return

    validateFields(obj)      ## checks to see if all fields are filled in and filled in correctly

    mMsgToEnrollment ="""
Dear Enrollment,


An internship for %s has been approved by both the College of Business Internship Director and the supervisor, %s.

%s will be enrolled in:
%s in the %s of %s

Student Information:

Student Name: %s
Student Email: %s
Student ID: %s
Student Major: %s
Bus 384 Enrollment: %s
COB Admittance: %s

Supervisor Information:

Supervisor Name: %s %s
Supervisor Title: %s
Organization Name: %s
Supervisor Email: %s
Supervisor Phone Number: %s
Organization Address: %s

Internship Information:

Internship Name: %s
Student Job Title: %s
Start Date (in YYYY/MM/DD format): %s
End Date (in YYYY/MM/DD format): %s
Pay Rate: %s


For more information or clarification, please contact me immediately.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu             
                 """

                                        
      
    mMsgToStudent ="""
Dear %s,


Congratulations!  Your internship has been approved by the College of Business Internship Director and your supervisor.

In the next few days, you will be enrolled in:
%s in the %s of %s.

Shortly before the term begins, you will be able find course information, such as the syllabus and completion requirements, located under the "content" section of D2L.


For more information or clarification, please contact me immediately.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu
               """                  
                              
    supervisorTitle = obj.getSupervisorTitle()                                
    creditOption = obj.getCreditOption()
    studentJobPosition = obj.getStudentJobPosition()    
    studentEmail = obj.getStudentEmail()
    studentID = obj.getStudentID()
    studentName = obj.getStudentName()
    reason = obj.getReasonDeniedBySupervisor()
    fullname = obj.getStudentName()
    studentEmail = obj.getStudentEmail()
    studentID = obj.getStudentID()
    supervisorFirst = obj.getSupervisorFirstName()
    supervisorLast = obj.getSupervisorLastName()
    supervisorName = supervisorFirst + " " + supervisorLast
    supervisorJobTitle = obj.getSupervisorJobTitle()
    supervisorCompany = obj.getOrganizationName()
    supervisorEmail = obj.getSupervisorEmail()
    supervisorPhoneNumber = obj.getSupervisorPhoneNumber()
    supervisorAddress = obj.getOrganizationAddress()
    supervisorCity = obj.getOrganizationCity()
    supervisorState = obj.getOrganizationState()
    supervisorZip = obj.getOrganizationZip()
    supervisorFullAddress = supervisorAddress + " " + supervisorCity + ", " + supervisorState + " " + supervisorZip
    internshipTitle = fullname + "'s Internship"
    startDate = obj.getStartDate()
    endDate = obj.getCompletionDate()
    payRate = obj.getPayRate()
    semesterEnrolled = obj.getSemesterToEnroll()
    yearEnrolled = obj.getYearToEnroll()
    enrolled = semesterEnrolled + " " + yearEnrolled
    obj_url = obj.absolute_url()
    #####################################################
    bus384Enrollment = obj.getStudent384Year()
    COBAdmittance = obj.getStudentCOBYear()
    #####################################################
    major = obj.getStudentDeclareMajor()  
   
    major = ', '.join(major)
    
    
    mTo = getEnrollmentEmail(obj), getInternshipDirectorEmail(obj)
    mFrom = getInternshipDirectorEmail(obj)
    mSubj = 'COB Internship Fully Approved for %s' % fullname

    messageToEnrollment = mMsgToEnrollment % (fullname, supervisorName, fullname, creditOption, semesterEnrolled, yearEnrolled, fullname, studentEmail, studentID, major,bus384Enrollment,COBAdmittance, supervisorTitle,supervisorName, supervisorJobTitle, supervisorCompany, supervisorEmail, supervisorPhoneNumber, supervisorFullAddress, internshipTitle, studentJobPosition, startDate, endDate, payRate)
    messageToStudent = mMsgToStudent % (fullname, creditOption, semesterEnrolled, yearEnrolled)
        
    obj.MailHost.send(messageToEnrollment, mTo, mFrom, mSubj)
    obj.MailHost.send(messageToStudent, studentEmail, getInternshipDirectorEmail(obj), mSubj)

###################################################################################
   
def revokeApprovedInternship(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if not event.transition or \
       event.transition.id not in ['revokeInternship']:
        return
    ##code-section revokeApprovedInternship 
    studentName = obj.getStudentName()
    internshipTitle = obj.Title()
    supervisorCompany = obj.getOrganizationName()
    reason = obj.getReasonDeniedBySupervisor()
    fullname = obj.getStudentName()
    obj_url = obj.absolute_url()
  
    
    mMsg ="""
Dear %s,


Your internship with %s has been revoked.  Please go to %s to view your internship status.


Please contact me immediately for more information on your internship status.

Jessie Pondell
Internship Director for the College of Business
University of Wisconsin-Oshkosh
920-424-3032
pondellj@uwosh.edu                  
"""
    
    mTo = obj.getStudentEmail()
    mFrom = getInternshipDirectorEmail(obj)
    mSubj = 'COB Internship Revoked for %s' % fullname

    message = mMsg % (studentName, supervisorCompany, obj_url)
    obj.MailHost.send(message, mTo, mFrom, mSubj)
   
###################################################################################   
   
class StateError(ValueError):
    """
    Same as ValueError just renamed
    """
    
def validateFields(obj):
    creditOption = obj.getCreditOption()
    semesterToEnroll = obj.getSemesterToEnroll()
    yearToEnroll = obj.getYearToEnroll()
    startDate = obj.getStartDate()
    completionDate = obj.getCompletionDate()
    organizationName = obj.getOrganizationName()
    organizationPhoneNumber = obj.getOrganizationPhoneNumber()
    organizationAddress = obj.getOrganizationAddress()
    organizationCity = obj.getOrganizationCity()
    organizationState = obj.getOrganizationState()
    organizationZip = obj.getOrganizationZip()
    supervisorFirstName = obj.getSupervisorFirstName()
    supervisorLastName = obj.getSupervisorLastName()
    supervisorPhoneNumber = obj.getSupervisorPhoneNumber()
    supervisorEmail = obj.getSupervisorEmail()
    supervisorJobTitle = obj.getSupervisorJobTitle()
    studentName = obj.getStudentName()
    studentAddress = obj.getStudentAddress()
    studentPhoneNumber = obj.getStudentPhoneNumber()
    studentEmail = obj.getStudentEmail()
    studentCity = obj.getStudentCity()
    studentState = obj.getStudentState()
    studentZip = obj.getStudentZip()
    studentDeclareMajor = obj.getStudentDeclareMajor()
    studentGraduationSemester = obj.getStudentGraduationSemester()
    studentGraduationYear = obj.getStudentGraduationYear()
    studentCOBSemester = obj.getStudentCOBSemester()
    studentCOBYear = obj.getStudentCOBYear()
    student384Semester = obj.getStudent384Semester()
    student384Year = obj.getStudent384Year()
    supervisorTitle = obj.getSupervisorTitle()
    studentID = obj.getStudentID()
    studentJobPosition = obj.getStudentJobPosition()
    
    positionDescriptionQuestion1 = obj.getPositionDescriptionQuestion1()
    positionDescriptionQuestion2 = obj.getPositionDescriptionQuestion2()
    positionDescriptionQuestion3 = obj.getPositionDescriptionQuestion3()
    positionDescriptionQuestion4 = obj.getPositionDescriptionQuestion4()
    positionDescriptionQuestion5 = obj.getPositionDescriptionQuestion5()
    
    positionDescriptionQuestion1words = positionDescriptionQuestion1.split()
    positionDescriptionQuestion2words = positionDescriptionQuestion2.split()
    positionDescriptionQuestion3words = positionDescriptionQuestion3.split()
    positionDescriptionQuestion4words = positionDescriptionQuestion4.split()
    positionDescriptionQuestion5words = positionDescriptionQuestion5.split()
    payRate = obj.getPayRate()

        
    errors = []
    
################################################################################################
        # Student Information Errors #    
        
    if studentName is "":
        errors.append({
            'name': 'Student Name',
            'description': 'Not filled in...'
        })
        
    if studentAddress is "":
        errors.append({
            'name': 'Student Address',
            'description': 'Not filled in...'
        })

    if studentCity is "":
        errors.append({
            'name': 'Student City',
            'description': 'Not filled in...'
        })

    if studentState is "":
        errors.append({
            'name': 'Student State',
            'description': 'Not filled in...'
        })
        
    if not isZipCode.search(studentZip):
        errors.append({
            'name': 'Student Zip',
            'description': 'You must fill in a valid student zip code'
        })
       
###################################################################################################
# No errors thrown for major because the checkbox cannot be checked to see if it was filled out
# without messing up the edit screen.  For reasons unknown, putting out an error thrown for the major
# makes the student unable to edit the major and have the change reflected in the view template
###################################################################################################

    if studentEmail is "":
        errors.append({
            'name': 'Student Email',
            'description': 'Not filled in...'
        })

    if studentPhoneNumber is "":
        errors.append({
            'name': 'Student Phone Number',
            'description': 'Not filled in...'
        })

    if studentID is None:
        errors.append({
            'name': 'Student ID',
            'description': 'Not filled in...'
        })
        
    ##if the studentId has more than 7 characters in it, it is an invalid studentID
    if len(studentID) != 7: 
        errors.append({
            'name': 'Student ID',
            'description': 'Student IDs must be 7 numbers in length'
        })
        
    if studentGraduationSemester is None:
        errors.append({
            'name': 'Student Graduation Semester',
            'description': 'Not filled in...'
        })
        
    if not isYear.search(studentGraduationYear):
        errors.append({
            'name': 'Student Graduation Year',
            'description': 'Not a valid year, must be in YYYY format...'
        })
        
    if studentCOBSemester is None:
        errors.append({
            'name': 'Student COB Admission Semester',
            'description': 'Not filled in...'
        })
        
    if not isYear.search(studentCOBYear):
        errors.append({
            'name': 'Student COB Admission Year',
            'description': 'Not a valid year, must be in YYYY format...'
        })
        
    if student384Semester is None:
        errors.append({
            'name': 'Student Bus 384 Completion Semester',
            'description': 'Not filled in...'
        })
        
    if not isYear.search(student384Year):
        errors.append({
            'name': 'Student Bus 384 Completion Year',
            'description': 'Not a valid year, must be in YYYY format...'
        })
        
################################################################################################
        # Internship Site Information Errors #
        
        
    if organizationName is "":
        errors.append({
            'name': 'Organization Name',
            'description': 'Not filled in...'
        })

    if organizationAddress is "":
        errors.append({
            'name': 'Organization Address',
            'description': 'Not filled in...'
        })

    if organizationCity is "":
        errors.append({
            'name': 'Organization City',
            'description': 'Not filled in...'
        })

    if organizationState is "":
        errors.append({
            'name': 'Organization State',
            'description': 'Not filled in...'
        })

    if not isZipCode.search(organizationZip):
        errors.append({
            'name': 'Organization Zip',
            'description': 'You must enter a valid organization zip code'
        })
        
    if organizationPhoneNumber is "":
        errors.append({
            'name': 'Organization Phone Number',
            'description': 'Not filled in...'
        })
               
################################################################################################
        # Internship Information Errors #
        
        
    if payRate is "":
        errors.append({
            'name': 'Pay Rate',
                'description': 'Not filled in...'
        })      
        
    if startDate is None:
        errors.append({
            'name': 'Start Date',
            'description': 'Not filled in...'
        })
    if completionDate is None:
        errors.append({
            'name': 'Completion Date',
            'description': 'Not filled in...'
        })      
        
    if semesterToEnroll is None:
        errors.append({
            'name': 'Semester To Enroll',
            'description': 'Not filled in...'
        })
        
    if not isYear.search(yearToEnroll):
        errors.append({
            'name': 'Year To Enroll',
            'description': 'Not a valid year, must be in YYYY format...'
        })      

    if creditOption is None:
        errors.append({
            'name': 'Credit Option',
            'description': 'Please select a credit option...'
        })
        
################################################################################################
        # Supervisor Information Errors #


    if supervisorTitle is None:
        errors.append({
            'name': 'Supervisor Title',
            'description': 'Not filled in...'
        })

    if supervisorFirstName is "":
        errors.append({
            'name': 'Supervisor First Name',
            'description': 'Not filled in...'
        })
    if supervisorLastName is "":
        errors.append({
            'name': 'Supervisor Last Name',
            'description': 'Not filled in...'
        })

    if supervisorEmail is "":
        errors.append({
            'name': 'Supervisor Email',
            'description': 'Not filled in...'
        })

    if supervisorEmail.find(' ') > -1:
        errors.append({
            'name': 'Supervisor Email',
            'description': 'Supervisor email contains blank spaces'
        })

    if supervisorPhoneNumber is "":
        errors.append({
            'name': 'Supervisor Phone Number',
            'description': 'Not filled in...'
        })

    if supervisorJobTitle is "":
        errors.append({
            'name': 'Supervisor Job Title',
            'description': 'Not filled in...'
        })
        
################################################################################################
        # Position Description Errors #


    if studentJobPosition is "":
        errors.append({
            'name': 'Student Job Title',
            'description': 'Not filled in...'
        })     
                     
    if len(positionDescriptionQuestion1words) < 50:
        errors.append({
            'name': 'Major roles and responsibilities of your internship',
            'description': '"The major roles/responsibilities of your internship" must be a minimum of 50 words'
        })
        
    if len(positionDescriptionQuestion2words) < 1:
        errors.append({
            'name': 'Business skills and knowledge that are essential',
            'description': '"The business skills and knowledge that are essential for this position" must be filled in'
        })
        
    if len(positionDescriptionQuestion3words) < 1:
        errors.append({
            'name': 'Advanced coursework required',
            'description': '"The advanced coursework required for this position" must be filled in'
        })
        
    if len(positionDescriptionQuestion4words) < 50:
        errors.append({
            'name': 'Learning or experiences not yet learned or experienced',
            'description': '"The learning or experiences from this internship that you have not had the opportunity to learn or experience yet" must be a minimum of 50 words'
        })

    if len(positionDescriptionQuestion5words) < 50:
        errors.append({
            'name': 'Relationship to your major or goals',
            'description': '"The description of this position in realtionship to your major or goals" must be a minimum of 50 words'
        })
    
################################################################################################

    if len(errors) > 0:
        raise StateError, errors



######## This method looks up all the users in the system.  If an email address in the system matches that of an email
######## that a student put down for their supervisor (which must happen because a supervisor account is created if one
######## doesn't already exist), then that specific supervisor is assigned the local role of "ValidSupervisor."

def validateSupervisor(obj):
    internship = obj
    COBAInternship = internship.aq_inner  #### use aq_parent if you want all the members with the local role to have access
    studentSupervisor = obj.portal_membership.searchMembers('email', obj.getSupervisorEmail())
    supervisorEmailName = "%(email)s" % studentSupervisor[0]
    if obj.getSupervisorEmail() == supervisorEmailName:
        portal_membership = getToolByName(obj, 'portal_membership')
        supervisorUserName = "%(username)s" % studentSupervisor[0]
        COBAInternship.manage_addLocalRoles(supervisorUserName, ['ValidSupervisor'])
        COBAInternship.reindexObject()


####### The method below is not used

def getReviewState(self):
    status = self.portal_workflow.getStatusOf('COBAInternshipWorkflow', self)
    reviewState = status['review_state']
    if reviewState == ('pendingSupervisorApproval', 'deniedBySupervisor', 'approved'):
        return reviewState
