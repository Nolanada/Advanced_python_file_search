# main.py
import argparse
from utils.file_search import create_search_index, search_files
from utils.log_file import log_event, get_logs 
from utils.caching import cache_results, get_cached_results
from utils.file_metadata import get_file_metadata
from utils.system_monitoring import monitor_system
from utils.log_file import log_event, get_logs
from utils.user_management import add_user, get_users, update_user_role, delete_user
from utils.user_activities import record_activity, get_user_activity

def main():
    parser = argparse.ArgumentParser(description='Command Line Application for Various Utilities')
    parser.add_argument('--index', help='Create search index', action='store_true')
    parser.add_argument('--search', help='Search for files')
    parser.add_argument('--cache', help='Use caching for an expensive function', nargs=2, type=int)
    parser.add_argument('--metadata', help='Get file metadata')
    parser.add_argument('--log-event', help='Log an event', nargs=2, metavar=('log_level', 'message')) 
    parser.add_argument('--get-logs', help='Get logs by level')
    parser.add_argument('--monitor', help='Monitor system resources', action='store_true')
    parser.add_argument('--add-user', help='Add a new user', nargs=3, metavar=('username', 'email', 'role'))
    parser.add_argument('--get-users', help='Get list of users', action='store_true')
    parser.add_argument('--update-role', help='Update user role', nargs=2, metavar=('username', 'role'))
    parser.add_argument('--delete-user', help='Delete a user', metavar='username')
    parser.add_argument('--root-dir', help='Root directory to index', type=str)
    parser.add_argument('--index-dir', help='Directory to store index', type=str, default='indexdir')
    parser.add_argument('--record-activity', help='Record user activity', nargs=2, metavar=('user_id', 'activity'))
    parser.add_argument('--get-activity', help='Get user activity', type=int)
    args = parser.parse_args()
    if args.index: 
        create_search_index(args.index_dir, args.root_dir) 
        log_event('INFO', f"Index created for directory {args.root_dir} in {args.index_dir}") 
    if args.search: 
        results = search_files(args.index_dir, args.search) 
        log_event('INFO', f"Search performed for query '{args.search}'") 
    if args.cache: 
        result = expensive_function(args.cache[0], args.cache[1]) 
        log_event('INFO', f"Result of cached function: {result}") 
        print(f'Result of cached function: {result}') 
    if args.metadata: 
        get_file_metadata(args.metadata) 
        log_event('INFO', f"Fetched metadata for {args.metadata}") 
    if args.log_event: 
        log_level, message = args.log_event 
        log_event(log_level, message) 
        print(f"Logged event: {log_level} - {message}") 
    if args.get_logs: 
        log_level = args.get_logs.upper() 
        logs = get_logs(log_level) 
        for log in logs: 
            print(f"{log[1]} - {log[2]} - {log[3]}") 
    if args.monitor: 
        monitor_system() 
        log_event('INFO', "System monitoring started") 
    if args.add_user: 
        add_user(args.add_user[0], args.add_user[1], args.add_user[2]) 
        log_event('INFO', f"User {args.add_user[0]} added") 
        print(f'User {args.add_user[0]} added.') 
    if args.get_users: 
        users = get_users() 
        for user in users: 
            log_event('INFO', f"Fetched user: {user[1]}") 
            print(f'ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}') 
    if args.update_role: 
        update_user_role(args.update_role[0], args.update_role[1]) 
        log_event('INFO', f"User {args.update_role[0]}'s role updated to {args.update_role[1]}") 
        print(f'Role of {args.update_role[0]} updated to {args.update_role[1]}.') 
    if args.delete_user: 
        delete_user(args.delete_user) 
        log_event('INFO', f"User {args.delete_user} deleted") 
        print(f'User {args.delete_user} deleted.') 
    if args.record_activity: 
        record_activity(args.record_activity[0], args.record_activity[1]) 
        log_event('INFO', f"Recorded activity for user {args.record_activity[0]}: {args.record_activity[1]}") 
        print(f'Activity recorded: {args.record_activity[1]}') 
    if args.get_activity: 
        activities = get_user_activity(args.get_activity) 
        for activity in activities: 
            log_event('INFO', f"Fetched activity for user {args.get_activity}: {activity[2]}") 
            print(f'Timestamp: {activity[3]}, User: {activity[1]}, Activity: {activity[2]}')
if __name__ == '__main__':
    main()
