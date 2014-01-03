#!/bin/sh
 
### BEGIN INIT INFO
# Provides: typesetter
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Pi Key Logging Typesetter
# Description: Typesets keylogs on shutdown
### END INIT INFO


. /lib/lsb/init-functions
 
do_start () {
sudo typesetter
log_daemon_msg "Running Typesetter"
# start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --startas $DAEMON
log_end_msg $?
}
do_stop () {
sudo typesetter
log_daemon_msg "Stopping Typesetter"
# start-stop-daemon --stop --pidfile $PIDFILE --retry 10
log_end_msg $?
}
 
case "$1" in
 
start|stop)
do_${1}
;;
*)
echo "Usage: /etc/init.d/$DEAMON_NAME {start|stop}"
exit 1
;;
 
esac
exit 0