
# Best Practice to adhere to
• Rely on Django’s built-in authentication and reuse AbstractUser.
• Store sensitive config (secrets, keys) in environment variables.
• Keep apps modular (views, models, forms, tests).
• Follow Django’s migrations workflow (makemigrations, migrate).
• Write tests with the Django test framework for each new feature.
• Choose views based on use case:
  - Use FBVs for simple, one-off views with specific logic
  - Use CBVs for common CRUD operations and when inheritance is needed
• Adhere to the 12-Factor App principles for better maintainability.
Use comments to explain lines of code

ALWAYS USE BEST PRACTICES

ALWAYS USE INDUSTRY STANDARD