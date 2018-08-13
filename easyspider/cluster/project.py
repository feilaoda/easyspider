

class ProjectManager(object):
	"""docstring for ProjectManager"""
	def __init__(self, arg):
		super(ProjectManager, self).__init__()
		self.arg = arg
		

	def load_projects(self):
		pass


	def run_projects(self, projects):
		for proj in projects:
			self.run_on_start()


	def do_schedulers(self, projects):
		for proj in projects:
			self.run_scheduler(proj)


	def do_tasks(self, projects):
		for proj in projects:
			