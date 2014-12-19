import os, sys

def become_daemon(our_home_dir='.', out_log='/dev/null', err_log='/dev/null', pidfile='/var/tmp/daemon.pid'):
    """ Make the current process a daemon.  """

    try:
        # First fork
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed" (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.chdir(our_home_dir)
        os.umask(0)

        # Second fork
        try:
            pid = os.fork()
            if pid > 0:
                # You must write the pid file here.  After the exit()
                # the pid variable is gone.
                fpid = open(pidfile, 'wb')
                fpid.write(str(pid))
                fpid.close()
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed" (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

        si = open('/dev/null', 'r')
        so = open(out_log, 'a+', 0)
        se = open(err_log, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    except Exception, e:
        sys.stderr.write(str(e))