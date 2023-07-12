import os
"""
	run this to make all the migration, to migrate, and run the server automatically
	
"""
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')
os.system('python manage.py runserver 80')