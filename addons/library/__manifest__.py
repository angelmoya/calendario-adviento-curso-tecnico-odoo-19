{
    'name': "Library App",
    'summary': """
        Módulo de gestión de libros y préstamos para fines didácticos.""",
    'description': """
Módulo de ejemplo desarrollado como parte de un curso de desarrollo en Odoo.
        Incluye la gestión básica de:
        - Libros (Creación, Edición).
        - Autores.
        - Préstamos de libros a socios (clientes).
        - Ejemplos de campos simples, relaciones y lógica de negocio (Python).
    """,
    'author': "Angel Moya",
    'website': "https://angelmoya.es",
    'category': 'Customization',
    'version': '19.0.1.0.0',
    'depends': ['sale_management', 'purchase', 'stock', 'account'],
    'data': [
        'views/book_views.xml',
        'views/author_views.xml',
        'views/tag_views.xml',
        'security/library_security.xml',
        'security/ir.model.access.csv',
    ]
}
