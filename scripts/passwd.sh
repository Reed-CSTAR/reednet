#!/bin/sh
#
# We put this into /usr/local/bin so that shells find it first when a user runs
# passwd. It's still possible to run /bin/passwd just in case.
# 
# TODO: Is this sufficient for GNOME?

cat <<EOF
$(printf '\033[31;1m')Please do not change your password on this machine!$(printf '\033[0m')

Instead, change your password on Polly via SSH:

	$ ssh $(whoami)@polly.reed.edu
	$(whoami)@polly:~$ passwd

Once you change your password there, it will propagate to other machines.

If you really want to change your password on this machine (and only this
machine!), you can refer to the passwd utility by its normal path. Note that
your password change will be overriden without notice.
EOF
