"""
ui_system.py 
"""

from models import *
import sys
import datetime

class BaseUI:
    @staticmethod
    def clear_screen():
        print("\n" * 3)
    
    @staticmethod
    def show_header(title):
        BaseUI.clear_screen()
        print("\n" + "="*60)
        print(f"{title:^60}")
        print("="*60)
    
    @staticmethod
    def get_input(prompt, required=True):
        while True:
            user_input = input(f"\n{prompt}: ").strip()
            if not user_input and required:
                print("This field is required.")
                continue
            return user_input
    
    @staticmethod
    def get_choice(max_choice):
        while True:
            try:
                choice = int(input(f"\nEnter choice (1-{max_choice}): "))
                if 1 <= choice <= max_choice:
                    return choice
                print(f"Enter 1-{max_choice}")
            except ValueError:
                print("Enter a number")
    
    @staticmethod
    def show_message(message, msg_type="info"):
        if msg_type == "success":
            print(f"\nSUCCESS: {message}")
        elif msg_type == "error":
            print(f"\nERROR: {message}")
        else:
            print(f"\nINFO: {message}")
    
    @staticmethod
    def press_enter():
        input("\nPress Enter to continue...")


class MainApplication:
    def __init__(self):
        self.system = SystemManager()
    
    def run(self):
        BaseUI.show_header("SMART STUDENT TEAM COLLABORATION PLATFORM")
        print("\nInitializing system...")
        BaseUI.press_enter()
        
        while True:
            BaseUI.show_header("MAIN MENU")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            
            choice = BaseUI.get_choice(3)
            
            if choice == 1:
                self.handle_login()
            elif choice == 2:
                self.register_menu()
            elif choice == 3:
                self.exit_program()
                break
    
    def register_menu(self):
        BaseUI.show_header("REGISTER")
        print("1. Register as Student")
        print("2. Register as Lecturer")
        print("3. Back")
        
        choice = BaseUI.get_choice(3)
        
        if choice == 1:
            self.register_student()
        elif choice == 2:
            self.register_lecturer()
        elif choice == 3:
            return
    
    def handle_login(self):
        # Show demo accounts before login
        self.system.show_demo_accounts()
        
        email = BaseUI.get_input("Email")
        password = BaseUI.get_input("Password")
        user = self.system.login(email, password)
        
        if user:
            BaseUI.show_message(f"Welcome, {user.name}!", "success")
            BaseUI.press_enter()
            self.user_dashboard(user)
        else:
            BaseUI.show_message("Invalid credentials.", "error")
            BaseUI.press_enter()
    
    def register_student(self):
        BaseUI.show_header("REGISTER AS STUDENT")
        name = BaseUI.get_input("Full Name")
        email = BaseUI.get_input("Email")
        password = BaseUI.get_input("Password")
        
        student, message = self.system.register_student(name, email, password)
        
        if student:
            BaseUI.show_message(f"Registered! {message}", "success")
            self.system.current_user = student
            BaseUI.press_enter()
            self.user_dashboard(student)
        else:
            BaseUI.show_message(message, "error")
            BaseUI.press_enter()
    
    def register_lecturer(self):
        BaseUI.show_header("REGISTER AS LECTURER")
        name = BaseUI.get_input("Full Name")
        email = BaseUI.get_input("Email")
        password = BaseUI.get_input("Password")
        
        lecturer, message = self.system.register_lecturer(name, email, password)
        
        if lecturer:
            BaseUI.show_message(f"Registered! {message}", "success")
            self.system.current_user = lecturer
            BaseUI.press_enter()
            self.user_dashboard(lecturer)
        else:
            BaseUI.show_message(message, "error")
            BaseUI.press_enter()
    
    def user_dashboard(self, user):
        role = user.get_role()
        
        if role == "Student":
            self.student_dashboard(user)
        elif role == "Team Leader":
            self.team_leader_dashboard(user)
        elif role == "Lecturer":
            self.lecturer_dashboard(user)
    
    # ==================== STUDENT DASHBOARD ====================
    
    def student_dashboard(self, student):
        while True:
            BaseUI.show_header(f"STUDENT DASHBOARD - {student.name}")
            print(f"Student ID: {student.student_id}")
            print(f"Teams: {len(student.teams)} | Tasks: {len(student.tasks)}")
            print("-"*40)
            
            print("\n1. Task Management")
            print("2. Team Management")
            print("3. Team Discussions")
            print("4. View Meetings") 
            print("5. Provide Feedback to Team")
            print("6. Generate Report")
            print("7. Notifications")
            print("8. Logout")
            
            choice = BaseUI.get_choice(8)
            
            if choice == 1:
                self.task_management(student, False)
            elif choice == 2:
                self.team_management(student, False)
            elif choice == 3:
                self.team_discussions(student)
            elif choice == 4:
                self.view_meetings(student)
            elif choice == 5:
                self.provide_team_feedback(student)
            elif choice == 6:
                self.generate_student_report(student)
            elif choice == 7:
                self.show_notifications(student)
            elif choice == 8:
                self.system.current_user = None
                BaseUI.show_message("Logged out.", "success")
                BaseUI.press_enter()
                break
    
    # ==================== TEAM LEADER DASHBOARD ====================
    
    def team_leader_dashboard(self, leader):
        while True:
            BaseUI.show_header(f"TEAM LEADER DASHBOARD - {leader.name}")
            
            if leader.managed_teams:
                team = leader.managed_teams[0]
                progress = team.calculate_progress()
                print(f"Team: {team.name} ({progress['progress']:.1f}% complete)")
            
            print("-"*40)
            
            print("\n1. Task Management")
            print("2. Team Management")
            print("3. Team Discussions")
            print("4. Manage Meetings")  
            print("5. Provide Feedback to Team")
            print("6. Generate Report")
            print("7. Notifications")
            print("8. Logout")
            
            choice = BaseUI.get_choice(8)
            
            if choice == 1:
                self.task_management(leader, True)
            elif choice == 2:
                self.team_management(leader, True)
            elif choice == 3:
                self.team_discussions(leader)
            elif choice == 4:
                self.manage_meetings(leader)
            elif choice == 5:
                self.provide_team_feedback(leader)
            elif choice == 6:
                self.generate_leader_report(leader)
            elif choice == 7:
                self.show_notifications(leader)
            elif choice == 8:
                self.system.current_user = None
                BaseUI.show_message("Logged out.", "success")
                BaseUI.press_enter()
                break
    
    # ==================== LECTURER DASHBOARD ====================
    
    def lecturer_dashboard(self, lecturer):
        while True:
            BaseUI.show_header(f"LECTURER DASHBOARD - Dr. {lecturer.name}")
            print(f"Supervised Teams: {len(lecturer.supervised_teams)}")
            print("-"*40)
            
            print("\n1. View Team Progress")
            print("2. View Team Discussions")  
            print("3. Provide Feedback to Students")
            print("4. Generate Class Report")
            print("5. Notifications")
            print("6. Logout")
            
            choice = BaseUI.get_choice(6)
            
            if choice == 1:
                self.monitor_progress(lecturer)
            elif choice == 2:
                self.view_team_discussions(lecturer)
            elif choice == 3:
                self.feedback_management(lecturer)
            elif choice == 4:
                self.generate_lecturer_report(lecturer)
            elif choice == 5:
                self.show_notifications(lecturer)
            elif choice == 6:
                self.system.current_user = None
                BaseUI.show_message("Logged out.", "success")
                BaseUI.press_enter()
                break
    
    # ==================== TASK MANAGEMENT DASHBOARD ====================
    
    def task_management(self, user, is_leader):
        while True:
            BaseUI.show_header("TASK MANAGEMENT")
            
            print("1. View My Tasks")
            print("2. View Team Tasks")
            print("3. Update Task Status")
            print("4. Add Comment to Task")
            print("5. Add File Attachment")
            
            if is_leader:
                print("6. Create New Task")
                print("7. Back")
                max_choice = 7
            else:
                print("6. Back")
                max_choice = 6
            
            choice = BaseUI.get_choice(max_choice)
            
            if choice == 1:
                self.show_my_tasks(user)
            elif choice == 2:
                self.show_team_tasks(user)
            elif choice == 3:
                self.update_task_status(user)
            elif choice == 4:
                self.add_task_comment(user)
            elif choice == 5:
                self.add_file_attachment(user)
            elif choice == 6 and is_leader:
                self.create_task(user)
            elif choice == 6 and not is_leader:
                break
            elif choice == 7 and is_leader:
                break
    
    # ==================== TASK MANAGEMENT METHODS ====================
    
    def show_my_tasks(self, user):
        tasks = user.tasks
        BaseUI.show_header("MY TASKS")
        
        if not tasks:
            BaseUI.show_message("No tasks assigned.", "info")
        else:
            for i, task in enumerate(tasks, 1):
                status_text = f"[{task.status}]"
                priority_text = f"({task.priority})" if hasattr(task, 'priority') else ""
                deadline_text = f"Deadline: {task.deadline.strftime('%Y-%m-%d')}" if task.deadline else ""
                attachment_count = len(task.attachments)
                attachment_text = f" [{attachment_count} files]" if attachment_count > 0 else ""
                
                print(f"{i}. {task.title} {status_text} {priority_text}")
                if deadline_text:
                    print(f"   {deadline_text}")
                if attachment_text:
                    print(f"   {attachment_text}")
        
        BaseUI.press_enter()
    
    def show_team_tasks(self, user):
        teams = user.get_teams()
        if not teams:
            BaseUI.show_message("No teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("TEAM TASKS")
        for team in teams:
            tasks = team.tasks
            if tasks:
                print(f"\n{team.name}:")
                for task in tasks:
                    assignee = task.assignee.name if task.assignee else "Unassigned"
                    attachment_count = len(task.attachments)
                    attachment_text = f" [{attachment_count} files]" if attachment_count > 0 else ""
                    print(f"  - {task.title} ({assignee}) - {task.status}{attachment_text}")
        
        BaseUI.press_enter()
    
    def update_task_status(self, user):
        tasks = user.tasks
        if not tasks:
            BaseUI.show_message("No tasks to update.", "info")
            BaseUI.press_enter()
            return
        
        print("\nSelect task:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.title} - {task.status}")
        
        try:
            task_num = int(input("\nTask number: "))
            if 1 <= task_num <= len(tasks):
                task = tasks[task_num - 1]
                
                print("\nSelect new status:")
                print("1. To Do")
                print("2. In Progress")
                print("3. Done")
                
                status_choice = BaseUI.get_choice(3)
                status_map = {1: TaskStatus.TODO, 2: TaskStatus.IN_PROGRESS, 3: TaskStatus.DONE}
                
                old_status = task.status
                task.status = status_map[status_choice]
                BaseUI.show_message(f"Task '{task.title}' updated: {old_status} -> {task.status}", "success")
                
                # Add comment about status change
                comment = f"Status changed from {old_status} to {task.status}"
                task.comments.append(Comment(user, comment))
        except:
            BaseUI.show_message("Invalid input.", "error")
        
        BaseUI.press_enter()
    
    def add_task_comment(self, user):
        tasks = user.tasks
        if not tasks:
            BaseUI.show_message("No tasks to comment on.", "info")
            BaseUI.press_enter()
            return
        
        print("\nSelect task:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.title}")
        
        try:
            task_num = int(input("\nTask number: "))
            if 1 <= task_num <= len(tasks):
                task = tasks[task_num - 1]
                comment_text = BaseUI.get_input("Your comment")
                
                if comment_text:
                    comment = Comment(user, comment_text)
                    task.comments.append(comment)
                    BaseUI.show_message("Comment added successfully.", "success")
                else:
                    BaseUI.show_message("Comment cannot be empty.", "error")
        except ValueError:
            BaseUI.show_message("Invalid input.", "error")
        
        BaseUI.press_enter()
    
    def add_file_attachment(self, user):
        tasks = user.tasks
        if not tasks:
            BaseUI.show_message("No tasks to add attachments to.", "info")
            BaseUI.press_enter()
            return
        
        print("\nSelect task to add attachment:")
        for i, task in enumerate(tasks, 1):
            attachment_count = len(task.attachments)
            attachment_info = f" ({attachment_count} files)" if attachment_count > 0 else ""
            print(f"{i}. {task.title}{attachment_info}")
        
        try:
            task_num = int(input("\nTask number: "))
            if 1 <= task_num <= len(tasks):
                task = tasks[task_num - 1]
                filename = BaseUI.get_input("Filename")
                
                if filename:
                    attachment = task.add_attachment(filename)
                    BaseUI.show_message(f"File '{filename}' added to task '{task.title}'", "success")
                    
                    # Add comment about the attachment
                    comment = f"Added file: {filename}"
                    task.comments.append(Comment(user, comment))
                else:
                    BaseUI.show_message("Filename cannot be empty.", "error")
        except ValueError:
            BaseUI.show_message("Invalid input.", "error")
        
        BaseUI.press_enter()

    def create_task(self, leader):
        if not leader.managed_teams:
            BaseUI.show_message("No teams to create tasks for.", "info")
            BaseUI.press_enter()
            return
        
        team = leader.managed_teams[0]
        members = [m for m in team.members if m != leader]
        
        if not members:
            BaseUI.show_message("No team members to assign tasks to.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("CREATE TASK")
        title = BaseUI.get_input("Task Title")
        description = BaseUI.get_input("Description")
        
        # Set priority 
        print("\nSelect priority:")
        print("1. Low")
        print("2. Medium")
        print("3. High")
        priority_choice = BaseUI.get_choice(3)
        priority_map = {1: Priority.LOW, 2: Priority.MEDIUM, 3: Priority.HIGH}
        priority = priority_map[priority_choice]
        
        # Set deadline 
        print("\nSet deadline:")
        days = int(BaseUI.get_input("Days from today", required=False) or "7")
        deadline = datetime.datetime.now() + datetime.timedelta(days=days)
        
        print("\nSelect assignee:")
        for i, member in enumerate(members, 1):
            print(f"{i}. {member.name}")
        
        assignee_choice = BaseUI.get_choice(len(members))
        assignee = members[assignee_choice - 1]
        
        task = self.system.create_task(title, description, assignee, team)
        if task:
            # Set additional properties
            task.priority = priority
            task.deadline = deadline
            
            BaseUI.show_message(f"Task '{title}' created for {assignee.name}", "success")
            
            # Send notification 
            notification = Notification(f"New task: {title} (Deadline: {deadline.strftime('%Y-%m-%d')})", assignee)
            assignee.notifications.append(notification)
            
            # Ask about file attachment 
            add_attachment = input("\nAdd file attachment now? (y/n): ").lower()
            if add_attachment == 'y':
                filename = BaseUI.get_input("Filename")
                if filename:
                    task.add_attachment(filename)
                    BaseUI.show_message(f"Attachment '{filename}' added", "success")
        
        BaseUI.press_enter()

    # ==================== TEAM MANAGEMENT DASHBOARD ====================
    
    def team_management(self, user, is_leader):
        while True:
            BaseUI.show_header("TEAM MANAGEMENT")
            
            print("1. View My Teams")
            print("2. View Team Progress")
            
            if is_leader:
                print("3. Create Team")
                print("4. Invite Member")
                print("5. Remove Member")
                print("6. Back")
                max_choice = 6
            else:
                print("3. Join Team")
                print("4. Leave Team")
                print("5. Back")
                max_choice = 5
            
            choice = BaseUI.get_choice(max_choice)
            
            if choice == 1:
                self.show_my_teams(user)
            elif choice == 2:
                self.show_team_progress(user)
            elif choice == 3 and is_leader:
                self.create_team(user)
            elif choice == 3 and not is_leader:
                self.join_team(user)
            elif choice == 4 and is_leader:
                self.invite_member(user)
            elif choice == 4 and not is_leader:
                self.leave_team(user)
            elif choice == 5 and is_leader:
                self.remove_member(user)
            elif (choice == 5 and not is_leader) or (choice == 6 and is_leader):
                break
    
    # ==================== TEAM MANAGEMENT METHODS ====================

    def show_my_teams(self, user):
        teams = user.get_teams()
        if not teams:
            BaseUI.show_message("No teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("MY TEAMS")
        for i, team in enumerate(teams, 1):
            is_leader = hasattr(user, 'managed_teams') and team in getattr(user, 'managed_teams', [])
            leader_tag = " (Leader)" if is_leader else ""
            progress = team.calculate_progress()
            print(f"{i}. {team.name}{leader_tag}")
            print(f"   Project: {team.project_title}")
            print(f"   Progress: {progress['progress']:.1f}% | Members: {len(team.members)}")
        
        BaseUI.press_enter()
    
    def show_team_progress(self, user):
        teams = user.get_teams()
        if not teams:
            BaseUI.show_message("No teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("TEAM PROGRESS")
        for team in teams:
            progress = team.calculate_progress()
            print(f"\n{team.name}:")
            print(f"  Total Tasks: {progress['total']}")
            print(f"  Completed: {progress['completed']}")
            print(f"  Progress: {progress['progress']:.1f}%")
        
        BaseUI.press_enter()
    
    def create_team(self, leader):
        BaseUI.show_header("CREATE TEAM")
        name = BaseUI.get_input("Team Name")
        project = BaseUI.get_input("Project Title")
        
        team = self.system.create_team(name, project, leader)
        if team:
            BaseUI.show_message(f"Team '{name}' created!", "success")
        
        BaseUI.press_enter()
    
    def join_team(self, user):
        available = self.system.get_available_teams(user)
        if not available:
            BaseUI.show_message("No teams available to join.", "info")
            BaseUI.press_enter()
            return
        
        print("\nAvailable Teams:")
        for i, team in enumerate(available, 1):
            print(f"{i}. {team.name} - {team.project_title}")
        
        team_choice = BaseUI.get_choice(len(available))
        team = available[team_choice - 1]
        
        if team.add_member(user):
            BaseUI.show_message(f"Joined {team.name}!", "success")
        else:
            BaseUI.show_message("Failed to join team.", "error")
        
        BaseUI.press_enter()
    
    def invite_member(self, leader):
        if not leader.managed_teams:
            BaseUI.show_message("No teams to invite to.", "info")
            BaseUI.press_enter()
            return
        
        team = leader.managed_teams[0]
        BaseUI.show_header(f"INVITE TO {team.name}")
        
        print("\n[Invite Member Function]")
        print(f"Team: {team.name}")
        print("Available students would be listed here...")
        print("[In real system, would send invitation]")
        
        BaseUI.press_enter()
    
    def leave_team(self, user):
        teams = user.get_teams()
        if not teams:
            BaseUI.show_message("No teams to leave.", "info")
            BaseUI.press_enter()
            return
        
        print("\nSelect team to leave:")
        for i, team in enumerate(teams, 1):
            print(f"{i}. {team.name}")
        
        team_choice = BaseUI.get_choice(len(teams))
        team = teams[team_choice - 1]
        
        if team.remove_member(user):
            BaseUI.show_message(f"Left {team.name}", "success")
        else:
            BaseUI.show_message("Failed to leave team.", "error")
        
        BaseUI.press_enter()
    
    def remove_member(self, leader):
        if not leader.managed_teams:
            BaseUI.show_message("No teams.", "info")
            BaseUI.press_enter()
            return
        
        team = leader.managed_teams[0]
        members = [m for m in team.members if m != leader]
        
        if not members:
            BaseUI.show_message("No members to remove.", "info")
            BaseUI.press_enter()
            return
        
        print("\nSelect member to remove:")
        for i, member in enumerate(members, 1):
            print(f"{i}. {member.name}")
        
        member_choice = BaseUI.get_choice(len(members))
        member = members[member_choice - 1]
        
        if team.remove_member(member):
            BaseUI.show_message(f"Removed {member.name}", "success")
        else:
            BaseUI.show_message("Failed to remove member.", "error")
        
        BaseUI.press_enter()
      
    # ==================== LECTURER FUNCTIONS ====================
    
    def view_team_discussions(self, lecturer):
        teams = lecturer.supervised_teams
        if not teams:
            BaseUI.show_message("No supervised teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("TEAM DISCUSSIONS")
        
        for team in teams:
            messages = team.chat_messages
            print(f"\n{team.name} (Project: {team.project_title}):")
            print("-"*40)
            
            if messages:
                for msg in messages[-10:]:
                    time = msg.timestamp.strftime("%Y-%m-%d %H:%M")
                    sender_role = "Lecturer" if isinstance(msg.sender, Lecturer) else "Student"
                    print(f"[{time}] {msg.sender.name} ({sender_role}): {msg.content}")
            else:
                print("No discussions yet.")
        
        BaseUI.press_enter()
    
    def feedback_management(self, lecturer):
        teams = lecturer.supervised_teams
        if not teams:
            BaseUI.show_message("No supervised teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("PROVIDE FEEDBACK TO STUDENTS")
        
        # Get all students
        all_students = []
        for team in teams:
            for member in team.members:
                if isinstance(member, Student) and member not in all_students:
                    all_students.append(member)
        
        if not all_students:
            BaseUI.show_message("No students available.", "info")
            BaseUI.press_enter()
            return
        
        print("\nSelect student:")
        for i, student in enumerate(all_students, 1):
            # Displays the student's team
            student_teams = [t.name for t in student.get_teams() if t in teams]
            teams_info = f" - Teams: {', '.join(student_teams)}" if student_teams else ""
            print(f"{i}. {student.name}{teams_info}")
        
        student_choice = BaseUI.get_choice(len(all_students))
        student = all_students[student_choice - 1]
        
        feedback = BaseUI.get_input("Your feedback to student")
        if feedback:
            self.system.provide_feedback(lecturer, student, feedback)
            BaseUI.show_message(f"Feedback sent to {student.name}", "success")
            
            # Send notification
            notification = Notification(
                f"You received feedback from Dr. {lecturer.name}",
                student
            )
            student.notifications.append(notification)
        
        BaseUI.press_enter()
    
    def monitor_progress(self, lecturer):
        teams = lecturer.supervised_teams
        if not teams:
            BaseUI.show_message("No supervised teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("TEAM PROGRESS MONITORING")
        
        for team in teams:
            progress = team.calculate_progress()
            print(f"\n{team.name}:")
            print(f"  Project: {team.project_title}")
            print(f"  Progress: {progress['progress']:.1f}%")
            print(f"  Tasks: {progress['completed']}/{progress['total']}")
            
            # Show task status breakdown
            tasks = team.tasks
            if tasks:
                todo = len([t for t in tasks if t.status == TaskStatus.TODO])
                in_progress = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
                done = len([t for t in tasks if t.status == TaskStatus.DONE])
                print(f"  Status: To Do={todo}, In Progress={in_progress}, Done={done}")
            
            print(f"  Members: {len(team.members)}")
        
        BaseUI.press_enter()
    
    # ==================== TEAM DISCUSSIONS ====================
    
    def team_discussions(self, user):
        teams = user.get_teams()
        if not teams:
            BaseUI.show_message("No teams to discuss with.", "info")
            BaseUI.press_enter()
            return
        
        while True:
            BaseUI.show_header("TEAM DISCUSSIONS")
            print("1. View Discussions")
            print("2. Send Message")
            print("3. Back")
            
            choice = BaseUI.get_choice(3)
            
            if choice == 1:
                self.view_discussions(teams)
            elif choice == 2:
                self.send_message(user, teams)
            elif choice == 3:
                break
    
    def view_discussions(self, teams):
        BaseUI.show_header("TEAM DISCUSSIONS")
        for team in teams:
            messages = team.chat_messages
            print(f"\n{team.name} (Project: {team.project_title}):")
            print("-"*40)
            
            if messages:
                for msg in messages[-10:]:  # Show the last 10 messages
                    time = msg.timestamp.strftime("%Y-%m-%d %H:%M")
                    print(f"[{time}] {msg.sender.name}: {msg.content}")
            else:
                print("No discussions yet.")
        
        BaseUI.press_enter()
    
    def send_message(self, user, teams):
        print("\nSelect team:")
        for i, team in enumerate(teams, 1):
            print(f"{i}. {team.name}")
        
        team_choice = BaseUI.get_choice(len(teams))
        team = teams[team_choice - 1]
        
        message = BaseUI.get_input("Your message")
        if message:
            self.system.send_chat_message(user, team, message)
            BaseUI.show_message("Message sent to team discussions!", "success")
        
        BaseUI.press_enter()
    
     # ==================== MEETING MANAGEMENT ====================

    def view_meetings(self, user):
        teams = user.get_teams()
        if not teams:
            BaseUI.show_message("No teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header("TEAM MEETINGS")
        
        has_meetings = False
        for team in teams:
            meetings = team.meetings
            if meetings:
                has_meetings = True
                print(f"\n{team.name}:")
                for i, meeting in enumerate(meetings, 1):
                    time_str = meeting.datetime.strftime('%Y-%m-%d %H:%M')
                    print(f"  {i}. {meeting.title}")
                    print(f"     Time: {time_str}")
        
        if not has_meetings:
            BaseUI.show_message("No meetings scheduled.", "info")
        
        BaseUI.press_enter()
    
    def manage_meetings(self, leader):
        if not leader.managed_teams:
            BaseUI.show_message("No teams.", "info")
            BaseUI.press_enter()
            return
        
        team = leader.managed_teams[0]
        
        while True:
            BaseUI.show_header(f"MEETINGS - {team.name}")
            print("1. View Meetings")
            print("2. Schedule Meeting")
            print("3. Back")
            
            choice = BaseUI.get_choice(3)
            
            if choice == 1:
                self.view_team_meetings(team)
            elif choice == 2:
                self.schedule_meeting(leader, team)
            elif choice == 3:
                break
    
    def view_team_meetings(self, team):
        BaseUI.show_header(f"MEETINGS - {team.name}")
        
        meetings = team.meetings
        if not meetings:
            BaseUI.show_message("No meetings scheduled.", "info")
        else:
            for i, meeting in enumerate(meetings, 1):
                time_str = meeting.datetime.strftime('%Y-%m-%d %H:%M')
                print(f"{i}. {meeting.title}")
                print(f"   Time: {time_str}")
                print(f"   Location: {meeting.location}")
        
        BaseUI.press_enter()
    
    def schedule_meeting(self, leader, team):
        BaseUI.show_header("SCHEDULE MEETING")
        
        title = BaseUI.get_input("Meeting Title")
        
        # Enter the meeting date and time
        print("\nEnter meeting date and time:")
        
        # Enter date
        while True:
            date_str = BaseUI.get_input("Date (YYYY-MM-DD)")
            try:
                year, month, day = map(int, date_str.split('-'))
                meeting_date = datetime.date(year, month, day)
                
                # Check date 
                today = datetime.date.today()
                if meeting_date < today:
                    print("Date must be in the future. Try again.")
                    continue
                break
            except (ValueError, TypeError):
                print("Invalid date format. Use YYYY-MM-DD (e.g., 2025-12-25)")
        
        # Enter time
        while True:
            time_str = BaseUI.get_input("Time (HH:MM, 24-hour format)")
            try:
                hour, minute = map(int, time_str.split(':'))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    print("Invalid time. Hour must be 0-23, minute 0-59.")
                    continue
                break
            except (ValueError, TypeError):
                print("Invalid time format. Use HH:MM (e.g., 14:30)")
        
        meeting_time = datetime.datetime.combine(meeting_date, datetime.time(hour, minute))
        
        # Schedule meeting
        meeting = self.system.create_meeting(title, team, meeting_time)
        if meeting:
            BaseUI.show_message(f"Meeting '{title}' scheduled!", "success")
            print(f"\nMeeting Details:")
            print(f"  Title: {title}")
            print(f"  Time: {meeting_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Team: {team.name}")
            
            # Send notifications to team members
            for member in team.members:
                notification = Notification(
                    f"New meeting scheduled: {title} at {meeting_time.strftime('%Y-%m-%d %H:%M')}",
                    member
                )
                member.notifications.append(notification)
        
        BaseUI.press_enter()

# ==================== PROVIDE FEEDBACK ====================
    
    def provide_team_feedback(self, user):
        teams = user.get_teams()
        if not teams:
            BaseUI.show_message("No teams to provide feedback in.", "info")
            BaseUI.press_enter()
            return
        
        # Select team
        print("\nSelect team:")
        for i, team in enumerate(teams, 1):
            print(f"{i}. {team.name}")
        
        team_choice = BaseUI.get_choice(len(teams))
        selected_team = teams[team_choice - 1]
        
   
        team_members = [member for member in selected_team.members if member != user]
        
        if not team_members:
            BaseUI.show_message("No other team members to provide feedback to.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header(f"PROVIDE FEEDBACK - {selected_team.name}")
        
        print("\nSelect team member to provide feedback:")
        for i, member in enumerate(team_members, 1):
            role = "Team Leader" if isinstance(member, TeamLeader) else "Student"
            leader_tag = " (Leader)" if member == selected_team.leader else ""
            print(f"{i}. {member.name} ({role}){leader_tag}")
        
        try:
            member_choice = int(input("\nSelect member: "))
            if 1 <= member_choice <= len(team_members):
                target_member = team_members[member_choice - 1]
                feedback_text = BaseUI.get_input("Your feedback")
                
                if feedback_text:
                  
                    feedback = Feedback(user, target_member, feedback_text)
                    
                    if hasattr(self.system, 'feedback_list'):
                        self.system.feedback_list.append(feedback)
                    
                    BaseUI.show_message(f"Feedback sent to {target_member.name}", "success")
                    
                    # Send notification
                    notification = Notification(
                        f"You received feedback from {user.name}",
                        target_member
                    )
                    target_member.notifications.append(notification)
                else:
                    BaseUI.show_message("Feedback cannot be empty.", "error")
        except ValueError:
            BaseUI.show_message("Invalid selection.", "error")
        
        BaseUI.press_enter()

    # ==================== REPORT GENERATION ====================
    
    def generate_student_report(self, student):
        BaseUI.show_header(f"STUDENT REPORT - {student.name}")
        
        print(f"Student: {student.name}")
        print(f"Student ID: {student.student_id}")
        print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("-"*40)
        
        # Team information
        teams = student.get_teams()
        if teams:
            print("\nTEAM PARTICIPATION:")
            for team in teams:
                is_leader = hasattr(student, 'managed_teams') and team in getattr(student, 'managed_teams', [])
                leader_tag = " (Leader)" if is_leader else ""
                
                # Calculate team-specific tasks
                team_tasks = [t for t in student.tasks if t.team == team]
                completed = len([t for t in team_tasks if t.status == TaskStatus.DONE])
                total = len(team_tasks)
                
                print(f"\n- {team.name}{leader_tag}")
                print(f"  Project: {team.project_title}")
                print(f"  Tasks: {completed}/{total} completed")
                if total > 0:
                    print(f"  Completion: {(completed/total*100):.1f}%")
        else:
            print("\nNo teams joined yet.")
        
        # Task summary
        tasks = student.tasks
        if tasks:
            completed = len([t for t in tasks if t.status == TaskStatus.DONE])
            in_progress = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
            todo = len([t for t in tasks if t.status == TaskStatus.TODO])
            
            print(f"\nTASK SUMMARY:")
            print(f"Total Tasks: {len(tasks)}")
            print(f"Completed: {completed}")
            print(f"In Progress: {in_progress}")
            print(f"To Do: {todo}")
            
            if len(tasks) > 0:
                print(f"Overall Completion: {(completed/len(tasks)*100):.1f}%")
        
        print(f"\n[Report generated successfully]")
        BaseUI.press_enter()
    
    def generate_leader_report(self, leader):
        if not leader.managed_teams:
            BaseUI.show_message("No teams.", "info")
            BaseUI.press_enter()
            return
        
        team = leader.managed_teams[0]
        BaseUI.show_header(f"TEAM REPORT - {team.name}")
        
        progress = team.calculate_progress()
        print(f"Team: {team.name}")
        print(f"Project: {team.project_title}")
        print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("-"*40)
        
        print(f"\nOVERVIEW:")
        print(f"Progress: {progress['progress']:.1f}%")
        print(f"Total Tasks: {progress['total']}")
        print(f"Completed: {progress['completed']}")
        print(f"Members: {len(team.members)}")
        
        print(f"\nMEMBER CONTRIBUTIONS:")
        for member in team.members:
            member_tasks = [t for t in member.tasks if t.team == team]
            completed = len([t for t in member_tasks if t.status == TaskStatus.DONE])
            total = len(member_tasks)
            
            leader_tag = " (Leader)" if member == leader else ""
            print(f"\n- {member.name}{leader_tag}")
            print(f"  Tasks: {completed}/{total} completed")
            if total > 0:
                print(f"  Rate: {(completed/total*100):.1f}%")
        
        BaseUI.press_enter()
    
    def generate_lecturer_report(self, lecturer):
        teams = lecturer.supervised_teams
        if not teams:
            BaseUI.show_message("No supervised teams.", "info")
            BaseUI.press_enter()
            return
        
        BaseUI.show_header(f"CLASS REPORT - Dr. {lecturer.name}")
        
        print(f"Lecturer: Dr. {lecturer.name}")
        print(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Supervised Teams: {len(teams)}")
        print("-"*40)
        
        total_students = 0
        total_tasks = 0
        completed_tasks = 0
        
        print("\nTEAM SUMMARIES:")
        for team in teams:
            progress = team.calculate_progress()
            total_students += len(team.members)
            total_tasks += progress['total']
            completed_tasks += progress['completed']
            
            print(f"\n{team.name}:")
            print(f"  Project: {team.project_title}")
            print(f"  Progress: {progress['progress']:.1f}%")
            print(f"  Members: {len(team.members)}")
            print(f"  Tasks: {progress['completed']}/{progress['total']}")
        
        print(f"\nCLASS SUMMARY:")
        print(f"Total Students: {total_students}")
        print(f"Total Tasks: {total_tasks}")
        print(f"Completed Tasks: {completed_tasks}")
        if total_tasks > 0:
            print(f"Overall Progress: {(completed_tasks/total_tasks*100):.1f}%")
        
        BaseUI.press_enter()
    
    # ==================== NOTIFICATIONS ====================
    
    def show_notifications(self, user):
        notifications = user.notifications
        BaseUI.show_header("NOTIFICATIONS")
        
        if not notifications:
            BaseUI.show_message("No notifications.", "info")
        else:
            unread_count = sum(1 for n in notifications if not n.is_read)
            print(f"You have {len(notifications)} notification(s) ({unread_count} unread)")
            print("-"*40)
            
            for i, notification in enumerate(notifications, 1):
                time = notification.timestamp.strftime("%H:%M")
                status = "[READ]" if notification.is_read else "[NEW]"
                print(f"{i}. {status} [{time}] {notification.message}")
        
        BaseUI.press_enter()
    
    # ==================== EXIT ====================
    
    def exit_program(self):
        BaseUI.show_header("THANK YOU")
        print("\nThank you for using the Smart Student Team Collaboration Platform!")
        print("\nGoodbye!")
        print("\n" + "="*60)
        sys.exit(0)