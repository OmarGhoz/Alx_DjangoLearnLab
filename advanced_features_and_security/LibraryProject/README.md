This document outlines the permissions and groups setup for access control in the Django application.

Permissions
Custom permissions on the Document model:

can_view: Allows viewing documents.
can_create: Allows creating new documents.
can_edit: Allows editing documents.
can_delete: Allows deleting documents.
Groups and Permissions
Admins

Permissions: can_view, can_create, can_edit, can_delete (full access).
Editors

Permissions: can_create, can_edit (create and edit only).
Viewers

Permissions: can_view (view-only access).