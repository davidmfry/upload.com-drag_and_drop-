import mandrill

mandrill_client = mandrill.Mandrill('7mkIVyEhxG6rQkMo_TA0-g')
try:
	message = {'from_email': 'message.david.fry.tv@gmail.com',
	     		'from_name': 'Python Script',
	     		'to': [{'email': 'david.fry.tv@gmail.com',
	            		'name': 'David Fry',
	             		'type': 'to'}],
	             'subject': 'It is exciting to send from python',
	             'text': 'This is a test from the Mandrill API and email system',

	     		}
	result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool', send_at='')
except mandrill.Error, e:
    # Mandrill errors are thrown as exceptions
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
    raise