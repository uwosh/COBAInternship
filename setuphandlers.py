# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2008 by []
# Generator: ArchGenXML Version 2.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andrew Schultz and Josh Klotz"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('COBAInternship: setuphandlers')
from Products.COBAInternship.config import PROJECTNAME
from Products.COBAInternship.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
##/code-section HEAD

def isNotCOBAInternshipProfile(context):
    return context.readDataFile("COBAInternship_marker.txt") is None



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotCOBAInternshipProfile(context): return 
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotCOBAInternshipProfile(context): return
    site = context.getSite()
    
#    pg = site.portal_groups
 #   allGroups = pg.getGroupIds()
  #  for c in ('COBAInternship: Supervisors'):
   #     if (c not in allGroups):
    #        pg.addGroup(c)
   # pg.setRolesForGroup('COBAInternship: Supervisors', ['Supervisor',])


##code-section FOOT
##/code-section FOOT
