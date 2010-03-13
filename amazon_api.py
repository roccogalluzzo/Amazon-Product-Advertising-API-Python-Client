import urllib, re,time, urllib2, hmac, hashlib, base64
from urlparse import urlparse

class AwsProductApi:
	"Class for send requests on Amazon Product Advertising API."
 
	def __init__(self, host, access_key, secret_key):
 
		self.host = host
		self.access_key = access_key
		self.secret_key = secret_key
 
	def _raw_request(self, params):
		"Used by other method of class for send a request."
		# Params common to all requests
		params['Service'] = 'AWSECommerceService'
		params['Version'] = '2009-10-01'
		# Set access key
		params['AWSAccessKeyId'] = self.access_key
		# Calculate the timedate to send request by API
		params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
		# encode the url params based on RFC 3986
		keys =map(lambda x: urllib.quote(x,safe='~'), params.keys())
		values = map(lambda x: urllib.quote(x,safe='~'), params.values())
		# Sort keys in ASCII order
		keys = self._ascii_sort(keys)
		# Remap the dict for respect the ASCII order
		values = map(params.get, keys)
		# Build URL paramtres from dict and ancode them with = and &
		url_params = urllib.urlencode( zip(keys,values) )
		# Retrieve host and path
		url = urlparse(self.host)
		 
		# Build string to sign
		sign_string = "GET\n%s\n%s\n%s"%(url.netloc, url.path, url_params)
		# Build signature
		signature = hmac.new(self.secret_key , sign_string, hashlib.sha256).digest()
		signature = base64.encodestring(signature)
		# Encode url safe the signature
		signature = signature.rstrip()
		signature = urllib.quote(signature,safe='~')
		# Send request
		#s = urllib2.urlopen(
		print "%s?%s&Signature=%s" % (self.host, url_params, signature)
		# Return XML data
		#return s.read()
 
	def _ascii_sort(self, l ):
		"Sort the given list in ASCII order."
		 
		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
		return sorted(l, key=alphanum_key )
		
	def ItemLookup (self, params):
		"Send an ItemLookup request"
		params['Operation']='ItemLookup'
		self._raw_request(params)
	
	def ItemSearch (self, params):
		"Send an ItemLookup request"
		params['Operation']='ItemSearch'
		self._raw_request(params)
		
	def BrowseNodeLookup(self, params):
		"Send an BrowseNodeLookup request"
		params['Operation']='ItemSearch'
		self._raw_request(params)
		
		
