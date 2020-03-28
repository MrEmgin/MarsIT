user = User()
user.name = 'Roman'
user.surname = 'Ovcharov'
user.age = 23
user.position = 'Middle engineer'
user.speciality = 'Engineer of ecosystems'
user.address = 'module_2'
user.email = 'roma123@mars.org'
user.hashed_password = '123456'
session.add(user)

user = User()
user.name = 'Denis'
user.surname = 'Bakin'
user.age = 21
user.position = 'Middle engineer'
user.speciality = 'Engineer of technical equipment'
user.address = 'module_3'
user.email = 'MrEmgin@mars.org'
user.hashed_password = '654321'
session.add(user)

user = User()
user.name = 'Mike'
user.surname = 'Johnson'
user.age = 32
user.position = 'Captain'
user.speciality = 'Captain'
user.address = 'module_1'
user.email = 'Marsian@mars.org'
user.hashed_password = '8800555'
session.add(user)

user = User()
user.name = 'Tom'
user.surname = 'Archer'
user.age = 26
user.position = 'Senior engineer'
user.speciality = 'Navigator'
user.address = 'module_1'
user.email = 'Archer@mars.org'
user.hashed_password = '112358'
session.add(user)

job = Jobs()
job.job = 'Deployment of residental modules 1 and 2'
job.team_leader = 3
job.work_size = 15
job.collaborators = '2, 3'
job.is_finished = False
job.start_date = datetime.datetime(2020, 3, 28, 11, 27, 0, 0)
job.end_date = datetime.datetime(2020, 4, 10, 11, 0, 0, 0)
session.add(job)

job = Jobs()
job.job = 'Exploration of mineral resources'
job.team_leader = 1
job.work_size = 24
job.collaborators = '3, 4'
job.is_finished = False
job.start_date = datetime.datetime(2020, 3, 28, 11, 27, 0, 0)
job.end_date = datetime.datetime(2020, 4, 10, 11, 0, 0, 0)
session.add(job)

job = Jobs()
job.job = 'Development of management systems'
job.team_leader = 2
job.work_size = 16
job.collaborators = '1, 4'
job.is_finished = False
job.start_date = datetime.datetime(2020, 3, 28, 11, 27, 0, 0)
job.end_date = datetime.datetime(2020, 4, 10, 11, 0, 0, 0)
session.add(job)

session.commit()
