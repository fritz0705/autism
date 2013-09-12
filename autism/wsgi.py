# coding: utf-8

import http.cookies
import collections

__all__ = [
	"SessionMiddleware",
	"Session"
]

class Session(collections.UserDict):
	def __init__(self, dict=None, sid=None, persistent=None):
		collections.UserDict.__init__(self, dict)
		self.persistent = True if persistent is True else False
		if sid is None:
			self.sid = self._generate_sid()
		else:
			self.sid = sid

	def __repr__(self):
		if self.persistent:
			return "<session [persistent] {0} {1!r}>".format(
				self.sid, self.data)
		return "<session {0} {1!r}>".format(self.sid, self.data)

class SessionMiddleware(object):
	session_cookie = "SESSID"
	app = None
	persistence = None

	def __init__(self, app, persistence=None, session_cookie=None):
		if session_cookie is not None:
			self.session_cookie = session_cookie
		if persistence is not None:
			self.persistence = persistence
		else:
			self.persistence = {}
		self.app = app

	def __call__(self, environ, start_response):
		session = None

		reqcookie = http.cookies.SimpleCookie(environ.get("HTTP_COOKIE", ""))
		session_id = None
		if self.session_cookie in reqcookie:
			session_id = reqcookie[self.session_cookie].value
		del reqcookie

		if session_id and session_id in self.persistence:
			session = Session(self.persistence[session_id], session_id)
			session.persistent = True
		del session_id
		
		if session is None:
			session = Session()
		
		def _start_response(status, header):
			cookie = http.cookies.SimpleCookie()
			cookie[self.session_cookie] = session.sid
			header.append(tuple(str(cookie).split(": ", 1)))

			return start_response(status, header)

		environ["autism.session"] = session

		out = self.app(environ, _start_response)

		if session:
			self.persistence[session.sid] = session

		return out

