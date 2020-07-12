#!/bin/bash

# We want to trigger the script only when the SSH session starts.
# To be notified also when session closes, you can watch for 
# the "close_session" value.
if [[ "$PAM_TYPE" != "open_session" ]]; then
        exit 0
fi

read -r -d '' CONTENT <<-EOF || true
Host: $(hostname)
User: $(echo $PAM_USER)
Now UTC: $(date --utc "+%F %T")
Env:
$(printenv)
EOF

echo "$CONTENT" | mail -s "[ssh] $PAM_USER logged to $(hostname)" ${MAIL_TO_SEND}