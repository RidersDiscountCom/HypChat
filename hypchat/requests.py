from __future__ import absolute_import, division
import requests

class BearerAuth(requests.auth.AuthBase):
	def __init__(self, token):
		self.token = token
	
	def __call__(self, r):
		r.headers['Authorization'] = "Bearer %s" % self.token
		return r

def req(method, url, params=None, data=None):
	c = getattr(requests, method.lower())
	kwargs = {}
	if params is not None:
		kwargs['params'] = params
	if data is not None:
		kwargs['headers'] = {'content-type': 'application/json'}
		kwargs['data'] = json.dumps(data)
	return c(url, auth=BearerAuth(AUTH_TOKEN), **kwargs)

class HttpClientError(requests.exceptions.HTTPError):
	"""The 4xx class of status code is intended for cases in which the client seems to have erred. 
	Except when responding to a HEAD request, the server SHOULD include an entity containing an 
	explanation of the error situation, and whether it is a temporary or permanent condition. These 
	status codes are applicable to any request method. User agents SHOULD display any included 
	entity to the user.
	"""

_http_errors = {}

class HttpBadRequest(HttpClientError):
	"""400 Bad Request

	The request could not be understood by the server due to malformed syntax. The client SHOULD 
	NOT repeat the request without modifications.
	"""
_http_errors[400] = HttpBadRequest

class HttpUnauthorized(HttpClientError):
	"""401 Unauthorized

	The request requires user authentication. The response MUST include a WWW-Authenticate header 
	field (section 14.47) containing a challenge applicable to the requested resource. The client 
	MAY repeat the request with a suitable Authorization header field (section 14.8). If the 
	request already included Authorization credentials, then the 401 response indicates that 
	authorization has been refused for those credentials. If the 401 response contains the same 
	challenge as the prior response, and the user agent has already attempted authentication at 
	least once, then the user SHOULD be presented the entity that was given in the response, since 
	that entity might include relevant diagnostic information. HTTP access authentication is 
	explained in "HTTP Authentication: Basic and Digest Access Authentication".
	"""
_http_errors[401] = HttpUnauthorized

class HttpPaymentRequired(HttpClientError):
	"""402 Payment Required

	This code is reserved for future use.
	"""
_http_errors[402] = HttpPaymentRequired

class HttpForbidden(HttpClientError):
	"""403 Forbidden

	The server understood the request, but is refusing to fulfill it. Authorization will not help 
	and the request SHOULD NOT be repeated. If the request method was not HEAD and the server 
	wishes to make public why the request has not been fulfilled, it SHOULD describe the reason for 
	the refusal in the entity. If the server does not wish to make this information available to 
	the client, the status code 404 (Not Found) can be used instead.
	"""
_http_errors[403] = HttpForbidden

class HttpNotFound(HttpClientError):
	"""404 Not Found

	The server has not found anything matching the Request-URI. No indication is given of whether 
	the condition is temporary or permanent. The 410 (Gone) status code SHOULD be used if the 
	server knows, through some internally configurable mechanism, that an old resource is 
	permanently unavailable and has no forwarding address. This status code is commonly used when 
	the server does not wish to reveal exactly why the request has been refused, or when no other 
	response is applicable.
	"""
_http_errors[404] = HttpNotFound

class HttpMethodNotAllowed(HttpClientError):
	"""405 Method Not Allowed

	The method specified in the Request-Line is not allowed for the resource identified by the 
	Request-URI. The response MUST include an Allow header containing a list of valid methods for 
	the requested resource.
	"""
_http_errors[405] = HttpMethodNotAllowed

class HttpNotAcceptable(HttpClientError):
	"""The resource identified by the request is only capable of generating response entities which 
	have content characteristics not acceptable according to the accept headers sent in the request.

	Unless it was a HEAD request, the response SHOULD include an entity containing a list of 
	available entity characteristics and location(s) from which the user or user agent can choose 
	the one most appropriate. The entity format is specified by the media type given in the 
	Content-Type header field. Depending upon the format and the capabilities of the user agent, 
	selection of the most appropriate choice MAY be performed automatically. However, this 
	specification does not define any standard for such automatic selection.

		Note: HTTP/1.1 servers are allowed to return responses which are not acceptable according 
		to the accept headers sent in the request. In some cases, this may even be preferable to 
		sending a 406 response. User agents are encouraged to inspect the headers of an incoming 
		response to determine if it is acceptable.
	
	If the response could be unacceptable, a user agent SHOULD temporarily stop receipt of more 
	data and query the user for a decision on further actions.
	"""
_http_errors[406] = HttpNotAcceptable

class HttpProxyAuthenticationRequired(HttpClientError):
	"""407 Proxy Authentication Required

	This code is similar to 401 (Unauthorized), but indicates that the client must first 
	authenticate itself with the proxy. The proxy MUST return a Proxy-Authenticate header field 
	(section 14.33) containing a challenge applicable to the proxy for the requested resource. The 
	client MAY repeat the request with a suitable Proxy-Authorization header field (section 14.34). 
	HTTP access authentication is explained in "HTTP Authentication: Basic and Digest Access 
	Authentication".
	"""
_http_errors[407] = HttpProxyAuthenticationRequired

class HttpRequestTimeout(HttpClientError):
	"""408 Request Timeout

	The client did not produce a request within the time that the server was prepared to wait. The 
	client MAY repeat the request without modifications at any later time.
	"""
_http_errors[408] = HttpRequestTimeout

class HttpConflict(HttpClientError):
	"""409 Conflict

	The request could not be completed due to a conflict with the current state of the resource. 
	This code is only allowed in situations where it is expected that the user might be able to 
	resolve the conflict and resubmit the request. The response body SHOULD include enough 
	information for the user to recognize the source of the conflict. Ideally, the response entity 
	would include enough information for the user or user agent to fix the problem; however, that 
	might not be possible and is not required.

	Conflicts are most likely to occur in response to a PUT request. For example, if versioning 
	were being used and the entity being PUT included changes to a resource which conflict with 
	those made by an earlier (third-party) request, the server might use the 409 response to 
	indicate that it can't complete the request. In this case, the response entity would likely 
	contain a list of the differences between the two versions in a format defined by the response 
	Content-Type.
	"""
_http_errors[409] = HttpConflict

class HttpGone(HttpClientError):
	"""410 Gone

	The requested resource is no longer available at the server and no forwarding address is known. 
	This condition is expected to be considered permanent. Clients with link editing capabilities 
	SHOULD delete references to the Request-URI after user approval. If the server does not know, 
	or has no facility to determine, whether or not the condition is permanent, the status code 404 
	(Not Found) SHOULD be used instead. This response is cacheable unless indicated otherwise.

	The 410 response is primarily intended to assist the task of web maintenance by notifying the 
	recipient that the resource is intentionally unavailable and that the server owners desire that 
	remote links to that resource be removed. Such an event is common for limited-time, promotional 
	services and for resources belonging to individuals no longer working at the server's site. It 
	is not necessary to mark all permanently unavailable resources as "gone" or to keep the mark 
	for any length of time -- that is left to the discretion of the server owner.
	"""
_http_errors[410] = HttpGone

class HttpLengthRequired(HttpClientError):
	"""411 Length Required

	The server refuses to accept the request without a defined Content-Length. The client MAY 
	repeat the request if it adds a valid Content-Length header field containing the length of the 
	message-body in the request message.
	"""
_http_errors[411] = HttpLengthRequired

class HttpPreconditionFailed(HttpClientError):
	"""412 Precondition Failed

	The precondition given in one or more of the request-header fields evaluated to false when it 
	was tested on the server. This response code allows the client to place preconditions on the 
	current resource metainformation (header field data) and thus prevent the requested method from 
	being applied to a resource other than the one intended.
	"""
_http_errors[412] = HttpPreconditionFailed

class HttpRequestEntityTooLarge(HttpClientError):
	"""413 Request Entity Too Large

	The server is refusing to process a request because the request entity is larger than the 
	server is willing or able to process. The server MAY close the connection to prevent the client 
	from continuing the request.

	If the condition is temporary, the server SHOULD include a Retry-After header field to indicate 
	that it is temporary and after what time the client MAY try again.
	"""
_http_errors[413] = HttpRequestEntityTooLarge

class HttpRequestUriTooLong(HttpClientError):
	"""414 Request-URI Too Long

	The server is refusing to service the request because the Request-URI is longer than the server 
	is willing to interpret. This rare condition is only likely to occur when a client has 
	improperly converted a POST request to a GET request with long query information, when the 
	client has descended into a URI "black hole" of redirection (e.g., a redirected URI prefix that 
	points to a suffix of itself), or when the server is under attack by a client attempting to 
	exploit security holes present in some servers using fixed-length buffers for reading or 
	manipulating the Request-URI.
	"""
_http_errors[414] = HttpRequestUriTooLong

class HttpUnsupportedMediaType(HttpClientError):
	"""415 Unsupported Media Type

	The server is refusing to service the request because the entity of the request is in a format 
	not supported by the requested resource for the requested method.
	"""
_http_errors[415] = HttpUnsupportedMediaType

class HttpRequestedRangeNotSatisfiable(HttpClientError):
	"""416 Requested Range Not Satisfiable

	A server SHOULD return a response with this status code if a request included a Range 
	request-header field (section 14.35), and none of the range-specifier values in this field 
	overlap the current extent of the selected resource, and the request did not include an 
	If-Range request-header field. (For byte-ranges, this means that the first-byte-pos of all of 
	the byte-range-spec values were greater than the current length of the selected resource.)

	When this status code is returned for a byte-range request, the response SHOULD include a 
	Content-Range entity-header field specifying the current length of the selected resource (see 
	section 14.16). This response MUST NOT use the multipart/byteranges content-type.
	"""
_http_errors[416] = HttpRequestedRangeNotSatisfiable

class HttpExpectationFailed(HttpClientError):
	"""417 Expectation Failed

	The expectation given in an Expect request-header field (see section 14.20) could not be met by 
	this server, or, if the server is a proxy, the server has unambiguous evidence that the request 
	could not be met by the next-hop server.
	"""
_http_errors[417] = HttpExpectationFailed


class HttpServerError(requests.exceptions.HTTPError):
	"""Server Error 5xx

	Response status codes beginning with the digit "5" indicate cases in which the server is aware 
	that it has erred or is incapable of performing the request. Except when responding to a HEAD 
	request, the server SHOULD include an entity containing an explanation of the error situation, 
	and whether it is a temporary or permanent condition. User agents SHOULD display any included 
	entity to the user. These response codes are applicable to any request method.
	"""

class HttpInternalServerError(HttpServerError):
	"""500 Internal Server Error

	The server encountered an unexpected condition which prevented it from fulfilling the request.
	"""
_http_errors[500] = HttpInternalServerError

class HttpNotImplemented(HttpServerError, NotImplementedError):
	"""501 Not Implemented

	The server does not support the functionality required to fulfill the request. This is the 
	appropriate response when the server does not recognize the request method and is not capable 
	of supporting it for any resource.
	"""
_http_errors[501] = HttpNotImplemented

class HttpBadGateway(HttpServerError):
	"""502 Bad Gateway

	The server, while acting as a gateway or proxy, received an invalid response from the upstream 
	server it accessed in attempting to fulfill the request.
	"""
_http_errors[502] = HttpBadGateway

class HttpServiceUnavailable(HttpServerError):
	"""503 Service Unavailable

	The server is currently unable to handle the request due to a temporary overloading or 
	maintenance of the server. The implication is that this is a temporary condition which will be 
	alleviated after some delay. If known, the length of the delay MAY be indicated in a 
	Retry-After header. If no Retry-After is given, the client SHOULD handle the response as it 
	would for a 500 response.

		Note: The existence of the 503 status code does not imply that a server must use it when 
		becoming overloaded. Some servers may wish to simply refuse the connection.
	"""
_http_errors[503] = HttpServiceUnavailable

class HttpGatewayTimeout(HttpServerError):
	"""504 Gateway Timeout

	The server, while acting as a gateway or proxy, did not receive a timely response from the 
	upstream server specified by the URI (e.g. HTTP, FTP, LDAP) or some other auxiliary server 
	(e.g. DNS) it needed to access in attempting to complete the request.

		Note: Note to implementors: some deployed proxies are known to return 400 or 500 when DNS 
		lookups time out.
	"""
_http_errors[504] = HttpGatewayTimeout

class HttpVersionNotSupported(HttpServerError):
	"""505 HTTP Version Not Supported

	The server does not support, or refuses to support, the HTTP protocol version that was used in 
	the request message. The server is indicating that it is unable or unwilling to complete the 
	request using the same major version as the client, as described in section 3.1, other than 
	with this error message. The response SHOULD contain an entity describing why that version is 
	not supported and what other protocols are supported by that server.
	"""
_http_errors[505] = HttpVersionNotSupported


class Requests(requests.sessions.Session):
	"""
	Class that extends the requests module in two ways:
	 * Supports default arguments, for things like repeated Auth
	 * Raise errors when requests go poorly
	"""
	
	def __init__(self, **kwargs):
		self._template = kwargs.copy()
		super(Requests, self).__init__()
	
	def _kw(self, kwargs):
		kw = self._template.copy()
		kw.update(kwargs)
		return kw
	
	def request(self, method, url, **kwargs):
		rv = super(Requests, self).request(method, url, **self._kw(kwargs))
		# Raise one of our specific errors
		if rv.status_code in _http_errors:
			raise _http_errors[rv.status_code](rv.text, response=rv)
		# Try to raise for errors we didn't code for
		rv.raise_for_status()
		return rv
