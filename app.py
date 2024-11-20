from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
from dotenv import load_dotenv
import os

from models import db, User, Group, Todo

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())  # Use environment variable if available
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Google OAuth2 credentials
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
if not GOOGLE_CLIENT_ID:
    raise ValueError("No Google Client ID set. Please configure GOOGLE_CLIENT_ID in .env file")

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_group_hierarchy():
    """Get all groups with their subgroups"""
    with app.app_context():
        if not current_user.is_authenticated:
            return {}
            
        # Get all groups for the current user
        main_groups = Group.query.filter_by(parent_group=None, user_id=current_user.id).all()
        all_groups = Group.query.filter_by(user_id=current_user.id).all()
        
        # Create a mapping of parent to children
        group_children = {}
        for group in all_groups:
            if group.parent_group not in group_children:
                group_children[group.parent_group] = []
            group_children[group.parent_group].append(group)
        
        def build_subgroup_tree(parent_name):
            """Recursively build the subgroup tree"""
            if parent_name not in group_children:
                return []
            
            subgroups = []
            for group in sorted(group_children[parent_name], key=lambda x: x.name):
                subgroup = {
                    'name': group.name,
                    'subgroups': build_subgroup_tree(group.name)
                }
                subgroups.append(subgroup)
            return subgroups
        
        # Build hierarchy
        hierarchy = {}
        
        # Add main groups with their complete subgroup trees
        for group in sorted(main_groups, key=lambda x: x.name):
            # Only count tasks belonging to the current user
            task_count = Todo.query.filter_by(
                group=group.name,
                user_id=current_user.id
            ).count()
            
            hierarchy[group.name] = {
                'subgroups': build_subgroup_tree(group.name),
                'task_count': task_count
            }
        
        return hierarchy

@app.route('/')
def index():
    selected_group = request.args.get('group')
    
    # Get todos for the current user or todos without a user during migration
    if current_user.is_authenticated:
        todos = Todo.query.filter(
            (Todo.user_id == current_user.id) | (Todo.user_id.is_(None))
        ).order_by(Todo.due_date.asc(), Todo.end_time.asc()).all()
    else:
        todos = Todo.query.filter(Todo.user_id.is_(None)).order_by(Todo.due_date.asc(), Todo.end_time.asc()).all()
    
    if selected_group:
        todos = [todo for todo in todos if todo.group == selected_group]
    
    groups = get_group_hierarchy()
    return render_template('index.html', todos=todos, groups=groups, selected_group=selected_group)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    group = request.form.get('group')
    due_date_str = request.form.get('due_date')
    end_time_str = request.form.get('end_time')
    
    if title:
        # Create new group if it doesn't exist
        if group and not Group.query.filter_by(name=group, user_id=current_user.id).first():
            new_group = Group(name=group, user_id=current_user.id)
            db.session.add(new_group)
            db.session.commit()
        
        # Parse date and time
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        end_time = datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else None
        
        todo = Todo(
            title=title,
            group=group,
            due_date=due_date,
            end_time=end_time,
            user_id=current_user.id
        )
        db.session.add(todo)
        db.session.commit()
        
    return redirect(url_for('index', group=group))

@app.route('/add_group', methods=['POST'])
@login_required
def add_group():
    name = request.form.get('name')
    parent_group = request.form.get('parent_group')
    
    if name and name.strip():
        name = name.strip()
        # Check if group already exists for the current user
        existing_group = Group.query.filter_by(
            name=name,
            user_id=current_user.id
        ).first()
        if not existing_group:
            # If parent_group is empty string or "None", set it to None
            parent = None if not parent_group or parent_group == "None" else parent_group
            new_group = Group(
                name=name,
                parent_group=parent,
                user_id=current_user.id
            )
            db.session.add(new_group)
            db.session.commit()
    return redirect(url_for('index', group=parent_group if parent_group and parent_group != "None" else None))

@app.route('/complete/<int:id>')
@login_required
def complete(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id == current_user.id:
        todo.completed = not todo.completed
        db.session.commit()
    
    # Only redirect with group parameter if the todo has a group
    if todo.group:
        return redirect(url_for('index', group=todo.group))
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id == current_user.id:
        group = todo.group  # Store group before deleting
        db.session.delete(todo)
        db.session.commit()
    
    # Only redirect with group parameter if the todo had a group
    if group:
        return redirect(url_for('index', group=group))
    return redirect(url_for('index'))

@app.route('/delete_group/<group>', methods=['GET', 'POST'])
@login_required
def delete_group(group):
    with app.app_context():
        def delete_group_recursive(group_name):
            # Get all subgroups
            subgroups = Group.query.filter_by(parent_group=group_name, user_id=current_user.id).all()
            
            # Recursively delete all subgroups
            for subgroup in subgroups:
                delete_group_recursive(subgroup.name)
            
            # Delete all tasks in this group
            Todo.query.filter_by(group=group_name, user_id=current_user.id).delete(synchronize_session=False)
            
            # Delete the group itself
            group_to_delete = Group.query.filter_by(name=group_name, user_id=current_user.id).first()
            if group_to_delete:
                db.session.delete(group_to_delete)
        
        try:
            # Start recursive deletion
            delete_group_recursive(group)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting group: {e}")
        
        return redirect(url_for('index'))

@app.route('/delete_all_tasks', methods=['POST'])
@login_required
def delete_all_tasks():
    """Delete all tasks and groups from the database"""
    with app.app_context():
        # Delete all tasks and groups
        Todo.query.filter_by(user_id=current_user.id).delete()
        Group.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
    return '', 204  # No content response

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
        
        end_time = request.form.get('end_time')
        if end_time:
            try:
                todo.end_time = datetime.strptime(end_time, '%H:%M').time()
            except ValueError:
                todo.end_time = None
        else:
            todo.end_time = None
        
        group_name = request.form.get('group')
        if group_name:
            group = Group.query.filter_by(name=group_name, user_id=current_user.id).first()
            todo.group = group_name if group else None
        else:
            todo.group = None
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_todo.html', todo=todo, groups=get_group_hierarchy())

@app.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('signup.html', google_client_id=GOOGLE_CLIENT_ID)

@app.route('/login')
def login():
    print("Using Google Client ID:", GOOGLE_CLIENT_ID)  # Debug print
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', google_client_id=GOOGLE_CLIENT_ID)

@app.route('/callback', methods=['POST'])
def callback():
    try:
        # Get the token from the request
        token = request.json['credential']
        
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID)

        # Get user info
        email = idinfo['email']
        name = idinfo['name']

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create new user
            user = User(email=email, name=name)
            db.session.add(user)
            db.session.commit()

        # Log in the user
        login_user(user)
        return jsonify({'success': True})

    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid token'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.context_processor
def utility_processor():
    def is_user_authenticated():
        return current_user.is_authenticated
    return dict(is_user_authenticated=is_user_authenticated)

if __name__ == '__main__':
    # Ensure instance folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    
    # Initialize database if it doesn't exist
    with app.app_context():
        if not os.path.exists(os.path.join(app.instance_path, 'todos.db')):
            db.create_all()
            print("Created new database with schema")
        else:
            print("Using existing database")
    
    app.run(debug=True)
