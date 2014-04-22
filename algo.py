import sys

class RevisedDeferredAcceptance:
	
	def __init__(self):
		self.machines = [
			{
				'id': 'A',
				'capacity': 2,
				'preference': ['c', 'a', 'b'],
			},
			{
				'id': 'B',
				'capacity': 1,
				'preference': ['b', 'c'],
			},
		]

		self.jobs = [
			{
				'id': 'a',
				'size': 2,
				'preference': ['A'],
			},
			{
				'id': 'b',
				'size': 1,
				'preference': ['A', 'B'],
			},
			{
				'id': 'c',
				'size': 1,
				'preference': ['B', 'A'],	
			},
		]

		self.matching = []

		self._lastIndex = None

	def run(self):
		self._init_to_free()

		while True:
			j = self._getNextJob()
			if j is None:
				break

			m_id = self._getHeighestRankedMachine_job(j)
			m = self._getById(m_id, self.machines)

			if m['capacity'] >= j['size']:
				self.matching.append((j, m))
				j['free'] = False
				m['capacity'] -= j['size']
			else:
				# find already matched jobs
				matchedJobs = self._getJobsMatched_machine(m)
				sortedMatchedJobs = self._sortJobsByMachinePreference(matchedJobs, m)

				# sequential rejection #
				# Should this not be done in REVERSE ORDER?
				for each in sortedMatchedJobs:
					if m['preference'].index(each) > m['preference'].index(j['id']): # less preference
						matching.remove((each, m))
						m['capacity'] -= each['size']
						best_rejected = each

						if m['capacity'] >= j['size']:
							break
				##

				if m['capacity'] >= j['size']:
					matching.append((j,  m))
					j['free'] = False
					m['capacity'] += j['size']
				else:
					j['free'] = True
					best_rejected = j

				for each in m['preference']:
					if m['preference'].index(each) > m['preference'].index(best_rejected['id']): # less preference
						self._getById(each, self.jobs)['preference'].remove(m['id'])
						m['preference'].remove(each)

	def _init_to_free(self):
		# initialise all jobs and machines to be free
		for each in self.jobs:
			each['free'] = True
		for each in self.machines:
			each['free'] = True

	def _getNextJob(self):
		'''
		Implements: There Exists 'j' who is free, and p(j)<>Empty
		'''
		if self._lastIndex is not None:
			for i in range(self._lastIndex+1, len(self.jobs)):
				if self.jobs[i]['free'] == True:
					if self.jobs[i]['preference']:
						self._lastIndex = i
						return self.jobs[i]
			for i in range(0, self._lastIndex):
				if self.jobs[i]['free'] == True:
					if self.jobs[i]['preference']:
						self._lastIndex = i
						return self.jobs[i]
		else:
			for i in range(0, len(self.jobs)):
				if self.jobs[i]['free'] == True:
					if self.jobs[i]['preference']:
						self._lastIndex = i
						return self.jobs[i]
		return None

	def _getHeighestRankedMachine_job(self, job):
		return job['preference'][0]

	def _getJobsMatched_machine(self, machine):
		result = []
		for each in self.matching:
			if (each[1] == machine['id']):
				result += each[0]
		return result

	def _sortJobsByMachinePreference(self, jobs, machine):
		result = []
		for jobId in machine['preference']:
			for each in jobs:
				if each['id'] == jobId:
					result += job
		return result

	def _getById(self, needle, haystack):
		for each in haystack:
			if each['id'] == needle:
				return each
		return None



