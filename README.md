POST /api/posts/
- Create a new post
- Required fields: title, content
- Authentication: Required

GET /api/posts/
- Retrieve a list of posts

Likes Endpoints
- POST /posts/<int:pk>/like/: Like a post.
- POST /posts/<int:pk>/unlike/: Unlike a post.
Notifications Endpoints
- GET /notifications/: Fetch user notifications.
- POST /notifications/<int:pk>/read/: Mark a notification as read.