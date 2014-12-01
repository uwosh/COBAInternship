# -*- coding: UTF-8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# Author: Nik Kim <fafhrd@legco.biz>
__version__ = '$Revision: 1.9 $'[11:-2]




from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFCore import *



def check_member_email(self, email, registration=0):
    members = self.portal_membership.searchMembers('email', email)

    if not registration:
    	member=self.portal_membership.getAuthenticatedMember()
        m = {'username': member.getUserName(),
             'email': member.getProperty('email')}
        if m in members:
            members.remove(m)

    if members:
        return 1
    else:
        return 0



