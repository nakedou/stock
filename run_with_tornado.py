import argparse
import datetime
import os
import posix
import re
import signal
import sys

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from app import create_app

app = create_app()


def setup_stdio_linebuffer():
    if not sys.stdout.isatty():
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
    if not sys.stderr.isatty():
        sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 1)


def stop_server():
    IOLoop.instance().stop()


def gen_worker_sig_handler_stop_server(xperf_thread):
    def worker_sig_handler_stop_server(signum, frame):
        nonlocal xperf_thread
        if xperf_thread:
            xperf_thread.stop()
            xperf_thread.join()
        stop_server()
    return worker_sig_handler_stop_server


def master_sig_handler_stop_server(signum, frame):
    print("Signal {} received, server will be stopped".format(signum))
    posix.kill(0, signal.SIGINT)
    posix.wait()
    sys.exit(0)


def register_signal_handler_for_master():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGQUIT, master_sig_handler_stop_server)


def register_signal_handler_for_worker(xperf_thread=None):
    signal.signal(signal.SIGINT, gen_worker_sig_handler_stop_server(xperf_thread))


def expand_num_list(str_list):
    """1-3,5-7,9 => [1,2,3,5,6,7,9]"""
    str_format = re.compile("^(\d+-\d+|\d+)(,(\d+-\d+|\d+))*$")
    if not str_format.match(str_list):
        return []
    result = set()
    re_range = re.compile("(\d+)-(\d+)")
    ranges = str_list.split(",")
    for unit in ranges:
        if unit.isdigit():
            result.add(int(unit))
        else:
            m = re_range.match(unit)
            if not m:
                continue
            result.update(list(range(int(m.group(1)), int(m.group(2)) + 1)))
    return list(result)


def main():
    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-p", "--port", action="store", dest="port", type=int,
                        help="listening port", default=8000)
    parser.add_argument("-n", "--num_processes", action="store", dest="num_processes", type=int,
                        help="num of worker processes", default=8)
    parser.add_argument("-m", "--multi_port", action="store_true", dest="multi_port",
                        help="use different port for each process", default=False)
    parser.add_argument("-c", "--cpu_set", action="store", dest="cpu_set",
                        help="run on cpu set", default="")
    parser.add_argument("-x", "--xperf", action="store_true", dest="xperf",
                        help="collect call stacks with python-flamegraph", default=False)
    args = parser.parse_args()

    print("Server starting with master pid {}".format(posix.getpid()))
    posix.setpgid(0, 0)
    register_signal_handler_for_master()

    if args.xperf:
        dest_dir = "xperf-log/{}".format(datetime.datetime.utcnow().timestamp())
        os.system("mkdir -p {}".format(dest_dir))

    port = args.port
    if not args.multi_port:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.bind(port)
        #http_server.start(args.num_processes)
        tornado.process.fork_processes(args.num_processes)
        sockets = http_server._pending_sockets
        http_server._pending_sockets = []
        http_server.add_sockets(sockets)
    else:
        tornado.process.fork_processes(args.num_processes)
        sockets = tornado.netutil.bind_sokets(args.port + tornado.process.task_id())
        http_server = HTTPServer(WSGIContainer(app))
        http_server.add_sockets(sockets)

    thread = None
    if args.xperf:
        from flamegraph.flamegraph import ProfileThread
        thread = ProfileThread(open("{}/perf-{}.log".format(dest_dir, posix.getpid()), "w"), 0.001, None)
        thread.start()

    register_signal_handler_for_worker(thread)
    IOLoop.instance().start()

if __name__ == "__main__":
    setup_stdio_linebuffer()
    # config log

    main()
