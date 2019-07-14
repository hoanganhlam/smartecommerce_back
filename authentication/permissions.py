version = '0.0.4'
SYSTEM_PARAM_KEY = 'PERMISSION_VERSION'
file_permissions = {
    'Department': [
        {
            'code': 'VIEW_DEPT',
            'name': 'Can view list department'
        },
        {
            'code': 'CREATE_DEPT',
            'name': 'Can create department'
        },
        {
            'code': 'VIEW_DEPT_DETAIL',
            'name': 'Can view department detail'
        },
        {
            'code': 'EDIT_DEPT',
            'name': 'Can update department'
        },
        {
            'code': 'DELETE_DEPT',
            'name': 'Can delete department'
        }
    ],
    'User': [
        {
            'code': 'VIEW_USER',
            'name': 'Can view user'
        }
    ]
}
