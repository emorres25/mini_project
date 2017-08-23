import json, requests, random, re
from pprint import pprint
 
from django.views import generic
from django.http.response import HttpResponse
 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
verify_token = '8510865767'
 
def get_joke(fbid, recevied_message):
    joke_text = requests.get("http://api.icndb.com/jokes/random/").json()['value']['joke']
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%'EAABkitQTatQBAPosC3d3O4d6dBRWC95mCuhHFfZCReaiqw3wZC1N36bktjjGyjyE6g1ve2ZBekHHo6hX6ZCOhHIwLZAd7lhQ9zaviSL6UVjp3eYu0un6swliknSPBuSAeFukSdQvcChdoiDEhCxhnJOuUmqRD39D7YJZAp1sDMfwZDZD'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
 
class jokebot(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
 
 
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']: 
                if 'message' in message: 
                    get_joke(message['sender']['id'], message['message']['text'])    
        return HttpResponse()