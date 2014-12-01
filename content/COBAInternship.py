# -*- coding: utf-8 -*-
#
# File: COBAInternship.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andrew Schultz and Josh Klotz"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.COBAInternship.config import * 
from Products.COBAInternship.content.ReadOnlyRichWidget import *


# version is of August 3 at 12:17pm


##code-section module-header #fill in your manual code here
##/code-section module-header


copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()  
copied_fields['title'].write_permission = "Manage Site" 
copied_fields['title'].read_permission = "Manage Site"
copied_fields['title'].widget.label = "Internship Name"
copied_fields['title'].widget.description = "Set automatically"		
copied_fields['title'].default = "Unsubmitted COB Internship"  #### generic name of all internships in the private state (students cannot edit the name)
copied_fields['title'].visible = False                         #### when the internships are submitted they get a new name (see private state event in wfsubscribers)
copied_fields['title'].searchable = 1



schema = Schema((

     TextField(
        name='studentInstructions1',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        default="""
        <h1>Student Instructions</h1>
        <p>1.)  Clicking save <b>will NOT</b> submit your application to your internship director, it only saves the form for future revisions.</p>
        <p>2.)  Make sure to fill out all fields.</p>
        <p>&nbsp;</p>
        <h3>After you are finished entering items into the fields</h3>
        <p>1.) Click the <b>save button</b> at the bottom of the screen.</p>
        <p>2.) You will then be redirected to a different page.</p>
        <p>3.) On the new page, you can edit your information again or submit your application to the College of Business.</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>""",
        widget=ReadOnlyRichWidget(
            label='studentInstructions1',
            label_msgid='COBAInternship_label_studentInstructions1',
            i18n_domain='COBAInternship',
        ),
       default_output_type='text/html',
       modify="Manager",
       write_permission="COBAInternship: Edit Form",
    ),
    
    
################################################################################################
	# Student Information #
	
	
    StringField(
        name='studentName',
        widget=StringField._properties['widget'](
            label="Student Name",
            label_msgid='COBAInternship_label_studentName',
            i18n_domain='COBAInternship',
        ),
        required=0,
        searchable=1,
        default_method="getStudentNameDefault",
        write_permission="COBAInternship: College Deny", 
    ),
    StringField(
        name='studentAddress',
        widget=StringField._properties['widget'](
            label="Student Address",
            description="Local Address",
            label_msgid='COBAInternship_label_studentAddress',
            i18n_domain='COBAInternship',
        ),
        required=0,
        searchable=1,
        write_permission="COBAInternship: Edit Form",
    ),
    StringField(
        name='studentCity',
        widget=StringField._properties['widget'](
            label="Student City",
            description="Local City",
            label_msgid='COBAInternship_label_studentCity',
            i18n_domain='COBAInternship',
        ),
        required=0,
        searchable=1,
        write_permission="COBAInternship: Edit Form",
    ),
    StringField(
        name='studentState',
        widget=StringField._properties['widget'](
            label="Student State",
            description="Local State",
            label_msgid='COBAInternship_label_studentState',
            i18n_domain='COBAInternship',
        ),
        required=0,
        searchable=1,
        default="WI",
        write_permission="COBAInternship: Edit Form",  
    ),
    StringField(
        name='studentZip',
        widget=StringField._properties['widget'](
            label="Student Zip Code",
            description="Local Zip Code",
            label_msgid='COBAInternship_label_studentZip',
            i18n_domain='COBAInternship',
        ),
        required=0,
        searchable=1,
        write_permission="COBAInternship: Edit Form",
    ),
    StringField(
        name='studentDeclareMajor',
        widget=MultiSelectionWidget(
            label="Declared Major",
            description="Select all that apply",
            label_msgid='COBAInternship_label_studentDeclareMajor',
            description_msgid='COBAInternship_help_studentDeclareMajor',
            i18n_domain='COBAInternship',
            format='checkbox',
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        multiValued=1,
        vocabulary=['Accounting','Supply Chain and Operations Management','Information Systems','Marketing','Economics','Finance','Human Resources Management','Other'],
    ),
    StringField(
        name='studentEmail',
        widget=StringField._properties['widget'](
            label="Student E-Mail Address",
            label_msgid='COBAInternship_label_studentEmail',
            i18n_domain='COBAInternship',
        ),
        required=0,
        searchable=1,
        default_method="getStudentEmailDefault",
        write_permission="COBAInternship: College Deny", 
    ),
    StringField(
        name='studentPhoneNumber',
        widget=StringField._properties['widget'](
            label="Student Phone Number",
            description="Phone Number must include area code. Examples include: (555) 555-5555 or 555-555-5555",
            label_msgid='COBAInternship_label_studentPhoneNumber',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        searchable=1,
    ),
    StringField(
        name='studentID',
        widget=StringField._properties['widget'](
        	description= "Must be 7 digits",
            label="Student ID",
            label_msgid='COBAInternship_label_studentID',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        searchable=1,
    ),
    StringField(
        name='studentGraduationSemester',
        widget=SelectionWidget(
            label="Estimated Semester of Graduation",
            label_msgid='COBAInternship_label_studentGraduationSemester',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
        required=False,
        searchable=True,
        vocabulary=['Fall','Spring','Summer'],
    ),
    StringField(
        name='studentGraduationYear',
        widget=StringField._properties['widget'](
            label="Estimated Graduation Year",
            label_msgid='COBAInternship_label_studentGraduationYear',
            i18n_domain='COBAInternship',
            description="Must be in YYYY format",
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        searchable=1,
    ),
    StringField(
        name='studentCOBSemester',
        widget=SelectionWidget(
            label="Semester Admitted To The College of Business",
            label_msgid='COBAInternship_label_studentCOBSemester',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
        required=False,
        searchable=True,
        vocabulary=['Fall','Spring','Summer'],
    ),
    StringField(
        name='studentCOBYear',
        widget=StringField._properties['widget'](
            label="Year Admitted To The College of Business",
            label_msgid='COBAInternship_label_studentCOBYear',
            i18n_domain='COBAInternship',
            description="Must be in YYYY format",
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        searchable=1,
    ),
    StringField(
        name='student384Semester',
        widget=SelectionWidget(
            label="Semester Business 384 Completed",
            label_msgid='COBAInternship_label_student384Semester',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
        required=False,
        searchable=True,
        vocabulary=['Fall','Spring','Summer'],
    ),
    StringField(
        name='student384Year',
        widget=StringField._properties['widget'](
            label="Year Business 384 Completed",
            label_msgid='COBAInternship_label_student384Year',
            i18n_domain='COBAInternship',
            description="Must be in YYYY format",
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        searchable=1,
    ),
    
    
################################################################################################
	# Internship Site Information #


    StringField(
        name='organizationName',
        widget=StringField._properties['widget'](
            label="Organization Name",
            label_msgid='COBAInternship_label_organizationName',
            i18n_domain='COBAInternship',
            populate=1,
        ),
        required=0,
        searchable=1,
        write_permission="COBAInternship: Edit Form",
    ),
    StringField(
        name='organizationAddress',
        widget=StringField._properties['widget'](
            label="Organization Address",
            label_msgid='COBAInternship_label_organizationAddress',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
    ),
    StringField(
        name='organizationCity',
        widget=StringField._properties['widget'](
            label="Organization City",
            label_msgid='COBAInternship_label_organizationCity',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
    ),
    StringField(
        name='organizationState',
        widget=StringField._properties['widget'](
            label="Organization State",
            label_msgid='COBAInternship_label_organizationState',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
        default="WI",
       
    ),
    StringField(
        name='organizationZip',
        widget=StringField._properties['widget'](
            label="Organization Zip Code",
            label_msgid='COBAInternship_label_organizationZip',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        searchable=1,
    ),
    StringField(
        name='organizationPhoneNumber',
        widget=StringField._properties['widget'](
            label="Organization Phone Number",
            description="Phone Number must include area code. Examples include: (555) 555-5555 or 555-555-5555",
            label_msgid='COBAInternship_label_organizationPhoneNumber',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
    ),


################################################################################################
	# Internship Information #


    StringField(
        name='payRate',
        widget=StringField._properties['widget'](
            label="Pay Rate",
            description="Please specify if the wage is hourly, on a salary, or volunteer.  If you are being paid, please specify the amount and if it is per hour, per month, etc...",
            label_msgid='COBAInternship_label_payRate',
            description_msgid='COBAInternship_help_payRate',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
    ), 
    DateTimeField(
        name='startDate',
        widget=DateTimeField._properties['widget'](
            label="Start Date",
            show_hm=False,
            starting_year='2010', #First year to show up in the drop down menu.
            ending_year='2025', #Last year to show up in the drop down menu.
            
            #When both the starting_year and ending_year are used, you get a more defined range
            #for the drop down menu.
            					
            description="Enter the date you will begin this internship",
            label_msgid='COBAInternship_label_startDate',
            description_msgid='COBAInternship_help_startDate',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
    ),
    DateTimeField(
        name='completionDate',
        widget=DateTimeField._properties['widget'](
            label="Completion Date",
            show_hm=False,
            starting_year='2010', #First year to show up in the drop down menu.
            ending_year='2025', #Last year to show up in the drop down menu.
            
            #When both the starting_year and ending_year are used, you get a more defined range
            #for the drop down menu.            
            
            description="Enter the estimated date of completion for this internship",
            label_msgid='COBAInternship_label_completionDate',
            description_msgid='COBAInternship_help_completionDate',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
    ),
    StringField(
        name='semesterToEnroll',
        widget=SelectionWidget(
            label="Semester of Enrollment",
            label_msgid='COBAInternship_label_semesterToEnroll',
            i18n_domain='COBAInternship',
        ),
        required=0,
        vocabulary=['Fall','Fall Interim','Summer','Spring','Spring Interim'],
        searchable=1,
        write_permission="COBAInternship: Edit Form",    
    ),
    StringField(
        name='yearToEnroll',
        widget=StringField._properties['widget'](
            label="Year To Enroll",
            label_msgid='COBAInternship_label_yearToEnroll',
            i18n_domain='COBAInternship',
            description="Must be in YYYY format",
        ),
        searchable=1,
        write_permission="COBAInternship: Edit Form",        
    ),
    StringField(
        name='creditOption',
        widget=SelectionWidget(
            label="Credit Option",
            description="Which credit option will you be enrolling in?",
            label_msgid='COBAInternship_label_creditOption',
            description_msgid='COBAInternship_help_creditOption',
            i18n_domain='COBAInternship',
        ),
        required=0,
        vocabulary=['Bus 492, 0 Credits (Business Internship)','Bus 492, 3 Credits (Business Internship)','Bus 442, 1 Credit (Full-time Co-op)', 'Bus 442, 3 Credits (Full-Time Co-Op)', 'Bus 442, 6 Credits (Full-Time Co-Op)'],
        searchable=1,
        write_permission="COBAInternship: Edit Form",
    ),
       
       
################################################################################################
	# Supervisor Information #       
       
       
    StringField(
        name='supervisorTitle',
        widget=SelectionWidget(
            label="Supervisor Title",
            label_msgid='COBAInternship_label_supervisorTitle',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        vocabulary=['Mr.','Ms.','Dr.'],
        searchable=1,
    ),
    StringField(
        name='supervisorFirstName',
        widget=StringField._properties['widget'](
            label="Supervisor First Name",
            label_msgid='COBAInternship_label_supervisorFirstName',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
    ),
    StringField(
        name='supervisorLastName',
        widget=StringField._properties['widget'](
            label="Supervisor Last Name",
            label_msgid='COBAInternship_label_supervisorLastName',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
    ),
    StringField(
        name='supervisorEmail',
        widget=StringField._properties['widget'](
            label="Supervisor E-Mail Address",
            description="It is important to enter a valid supervisor e-mail or your internship will be immediately denied",
            label_msgid='COBAInternship_label_supervisorEmail',
            description_msgid='COBAInternship_help_supervisorEmail',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
    ),
    StringField(
        name='supervisorPhoneNumber',
        widget=StringField._properties['widget'](
            label="Supervisor Phone Number",
            description="Phone Number must include area code. Examples include: (555) 555-5555 or 555-555-5555",
            label_msgid='COBAInternship_label_supervisorPhoneNumber',
            i18n_domain='COBAInternship',
        ),
        write_permission="COBAInternship: Edit Form",
        required=0,
        searchable=1,
    ),    
    StringField(
        name='supervisorJobTitle',
        widget=StringField._properties['widget'](
            label="Supervisor Job Title",
            label_msgid='COBAInternship_label_supervisorJobTitle',
            i18n_domain='COBAInternship',
        ),
        required=0,
        write_permission="COBAInternship: Edit Form",
        searchable=1,
    ),       
       
       
################################################################################################
	# Position Description #       
     
   
   StringField(
        name='studentJobPosition',
        widget=StringField._properties['widget'](
            label="Student Job Title",
            label_msgid='COBAInternship_label_studentJobPosition',
            i18n_domain='COBAInternship',
        ),
        required=0,
        searchable=1,
        write_permission="COBAInternship: Edit Form",
    ),
    TextField(
        name='positionDescriptionQuestion1',
        allowable_content_types=('text/plain',),
        widget=RichWidget(
            label="Please provide a position dscription, detailing the main roles/responsibilites of your internship",
            description="(50 word minimum)",
            label_msgid='COBAInternship_label_positionDescriptionQuestion1',
            description_msgid='COBAInternship_help_positionDescriptionQuestion1',
            i18n_domain='COBAInternship',
        ),
        default_output_type='text/html',
        write_permission="COBAInternship: Edit Form",
    ),
    TextField(
        name='positionDescriptionQuestion5',
        allowable_content_types=('text/plain',),
        widget=RichWidget(
            label="How does this position relate to your major and career goals?",
            description="(50 word minimum)",
            label_msgid='COBAInternship_label_positionDescriptionQuestion5',
            description_msgid='COBAInternship_help_positionDescriptionQuestion5',
            i18n_domain='COBAInternship',
        ),
        default_output_type='text/html',
        write_permission="COBAInternship: Edit Form",
    ),    
    TextField(
        name='positionDescriptionQuestion2',
        allowable_content_types=('text/plain',),
        widget=RichWidget(
            label="What business skills and knowledge are essential for this position?",
            label_msgid='COBAInternship_label_positionDescriptionQuestion2',
            i18n_domain='COBAInternship',
        ),
        default_output_type='text/html',
        write_permission="COBAInternship: Edit Form",
    ),
    TextField(
        name='positionDescriptionQuestion3',
        allowable_content_types=('text/plain',),
        widget=RichWidget(
            label="What advanced coursework or which specific College of Business courses will you use in this position",
            label_msgid='COBAInternship_label_positionDescriptionQuestion3',
            i18n_domain='COBAInternship',
        ),
        default_output_type='text/html',
        write_permission="COBAInternship: Edit Form",
    ),
    TextField(
        name='positionDescriptionQuestion4',
        allowable_content_types=('text/plain',),
        widget=RichWidget(
            label="What will you learn or experience from this internship that you have not had the opportunity to learn or experience yet?",
            description="(50 word minimum)",
            label_msgid='COBAInternship_label_positionDescriptionQuestion4',
            description_msgid='COBAInternship_help_positionDescriptionQuestion4',
            i18n_domain='COBAInternship',
        ),
        default_output_type='text/html',
        write_permission="COBAInternship: Edit Form",
    ),


    
    
################################################################################################    
    
    
    TextField(
        name='studentReminderInstructions1',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        default="""
        <h1>Student Reminder</h1>
        <p>1.)  Clicking save <b>will NOT</b> submit your application to your internship director, it only saves the form for future revisions.</p>
        <p>2.)  Make sure to fill out all fields.</p>
        <p>&nbsp;</p>
        <h3>After you are finished entering items into the fields</h3>
        <p>1.) Click the <b>save button</b> at the bottom of the screen.</p>
        <p>2.) You will then be redirected to a different page.</p>
        <p>3.) On the new page, you can edit your information again or submit your application to the College of Business.</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>""",
        widget=ReadOnlyRichWidget(
            label='studentReminderInstructions1',
            label_msgid='COBAInternship_label_studentReminderInstructions1',
            i18n_domain='COBAInternship',
        ),
        default_output_type='text/html',
        modify="Manager",
        write_permission="COBAInternship: Edit Form",
    ),
    
    
################################################################################################    
    
    TextField(
        name='reviewInstructions',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        default="""
        <p>-----------------------------------------------------------------------------------------------------------------------------</p>
        <p>&nbsp;</p>
        <h1>Instructions for Supervisors</h1>
        <p>&nbsp;</p>
        <h3>If you have a reason to deny the internship</h3>
        <p>1.)  Select the appropriate reason and click the <b>save button.</b></p>
        <p>2.)  After you click save, you will be redirected to the view page.</p>
        <p>3.)  On the view page, scroll down to the bottom of the page and click the <b>Deny by Supervisor button</b>.</p>
        <p>&nbsp;</p>
        <h3>If you want to approve the internship</h3>
        <p>1.)  Click the <b>save button</b> or the <b>cancel button.</b></p>
        <p>2.)  After you click save or cancel, you will be redirected to the view page.</p>
        <p>3.)  On the view page, scroll down to the bottom of the page and click the <b>Approve by Supervisor button</b>.</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>""",
        
        widget=ReadOnlyRichWidget(
            label='studentReminderInstructions1',
            label_msgid='COBAInternship_label_studentReminderInstructions1',
            i18n_domain='COBAInternship',
        ),
        default_output_type='text/html',
        modify="Manager",
        read_permission="COBAInternship: Supervisor Deny", 
        write_permission="COBAInternship: Supervisor Deny",
    ),

    
################################################################################################ 

 
    StringField(
        name='reasonDeniedByCollege',
        widget=MultiSelectionWidget(
            label="Reason for College Denying Internship",
            description="Select all that apply",
            label_msgid='COBAInternship_label_reasonDeniedByCollege',
            description_msgid='COBAInternship_label_reasonDeniedbyCollege',
            i18n_domain='COBAInternship',
            format='checkbox',
        ),
        read_permission="COBAInternship: College Deny", 
        write_permission="COBAInternship: College Deny",
        required=0,
        multiValued=1,
        vocabulary=['Student not eligible for internship credit','Incomplete information','Position description not detailed enough','Position does not meet internship requirements', 'Student not admitted to College of Business', 'Student did not complete BUS 384', 'Incorrect semester of enrollment', 'Pay rate not included or specified'],
    ),
    StringField(
        name='otherReasonDeniedByCollege',
        widget=StringField._properties['widget'](
            label="Other Reason(s) for College Denying Internship",
            description="List any other reasons not listed that the internship was denied",
            label_msgid='COBAInternship_label_otherReasonDeniedbyCollege',
            description_msgid='COBAInternship_help_otherReasonDeniedbyCollege',
            i18n_domain='COBAInternship',
        ),
        read_permission="COBAInternship: College Deny", 
        write_permission="COBAInternship: College Deny",    
     ),
     StringField(
        name='reasonDeniedBySupervisor',
        widget=MultiSelectionWidget(
            label="Reason for Supervisor Denying Internship",
            description="Select all that apply",
            label_msgid='COBAInternship_label_reasonDeniedBySupervisor',
            description_msgid='COBAInternship_label_reasonDeniedbySupervisor',
            i18n_domain='COBAInternship',
            format='checkbox',
        ),
        read_permission="COBAInternship: Supervisor Deny", 
        write_permission="COBAInternship: Supervisor Deny",
        required=0,
        multiValued=1,
        vocabulary=['Position not offered to student','Inaccurate position description','Supervisor not able to take on responsibilities', 'Student is no longer working at this organization'],
    ),             
    StringField(
        name='otherReasonDeniedBySupervisor',
        widget=StringField._properties['widget'](
            label="Other Reason(s) for Supervisor Denying Internship",
            description="List any other reasons not listed that the internship was denied",
            label_msgid='COBAInternship_label_otherReasonDeniedBySupervisor',
            description_msgid='COBAInternship_help_otherReasonDeniedBySupervisor',
            i18n_domain='COBAInternship',
        ),
        read_permission="COBAInternship: Supervisor Deny", 
        write_permission="COBAInternship: Supervisor Deny",
    ),
   
   
   
copied_fields['title']   

),

copied_fields['title'] 

)
 
##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

COBAInternship_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class COBAInternship(BaseContent, BrowserDefaultMixin):
    """
    """
    
    portal_type = 'UW-Oshkosh CoB Internship'
    
    schema = COBAInternship_schema
    security = ClassSecurityInfo()
    implements(interfaces.ICOBAInternship)
    meta_type = 'COBAInternship'
    filter_content_types = 0
    global_allow = 1
    _at_rename_after_creation = True

   


    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def getStudentEmailDefault(self):
        pm = self.portal_membership
        m = pm.getAuthenticatedMember()
        if m <> 'Anonymous User':
            return m.getProperty('email', '')
            
    def getStudentNameDefault(self):
        pm = self.portal_membership
        m = pm.getAuthenticatedMember()
        if m <> 'Anonymous User':
            return m.getProperty('fullname', '')
    
    def getReviewState(self):
        status = self.portal_workflow.getStatusOf('COBAInternshipWorkflow', self)
        reviewState = status['review_state']
        return reviewState
            
            
    def getReviewStateTitle(self):
    	reviewState = self.getReviewState()
    	reviewStateTitle = self.portal_workflow.getTitleForStateOnType(reviewState, 'UW-Oshkosh CoB Internship')
        return reviewStateTitle        
            




registerType(COBAInternship, PROJECTNAME)
# end of class COBAInternship

##code-section module-footer #fill in your manual code here
##/code-section module-footer
