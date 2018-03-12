import pip

def install(package):
	pip.main(['install', package])

def upgrade(package):
	pip.main(['install', '--upgrade', 'pip', package])

if __name__ == '__main__':
	try:
		import flask
	except ImportError:
		print("Installing flask....")
		install('flask')
		print("Flask installed")

	try:
		import requests
	except ImportError:
		print("Installing requests....")
		install('requests')
		print ("Requests installed")

	try:
		import enum
	except ImportError:
		print("Upgrading enum....")
		upgrade('enum34')
		print("Enum upgrade")

	import server
	server.run()