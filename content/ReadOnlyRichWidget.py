from Products.Archetypes.Widget import RichWidget
from AccessControl import ClassSecurityInfo

class ReadOnlyRichWidget(RichWidget):
    _properties = RichWidget._properties.copy()
    _properties.update({
        'macro' : "widgets/readonlyrich",
        'modes' : ('view'),
        })

    security = ClassSecurityInfo()
