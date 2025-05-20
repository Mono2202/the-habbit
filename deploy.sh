#!/bin/bash

SESSION="the-habbit"

# Kill any existing session with the same name
tmux has-session -t $SESSION 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Killing existing tmux session: $SESSION"
    tmux kill-session -t $SESSION
fi

# Start new detached session
echo "Starting new tmux session: $SESSION"
tmux new-session -d -s $SESSION

# Start backend in a new window
tmux new-window -t $SESSION -n 'backend'
tmux send-keys -t $SESSION:1 'cd /home/mono/projects/the-habbit/backend && pip install -r requirements.txt --break-system-packages && python app.py' C-m

# Start frontend in another window
tmux new-window -t $SESSION -n 'frontend'
tmux send-keys -t $SESSION:2 'cd /home/mono/projects/the-habbit/frontend' C-m
tmux send-keys -t $SESSION:2 'npm run build' C-m
tmux send-keys -t $SESSION:2 'serve -s build -l 5002' C-m

echo "Deployment started in tmux session: $SESSION"

