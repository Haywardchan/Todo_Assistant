from app import app, db, Todo
from datetime import datetime, date

def list_todos(group=None):
    with app.app_context():
        if group:
            todos = Todo.query.filter_by(group=group).order_by(Todo.due_date.asc(), Todo.start_time.asc()).all()
            print(f"\nTodo List - Group: {group}")
        else:
            todos = Todo.query.order_by(Todo.due_date.asc(), Todo.start_time.asc()).all()
            print("\nTodo List - All Tasks")
            
        print("-" * 80)
        for todo in todos:
            status = "✓" if todo.completed else " "
            remaining = todo.remaining_days()
            
            # Format remaining days message
            if remaining < 0:
                days_msg = f"[OVERDUE by {-remaining} day{'s' if -remaining != 1 else ''}]"
            elif remaining == 0:
                days_msg = "[DUE TODAY]"
            else:
                days_msg = f"[{remaining} day{'s' if remaining != 1 else ''} left]"
            
            # Format time information
            time_info = ""
            if todo.start_time:
                time_info = f"Time: {todo.start_time.strftime('%H:%M')}"
                if todo.end_time:
                    time_info += f" - {todo.end_time.strftime('%H:%M')}"
            
            print(f"[{status}] {todo.id}. {todo.title}")
            if todo.group:
                print(f"    Group: {todo.group}")
            print(f"    Due: {todo.due_date.strftime('%Y-%m-%d')} {days_msg}")
            if time_info:
                print(f"    {time_info}")
            print(f"    Created: {todo.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 80)

def list_groups():
    with app.app_context():
        groups = db.session.query(Todo.group).distinct().filter(Todo.group != None).all()
        groups = [g[0] for g in groups]
        
        print("\nAvailable Groups:")
        print("-" * 40)
        for group in groups:
            count = Todo.query.filter_by(group=group).count()
            print(f"- {group} ({count} tasks)")
        print("-" * 40)

def add_todo(title, due_date, group=None, start_time=None, end_time=None):
    with app.app_context():
        # Convert string dates/times to proper objects if needed
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        if isinstance(start_time, str) and start_time:
            start_time = datetime.strptime(start_time, '%H:%M').time()
        if isinstance(end_time, str) and end_time:
            end_time = datetime.strptime(end_time, '%H:%M').time()
            
        new_todo = Todo(
            title=title,
            due_date=due_date,
            start_time=start_time,
            end_time=end_time,
            group=group
        )
        db.session.add(new_todo)
        db.session.commit()
        print(f"\nAdded new todo:")
        print(f"Title: {title}")
        if group:
            print(f"Group: {group}")
        print(f"Due Date: {due_date}")
        if start_time:
            print(f"Time: {start_time.strftime('%H:%M')}", end="")
            if end_time:
                print(f" - {end_time.strftime('%H:%M')}")
            else:
                print()

def delete_todo(id):
    with app.app_context():
        todo = Todo.query.get(id)
        if todo:
            title = todo.title
            group = todo.group
            db.session.delete(todo)
            db.session.commit()
            print(f"\nDeleted todo: '{title}' (ID: {id})")
            if group:
                print(f"from group: {group}")
        else:
            print(f"\nNo todo found with ID: {id}")

def mark_completed(id, completed=True):
    with app.app_context():
        todo = Todo.query.get(id)
        if todo:
            todo.completed = completed
            db.session.commit()
            status = "completed" if completed else "uncompleted"
            print(f"\nMarked todo '{todo.title}' as {status}")
            if todo.group:
                print(f"in group: {todo.group}")
        else:
            print(f"\nNo todo found with ID: {id}")

# Example usage:
if __name__ == '__main__':
    print("\nTodo List Manager")
    print("================")
    
    # Add example todos
    add_todo(
        "Complete project presentation",
        due_date="2024-01-20",
        start_time="14:00",
        end_time="15:30",
        group="Work"
    )
    add_todo(
        "Submit report",
        due_date="2024-01-15",
        group="Work"
    )
    add_todo(
        "Study for exam",
        due_date="2024-01-18",
        start_time="09:00",
        end_time="12:00",
        group="School"
    )
    
    # List all groups
    list_groups()
    
    # List todos by group
    list_todos(group="Work")
    list_todos(group="School")
    
    # List all todos
    list_todos()
    
    # Mark a todo as completed
    mark_completed(1)
    
    # List updated todos
    print("\nAfter marking todo as completed:")
    list_todos()
