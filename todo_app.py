"""
MOBILE TODO APP - Local Storage with JSON
Simple, clean, mobile-friendly terminal UI
"""
import json
import os
from datetime import datetime
from typing import List, Dict

class TodoApp:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos: List[Dict] = []
        self.load_todos()
    
    def load_todos(self):
        """Load todos from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
                print(f"✓ Loaded {len(self.todos)} todos")
            except Exception as e:
                print(f"Error loading: {e}")
                self.todos = []
        else:
            print("New todo list created")
            self.todos = []
    
    def save_todos(self):
        """Save todos to JSON file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False
    
    def add_todo(self, title: str, priority: str = "normal"):
        """Add new todo"""
        if not title.strip():
            print("❌ Title cannot be empty!")
            return
        
        todo = {
            "id": len(self.todos) + 1,
            "title": title.strip(),
            "priority": priority,  # low, normal, high, urgent
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_at": None
        }
        
        self.todos.append(todo)
        self.save_todos()
        print(f"✓ Added: {title}")
    
    def list_todos(self, filter_by: str = "all"):
        """Display todos"""
        if not self.todos:
            print("📭 No todos yet!")
            return
        
        # Filter
        if filter_by == "completed":
            items = [t for t in self.todos if t["completed"]]
        elif filter_by == "pending":
            items = [t for t in self.todos if not t["completed"]]
        else:
            items = self.todos
        
        if not items:
            print(f"No {filter_by} todos")
            return
        
        print("\n" + "="*60)
        print(f"📋 TODO LIST ({len(items)} items)")
        print("="*60)
        
        for todo in items:
            status = "✓" if todo["completed"] else "○"
            priority_emoji = {
                "urgent": "🔴",
                "high": "🟠",
                "normal": "🟡",
                "low": "🟢"
            }
            emoji = priority_emoji.get(todo["priority"], "🟡")
            
            check = "✅ " if todo["completed"] else "   "
            print(f"{check}{status} [{todo['id']}] {emoji} {todo['title']}")
            print(f"     Created: {todo['created']}")
            if todo["completed_at"]:
                print(f"     Completed: {todo['completed_at']}")
        
        print("="*60)
    
    def mark_complete(self, todo_id: int):
        """Mark todo as complete"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                if todo["completed"]:
                    print("Already completed!")
                    return
                todo["completed"] = True
                todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save_todos()
                print(f"✓ Marked complete: {todo['title']}")
                return
        
        print("❌ Todo not found!")
    
    def mark_incomplete(self, todo_id: int):
        """Mark todo as incomplete"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = False
                todo["completed_at"] = None
                self.save_todos()
                print(f"✓ Marked incomplete: {todo['title']}")
                return
        
        print("❌ Todo not found!")
    
    def delete_todo(self, todo_id: int):
        """Delete todo"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                title = todo["title"]
                self.todos.pop(i)
                self.save_todos()
                print(f"✓ Deleted: {title}")
                return
        
        print("❌ Todo not found!")
    
    def edit_todo(self, todo_id: int, new_title: str):
        """Edit todo title"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                old_title = todo["title"]
                todo["title"] = new_title.strip()
                self.save_todos()
                print(f"✓ Updated: '{old_title}' → '{new_title}'")
                return
        
        print("❌ Todo not found!")
    
    def set_priority(self, todo_id: int, priority: str):
        """Change priority"""
        if priority not in ["low", "normal", "high", "urgent"]:
            print("Invalid priority! Use: low, normal, high, urgent")
            return
        
        for todo in self.todos:
            if todo["id"] == todo_id:
                old = todo["priority"]
                todo["priority"] = priority
                self.save_todos()
                print(f"✓ Priority changed: {old} → {priority}")
                return
        
        print("❌ Todo not found!")
    
    def get_stats(self):
        """Show statistics"""
        total = len(self.todos)
        completed = len([t for t in self.todos if t["completed"]])
        pending = total - completed
        urgent = len([t for t in self.todos if t["priority"] == "urgent"])
        
        print("\n" + "="*40)
        print("📊 STATISTICS")
        print("="*40)
        print(f"Total: {total}")
        print(f"✓ Completed: {completed}")
        print(f"○ Pending: {pending}")
        print(f"🔴 Urgent: {urgent}")
        if total > 0:
            progress = int((completed / total) * 100)
            bar = "█" * (progress // 5) + "░" * (20 - progress // 5)
            print(f"Progress: {bar} {progress}%")
        print("="*40)
    
    def clear_completed(self):
        """Delete all completed todos"""
        before = len(self.todos)
        self.todos = [t for t in self.todos if not t["completed"]]
        after = len(self.todos)
        self.save_todos()
        print(f"✓ Deleted {before - after} completed todos")
    
    def export_to_txt(self, filename="todos_export.txt"):
        """Export todos to text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("TODO LIST EXPORT\n")
            f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("="*50 + "\n\n")
            
            for todo in self.todos:
                status = "✓" if todo["completed"] else "○"
                f.write(f"{status} [{todo['priority'].upper()}] {todo['title']}\n")
                f.write(f"  Created: {todo['created']}\n")
                if todo["completed_at"]:
                    f.write(f"  Completed: {todo['completed_at']}\n")
                f.write("\n")
        
        print(f"✓ Exported to {filename}")
    
    def show_menu(self):
        """Display menu"""
        print("""
╔════════════════════════════════════╗
║         📱 TODO APP MENU           ║
╚════════════════════════════════════╝

1. ➕ Add todo
2. 📋 View all
3. ✅ Mark complete
4. ❌ Mark incomplete
5. ✏️  Edit todo
6. 🗑️  Delete todo
7. 🎯 Set priority
8. 📊 Show stats
9. 🧹 Clear completed
10. 💾 Export to text
11. 🔍 Filter (completed/pending)
12. ❓ Help
13. 🚪 Exit

╔════════════════════════════════════╗
        """)
    
    def show_help(self):
        """Show help"""
        print("""
╔════════════════════════════════════╗
║          📚 HELP GUIDE             ║
╚════════════════════════════════════╝

PRIORITY LEVELS:
  🟢 low      - Low priority
  🟡 normal   - Normal (default)
  🟠 high     - High priority
  🔴 urgent   - Urgent!

QUICK COMMANDS:
  add <title>              Add new todo
  add <title> urgent       Add urgent todo
  list                     View all
  list completed           View completed
  list pending             View pending
  done <id>                Mark complete
  undo <id>                Mark incomplete
  edit <id> <new title>    Edit todo
  del <id>                 Delete todo
  priority <id> <level>    Change priority
  stats                    View statistics
  clear                    Clear completed
  export                   Export to file
  help                     Show this help
  exit                     Exit app

EXAMPLE:
  add Buy groceries
  add Call mom high
  done 1
  priority 2 urgent

╔════════════════════════════════════╗
        """)
    
    def run(self):
        """Main app loop"""
        print("\n" + "="*40)
        print("📱 WELCOME TO TODO APP")
        print("="*40)
        print("Type 'help' for commands or '12' in menu\n")
        
        while True:
            self.show_menu()
            choice = input("Choose (1-13): ").strip()
            
            if choice == "1":
                title = input("Todo title: ").strip()
                priority = input("Priority (low/normal/high/urgent) [normal]: ").strip() or "normal"
                self.add_todo(title, priority)
            
            elif choice == "2":
                self.list_todos()
            
            elif choice == "3":
                self.list_todos()
                try:
                    todo_id = int(input("Todo ID to complete: "))
                    self.mark_complete(todo_id)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice == "4":
                self.list_todos()
                try:
                    todo_id = int(input("Todo ID to undo: "))
                    self.mark_incomplete(todo_id)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice == "5":
                self.list_todos()
                try:
                    todo_id = int(input("Todo ID to edit: "))
                    new_title = input("New title: ").strip()
                    self.edit_todo(todo_id, new_title)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice == "6":
                self.list_todos()
                try:
                    todo_id = int(input("Todo ID to delete: "))
                    self.delete_todo(todo_id)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice == "7":
                self.list_todos()
                try:
                    todo_id = int(input("Todo ID: "))
                    priority = input("Priority (low/normal/high/urgent): ").strip()
                    self.set_priority(todo_id, priority)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice == "8":
                self.get_stats()
            
            elif choice == "9":
                confirm = input("Clear all completed? (y/n): ")
                if confirm.lower() == 'y':
                    self.clear_completed()
            
            elif choice == "10":
                filename = input("Filename [todos_export.txt]: ").strip() or "todos_export.txt"
                self.export_to_txt(filename)
            
            elif choice == "11":
                filter_type = input("Filter (completed/pending): ").strip().lower()
                self.list_todos(filter_type)
            
            elif choice == "12":
                self.show_help()
            
            elif choice == "13" or choice.lower() == "exit":
                print("\n✓ Goodbye! 👋")
                break
            
            # Quick commands
            elif choice.startswith("add "):
                parts = choice[4:].split()
                if len(parts) > 1 and parts[-1] in ["low", "normal", "high", "urgent"]:
                    priority = parts[-1]
                    title = " ".join(parts[:-1])
                else:
                    priority = "normal"
                    title = " ".join(parts)
                self.add_todo(title, priority)
            
            elif choice.startswith("done "):
                try:
                    todo_id = int(choice[5:])
                    self.mark_complete(todo_id)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice.startswith("undo "):
                try:
                    todo_id = int(choice[5:])
                    self.mark_incomplete(todo_id)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice.startswith("del "):
                try:
                    todo_id = int(choice[4:])
                    self.delete_todo(todo_id)
                except ValueError:
                    print("Invalid ID!")
            
            elif choice in ["list", "help", "stats", "clear", "export"]:
                if choice == "list":
                    self.list_todos()
                elif choice == "help":
                    self.show_help()
                elif choice == "stats":
                    self.get_stats()
                elif choice == "clear":
                    confirm = input("Clear completed? (y/n): ")
                    if confirm.lower() == 'y':
                        self.clear_completed()
                elif choice == "export":
                    self.export_to_txt()
            
            else:
                print("❌ Invalid choice! Type 'help' for commands.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = TodoApp()
    app.run()
