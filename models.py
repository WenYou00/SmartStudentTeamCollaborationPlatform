"""
models.py - class
"""

import datetime

# ==================== ENUMERATIONS ====================
class TaskStatus:
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Priority:
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

# ==================== CORE CLASSES ====================

class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.notifications = []
        self.created_date = datetime.datetime.now()
    
    def get_user_id(self): return self.user_id
    def get_name(self): return self.name
    def get_email(self): return self.email
    def get_role(self): return "User"
    
    def check_login(self, email, password):
        return email == self.email and password == self.password
    
    def add_notification(self, notification):
        self.notifications.append(notification)
    
    def get_notifications(self):
        return self.notifications
    
    def display_info(self):
        print(f"\n{'='*40}")
        print("USER INFORMATION")
        print(f"{'='*40}")
        print(f"ID: {self.user_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Role: {self.get_role()}")
        print(f"Created: {self.created_date.strftime('%Y-%m-%d')}")


class Student(User):
    student_counter = 1000
    
    def __init__(self, user_id, name, email, password, student_id=None):
        if student_id is None:
            student_id = f"ST{Student.student_counter}"
            Student.student_counter += 1
        
        super().__init__(user_id, name, email, password)
        self.student_id = student_id
        self.teams = []
        self.tasks = []
    
    def get_role(self): return "Student"
    def get_student_id(self): return self.student_id
    def get_teams(self): return self.teams  # ADD THIS METHOD
    def get_tasks(self): return self.tasks
    
    def display_info(self):
        super().display_info()
        print(f"Student ID: {self.student_id}")
        print(f"Teams: {len(self.teams)}")
        print(f"Tasks: {len(self.tasks)}")
        print(f"{'='*40}")


class TeamLeader(Student):
    def __init__(self, user_id, name, email, password, student_id=None):
        super().__init__(user_id, name, email, password, student_id)
        self.managed_teams = []
    
    def get_role(self): return "Team Leader"


class Lecturer(User):
    staff_counter = 100
    
    def __init__(self, user_id, name, email, password, staff_id=None):
        if staff_id is None:
            Lecturer.staff_counter += 1
            staff_id = f"LC{Lecturer.staff_counter}"
        
        super().__init__(user_id, name, email, password)
        self.staff_id = staff_id
        self.supervised_teams = []
    
    def get_role(self): return "Lecturer"
    def get_staff_id(self): return self.staff_id
    def get_teams(self): return self.supervised_teams  # ADD THIS METHOD - FIXED!
    
    def display_info(self):
        super().display_info()
        print(f"Staff ID: {self.staff_id}")
        print(f"Supervised Teams: {len(self.supervised_teams)}")
        print(f"{'='*40}")


class Team:
    team_counter = 0
    
    def __init__(self, team_id=None, name=None, project_title=None):
        if team_id is None:
            Team.team_counter += 1
            team_id = f"TEA{Team.team_counter:03d}"
        
        self.team_id = team_id
        self.name = name if name else f"Team {team_id}"
        self.project_title = project_title if project_title else f"Project {team_id}"
        self.members = []
        self.tasks = []
        self.leader = None
        self.chat_messages = []
        self.meetings = []
        self.created_date = datetime.datetime.now()
    
    def get_id(self): return self.team_id
    def get_name(self): return self.name
    def get_project_title(self): return self.project_title
    def get_members(self): return self.members
    def get_tasks(self): return self.tasks
    def get_leader(self): return self.leader
    def get_chat_messages(self): return self.chat_messages
    def get_meetings(self): return self.meetings
    
    def add_member(self, student):
        if student not in self.members:
            self.members.append(student)
            student.teams.append(self)
            return True
        return False
    
    def remove_member(self, student):
        if student in self.members:
            self.members.remove(student)
            if self in student.teams:
                student.teams.remove(self)
            return True
        return False
    
    def set_leader(self, leader):
        if leader in self.members:
            self.leader = leader
            return True
        return False
    
    def calculate_progress(self):
        if not self.tasks:
            return {'total': 0, 'completed': 0, 'progress': 0}
        
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == TaskStatus.DONE)
        
        return {
            'total': total,
            'completed': completed,
            'progress': (completed / total) * 100 if total > 0 else 0
        }


class Task:
    task_counter = 0
    
    def __init__(self, task_id=None, title=None, description=None, assignee=None, team=None):
        if task_id is None:
            Task.task_counter += 1
            task_id = f"TASK{Task.task_counter:03d}"
        
        self.task_id = task_id
        self.title = title if title else f"Task {task_id}"
        self.description = description if description else f"Description for {task_id}"
        self.assignee = assignee
        self.team = team
        self.status = TaskStatus.TODO
        self.priority = Priority.MEDIUM
        self.deadline = None
        self.created_date = datetime.datetime.now()
        self.comments = []
        self.attachments = []  
        
        if team:
            team.tasks.append(self)
        
        if assignee:
            assignee.tasks.append(self)
    
    def get_id(self): return self.task_id
    def get_title(self): return self.title
    def get_status(self): return self.status
    def get_assignee(self): return self.assignee
    def get_attachments(self): return self.attachments  # ADD THIS METHOD
    
    def add_attachment(self, filename):  # ADD THIS METHOD
        attachment = FileAttachment(filename)
        self.attachments.append(attachment)
        return attachment


class Comment:
    def __init__(self, author, content):
        self.author = author
        self.content = content
        self.timestamp = datetime.datetime.now()


class FileAttachment:
    def __init__(self, filename):
        self.filename = filename
        self.upload_date = datetime.datetime.now()


class Notification:
    notification_counter = 0
    
    def __init__(self, message, user):
        Notification.notification_counter += 1
        self.notification_id = f"NOTIF{Notification.notification_counter:03d}"
        self.message = message
        self.user = user
        self.timestamp = datetime.datetime.now()
        self.is_read = False


class Meeting:
    meeting_counter = 0
    
    def __init__(self, title, team, datetime_obj):
        Meeting.meeting_counter += 1
        self.meeting_id = f"MET{Meeting.meeting_counter:03d}"
        self.title = title
        self.team = team
        self.datetime = datetime_obj
        self.location = "Online"
        team.meetings.append(self)


class ChatMessage:
    message_counter = 0
    
    def __init__(self, sender, team, content):
        ChatMessage.message_counter += 1
        self.message_id = f"MSG{ChatMessage.message_counter:03d}"
        self.sender = sender
        self.team = team
        self.content = content
        self.timestamp = datetime.datetime.now()
        team.chat_messages.append(self)


class Feedback:
    feedback_counter = 0
    
    def __init__(self, sender, receiver, content):
        Feedback.feedback_counter += 1
        self.feedback_id = f"FB{Feedback.feedback_counter:03d}"
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = datetime.datetime.now()


class Report:
    report_counter = 0
    
    def __init__(self, report_type, team, generated_by):
        Report.report_counter += 1
        self.report_id = f"REP{Report.report_counter:03d}"
        self.report_type = report_type
        self.team = team
        self.generated_by = generated_by
        self.generation_date = datetime.datetime.now()
    
    def generate_content(self):
        """Simple report generation"""
        progress = self.team.calculate_progress()
        
        content = f"""
REPORT: {self.report_type}
Team: {self.team.name}
Generated: {self.generation_date.strftime('%Y-%m-%d %H:%M')}
Generated by: {self.generated_by.name}

Progress: {progress['progress']:.1f}%
Total Tasks: {progress['total']}
Completed: {progress['completed']}
Members: {len(self.team.members)}
"""
        return content


# ==================== SYSTEM MANAGER ====================
class SystemManager:
    instance = None
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.initialize()
        return cls.instance
    
    def initialize(self):
        self.users = {}
        self.teams = {}
        self.tasks = {}
        self.current_user = None
        self.setup_demo_data()
    
    def setup_demo_data(self):
        """Setup basic demo data"""
        # Create demo users
        student1 = Student("STU001", "Ali bin Ahmad", "ali@university.edu", "pass123")
        student2 = Student("STU002", "Siti Nurhaliza", "siti@university.edu", "pass456")
        leader = TeamLeader("TLD001", "Ahmad Hassan", "ahmad@university.edu", "leader123")
        lecturer = Lecturer("LEC001", "Dr. Jennifer Smith", "smith@university.edu", "lecturer123")
        
        self.users = {
            "STU001": student1,
            "STU002": student2,
            "TLD001": leader,
            "LEC001": lecturer
        }
        
        # Create demo team
        team1 = Team("TEA001", "Web Development Team", "University Portal System")
        team1.add_member(leader)
        team1.add_member(student1)
        team1.add_member(student2)
        team1.set_leader(leader)
        
        leader.managed_teams.append(team1)
        lecturer.supervised_teams.append(team1)
        
        self.teams = {"TEA001": team1}
        
        # Create demo tasks
        task1 = Task("TASK001", "Design Homepage", "Create UI for homepage", student1, team1)
        task2 = Task("TASK002", "Database Design", "Design MySQL database", student2, team1)
        
        task1.status = TaskStatus.IN_PROGRESS
        task2.status = TaskStatus.DONE
        task1.priority = Priority.HIGH
        
        # Add demo attachment
        task1.add_attachment("design_mockup.png")
        
        self.tasks = {
            "TASK001": task1,
            "TASK002": task2
        }
        
        # Add demo chat message
        self.send_chat_message(leader, team1, "Welcome to the team!")
        
        # Add demo notification
        notification = Notification("Welcome to the platform!", student1)
        student1.notifications.append(notification)
    
    def show_demo_accounts(self):
        print("\n" + "="*60)
        print("Demo Accounts (Use for testing)")
        print("="*60)
        print("\nStudent: ali@university.edu / pass123")
        print("Team Leader: ahmad@university.edu / leader123")
        print("Lecturer: smith@university.edu / lecturer123")
        print("="*60)
    
    def login(self, email, password):
        for user in self.users.values():
            if user.check_login(email, password):
                self.current_user = user
                return user
        return None
    
    def register_student(self, name, email, password):
        for user in self.users.values():
            if user.email == email:
                return None, "Email already registered"
        
        user_id = f"STU{len([u for u in self.users.values() if isinstance(u, Student)]) + 1:03d}"
        student = Student(user_id, name, email, password)
        self.users[user_id] = student
        return student, f"Student ID: {student.student_id}"
    
    def register_lecturer(self, name, email, password): 
        for user in self.users.values():
            if user.email == email:
                return None, "Email already registered"
        
        user_id = f"LEC{len([u for u in self.users.values() if isinstance(u, Lecturer)]) + 1:03d}"
        lecturer = Lecturer(user_id, name, email, password)
        self.users[user_id] = lecturer
        return lecturer, f"Staff ID: {lecturer.staff_id}"
    
    def create_team(self, name, project_title, leader):
        team_id = f"TEA{len(self.teams) + 1:03d}"
        team = Team(team_id, name, project_title)
        team.set_leader(leader)
        team.add_member(leader)
        
        if isinstance(leader, TeamLeader):
            leader.managed_teams.append(team)
        
        self.teams[team_id] = team
        return team
    
    def create_task(self, title, description, assignee, team):
        task_id = f"TASK{len(self.tasks) + 1:03d}"
        task = Task(task_id, title, description, assignee, team)
        self.tasks[task_id] = task
        return task
    
    def send_chat_message(self, sender, team, content):
        return ChatMessage(sender, team, content)
    
    def provide_feedback(self, sender, receiver, content):
        return Feedback(sender, receiver, content)
    
    def create_meeting(self, title, team, datetime_obj):
        return Meeting(title, team, datetime_obj)
    
    def create_report(self, report_type, team, generated_by):
        return Report(report_type, team, generated_by)
    
    def get_available_teams(self, user):
        available = []
        for team in self.teams.values():
            if user not in team.members:
                available.append(team)
        return available