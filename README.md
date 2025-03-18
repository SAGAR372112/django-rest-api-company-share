This project is a Django REST Framework (DRF)-based API for managing company shares and member purchases. 
It ensures that members can buy shares within their individual limits while also enforcing the company's overall share limit. 
If limits are exceeded, appropriate notifications are provided.

Features
Company Share Management: Defines the total number of shares available.
Member Share Limits: Each member has a predefined limit on how many shares they can purchase.
Dynamic Limit Handling:
    If the company's total share limit is exceeded, the limit is raised.
    If a member tries to buy shares beyond their personal limit, an "Exceed Limit" message is returned.
RESTful Endpoints:
    Register companies and members.
    Buy shares (with validation for individual and company limits).
    View available shares and purchase history.


Tech Stack
Backend: Django & Django REST Framework
Database: PostgreSQL / SQLite
Authentication: Token-based authentication (Optional)
API Documentation: Swagger / DRF Browsable API
This API ensures fair share distribution while allowing the company to manage stock dynamicall
