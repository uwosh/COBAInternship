from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.COBAInternship.config import PROJECTNAME
import interfaces

InternshipFolderSchema = folder.ATBTreeFolderSchema.copy() + atapi.Schema((

))


InternshipFolderSchema['title'].storage = atapi.AnnotationStorage()
InternshipFolderSchema['description'].storage = atapi.AnnotationStorage()


schemata.finalizeATCTSchema(InternshipFolderSchema, folderish=True, moveDiscussion=False)


class InternshipFolder(folder.ATBTreeFolder):
    implements(interfaces.IInternshipFolder,)

    portal_type = 'InternshipFolder'
    schema = InternshipFolderSchema

    title = atapi.ATFieldProperty('title') 
    description = atapi.ATFieldProperty('description')
    

atapi.registerType(InternshipFolder, PROJECTNAME)
