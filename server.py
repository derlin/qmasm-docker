import cherrypy
import subprocess
from datetime import datetime
import traceback, sys, os

# not_supported = 'o', 'output', 'topology-file'
one_minus = ['h', 'v', 'f', 'O', 'p', 'C', 'P', 'q', 's', 'E']
two_minus = ['help', 'verbose', 'run', 'f', 'pin', 'values', 'chain-strength', 'pin-weight', 'qubo', 'samples', 'anneal-time', 'spin-revs', 'extra-args', 'always-embed', 'postproc', 'show', 'format']
available_arguments = dict([(k, "-%s %s") for k in one_minus] + [(k, "--%s %s") for k in two_minus])
default_arguments = dict(format="qbsolv", values="ints")

class QmasmWrapper(object):
    def __init__(self):
        self._help = None

    def get_help(self):
        if self._help is None: self._help = self._run_command('qmasm --help')
        return self._help

    def process_args(self, given_args):
        args = dict(**default_arguments)
        args.update(given_args)
        print "args %s" % args
        return [ available_arguments[k] % (k,v)
                for (k,v) in args.items()
                if k in available_arguments ]


    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
    def index(self, **query_args):
        try:
            if cherrypy.request.method != 'POST':
                if 'help' in query_args:
                    return self.get_help() 
                else:
                    return "Expecting a post with qmasm file as body"

            qmasm_arguments = " ".join(self.process_args(query_args))
            print "qmasm args %s" % qmasm_arguments
            body = cherrypy.request.body.read()

            filename = "/tmp/%s.qmasm" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(filename, 'w') as f: f.write(body)

            command = 'qmasm %s %s' % (filename, qmasm_arguments)
            print "launching %s" % command

            output = self._run_command(command)
            os.remove(filename)
            return output

        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            cherrypy.response.status = 500
            return e.output

    def _run_command(self, command):
        return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

if __name__ == '__main__':
    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.server.socket_port = 80

    conf = {
        '/': {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }

    cherrypy.quickstart(QmasmWrapper(), '/', conf)
