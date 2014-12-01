Important set up information!

1.)  make the users folder private
2.)  make all other folders public
3.)  limit tabs by clicking on site setup, navigation, un-checking automatically generate tabs



CRITICAL!!!!!!!!!!!!!!

4.)  Add an InternshipFolder, name it "internship-applications-folder"
5.)  Click on the folder, publish it, then click the sharing tab,  check the users can add box,
	 click save
6.)  Go to the ZMI, portal types, InternshipFolder, select COBAInternship from allowed
     content types, then uncheck implicitly addable, finally click save


7.) Go to the root ZMI and go into properties
8.) Add two properties: Internship_Director_Email and Enrollment_Email
9.) Make sure they are both strings and enter in the current internship director email
    and enrollment email in the value box
    
    cobinterns@uwosh.edu
    
    
/@@manage-viewlets to add the tabs

images folder to change main image



Dynamic Groups Predicate Info:

Supervisors:  python: principle.has_role(['Supervisor']) and not principle.has_role(['InternshipDirector'])

UWO Members:  python: principal.getProperty('email').endswith('@uwosh.edu')



For running tests

see the README file in the test folder