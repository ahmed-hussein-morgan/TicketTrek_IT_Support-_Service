# TicketTrek_IT_Support_Service

## Proposed architecture

- ### File tree

  - static (for css/js/image files)
  - templates (html)
  - root `__init__.py` file (package/module imports, assign vars, `create_app()`, blueprints)
  - DataStorage/Models (Database)
  - api (blueprints)
  - role-specific files

## Main functionalities (backend)

- View/Post/Edit/Delete tickets (users)
- View/Resolve/Delete tickets (IT)
- List tickets (users and IT)
- Register/login/modify users/IT tech
