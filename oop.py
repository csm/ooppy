r"""ooppy is a simple module for programming event loops in python; its
design is based on the liboop API."""

__version__ = '0.0.1'
__author__ = 'Casey Marshall <casey.s.marshall@gmail.com>'

SOCKET_READ = 1 << 0
SOCKET_WRITE = 1 << 1
SOCKET_EXCEPTION = 1 << 2

TIMER_ONESHOT = 1
TIMER_REPEAT  = 2

# Callback return values.
CONTINUE = 1
EXIT = 2
EXCEPTION = 3

class EventLoop(object):
	def __init__(self):
		self.sockets = {}
		self.timers = {}

	def on_socket(self, socket, what, handler, args=()):
		'''Add a socket or pipe to this event loop.
		
		Argument list:
			socket - The socket (or, possibly a UNIX pipe) to wait for events on.
			what - A bit set of SOCKET_* constants, tells what to wait for:
				- SOCKET_READ: wait for the socket to become readable (run when input is available).
				- SOCKET_WRITE: wait for the socket to become writable.
				- SOCKET_EXCEPTION: wait for exceptions on the socket.
			handler - A function to invoke when the event is triggered.
			args - A list of arguments to pass to the handler function.
		'''
		vals = []
		if socket in self.sockets:
			vals = self.sockets[socket]
		vals.append([what, handler, args])
		
	def cancel_socket(self, socket, what, handler=None):
		'''Remove a socket or pipe from this even loop.
		
		Argument list:
			socket - The socket (or, possibly a UNIX pipe) to remove.
			what - A bit set of operations you are no longer interested in.
			handler - The handler to remove. If None, all handlers are removed.
		'''
		if socket in self.sockets:
			del self.sockets[socket] # FIXME
	
		
	def on_timer(self, timeout, what, handler, args=()):
		'''Add a timer to this event loop; that is, run a function when the given
		timeout expires.
		
		Arguments are:
			timeout - the timeout, in seconds, to wait (can be fractional).
			what - integer value telling what to do:
				TIMER_ONESHOT: run handler one time, after the timeout expires.
				TIMER_REPEAT: call handler over and over, waiting timeout seconds
					each time.
		'''
		if what != TIMER_ONESHOT and what != TIMER_REPEAT:
			raise TypeError, 'what must be oop.TIMER_ONESHOT or oop.TIMER_REPEAT'
		vals = []
		if timeout in self.timers:
			vals = self.timers[timeout]
		vals.append([what, handler, args])
		
	def cancel_timer(self, timeout, handler=None):
		'''Remove a timer from this event loop.
		
		Arguments are:
			timeout - the timeout value to remove; if zero or negative, search for
					  and remove all handlers that match handler.
			handler - the handler to remove; if None, all handlers for that timeout
			 		  are removed.
		'''
		if timeout <= 0 and handler == None:
			raise TypeError, 'one of timeout or handler must not be 0 or None'
		if timeout <= 0:
			remove = []
			for k, v in self.timers:
				[self.timers[k].remove(v) for v in self.timers[k] if v[1] == handler]
		else:
			if timeout not in self.timers:
				raise KeyError, 'no timer for timeout %s' % str(timeout)
			if handler == None:
				del self.timers[timeout]
			else:
				[self.timers[timeout].remove(v) for v in self.timers[timeout] if v[1] == handler]
		
	def run(self):
		'''Run this event loop continuously, until some handler returns EXIT
		or EXCEPTION.'''
		while True:
			result = run_one(self)
			if result == EXIT or result == EXCEPTION:
				break
		
	def run_one(self):
		pass