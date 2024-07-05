import os

# File to store the user count
DATA_FOLDER = 'data'
USER_COUNT_FILE = os.path.join(DATA_FOLDER, 'user_count.txt')

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

def get_user_count():
    if not os.path.exists(USER_COUNT_FILE):
        return 10  # Start with 10 users
    with open(USER_COUNT_FILE, 'r') as f:
        return int(f.read().strip())

def update_user_count(delta):
    count = max(10, get_user_count() + delta)  # Ensure count doesn't go below 10
    with open(USER_COUNT_FILE, 'w') as f:
        f.write(str(count))
    return count

# CSS for the user count
USER_COUNT_CSS = """
<style>
.user-count {
    margin-top: 1rem;
    font-weight: bold;
    color: #4a4a4a;
}

@media screen and (max-width: 768px) {
    .user-count {
        font-size: 0.9rem;
    }
}
</style>
"""