import os
"""
	run this to make all the migration, to migrate, and run the server automatically
	
"""
print("""
.........................._ _ _
		__      _(_) | |
		\\ \\ /\\ / / | | |
		 \\ V  V /| | | |
		  \\_/\\_/ |_|_|_|
		[ by: adaomajor ]
	[ github: github.com/adaomajor ]
""")

os.system('python manage.py makemigrations app && python manage.py makemigrations')
os.system('python manage.py migrate app && python manage.py migrate')
os.system('python manage.py runserver 80')