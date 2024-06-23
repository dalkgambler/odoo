{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'category': 'Real Estate/Brokerage',
    'description': """
    This is a new python file to teach the ape behind the PC how it is done
    """,
    # data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        

        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml'
    ],
    
    'installable': True,
    'application': True,
}