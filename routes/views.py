from django.shortcuts import render , redirect, get_object_or_404 
from django.http import HttpResponse , JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Task , User, PushSubscription
from .forms import TaskForm
import random, requests, json
from webpush import send_user_notification
from webpush.models import PushInformation
from django.http import FileResponse
import os
from django.conf import settings
from pywebpush import webpush, WebPushException

# Create your views here.

def task_list(request):
    return render(request, 'tasks.html', {"tasks" : Task.objects.filter(user_id = request.session.get("id"))} )

def home(request):
    pass


def savenewtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
            
    return HttpResponse(form.cleaned_data['date'])

def newtask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = User.objects.get(id= request.session.get("id"))
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, 'newtask.html', {'form': form})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Replace with your list view name
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})


# views.py
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')
    #return render(request, 'confirm_delete.html', {'task': task})

#now the user implementation type thingy

def check_if_there_is_any_user_already_logged_in(request):
    loggedin_id = request.session.get("id")
    if loggedin_id :
        return redirect("tasks/")
    else:
        return redirect("login/")

def signup(request):
    return render(request, "register.html")

def register(request):
    global newusername, newpassword, newemail
    newusername = request.GET.get("username")
    newpassword = request.GET.get("password")
    newconfirmpwd = request.GET.get("confirm password")
    newemail = request.GET.get("mail")
    if newpassword == newconfirmpwd:
        if newemail in User.objects.values_list('email', flat=True):
            return HttpResponse(b'email already exists')
        else:
            return redirect('sendverificationemail', recipient=newemail)
        return redirect('/emailverify')
    signup_url = reverse('signup')
    return redirect(signup_url)

def login(request):
    return render(request, 'login.html')

def verify(request):
    Username = request.POST.get("username")
    Password = request.POST.get("password")
    try:
        user = User.objects.get(name = Username, password = Password)
        request.session["id"] = user.id
        return redirect('/')
    except:
        return redirect("login")


otpToBeChecked = None

def send_verification_email(request, recipient):
    otp = random.randint(10000, 99999)
    global otpToBeChecked
    otpToBeChecked = otp
    API_KEY = "D1F821EF57B5634978B993DF2E95075C386A95F08D2A725334E8CDC953CC449719065A94D3C498C64FEC4DFFBD6DA1E2" #'5E75CD07C85BBFE9A85475B4EB1E46102E041EEC354083B208B11420D482F6FCA3CDB2B1DC2B060B99F8C2250B03A522'
    url = "https://api.elasticemail.com/v2/email/send"
    payload = {
            'apikey': API_KEY,
            'subject': 'verification code for your account registration',
            'from': 'kowshikgarapati@gmail.com',
            'to': recipient, # request.GET.get('recipient'),
            'bodyHtml': f'<h1>{otp} is the OTP for your devcolab registration</h1>',
            'isTransactional': False
    }

        # Send a POST request to Elastic Email
    response = requests.post(url, data=payload)

        # Check response
    if response.status_code == 200:
        print(f"Email sent successfully! {otp}")
    else:
        print("Failed to send email:", response.json())
    return redirect('verifyotp')


def verifyotp(request):
    return render(request, "otpverification.html")

def emailverify(request):
    entered_otp = request.GET.get("otp")
    if entered_otp == str(otpToBeChecked):
        user_created = User.objects.create(name=newusername, password=newpassword, email=newemail)
        request.session['id'] = user_created.id
        return redirect('task_list')
    else:
        return redirect('signup')

def logout(request):
    request.session.flush()
    return redirect("checkifuserloggedin")

VAPID_PRIVATE_KEY = "5UMfwX2ybkCYjwZxlVLvLhURiYPNwyeAIkI0BtwmYKU"
VAPID_PUBLIC_KEY = "BMov4lzyLO5ZFKs5uuCXHtmE0yo6Z7-cTpth3oQVrgWroh07h0lQM6neggYlc8AGd5vj0cunf_QwmB0Gqhgb44Q"

def gpstesting(request):
    context = {
        "vapid_public_key": "BMov4lzyLO5ZFKs5uuCXHtmE0yo6Z7-cTpth3oQVrgWroh07h0lQM6neggYlc8AGd5vj0cunf_QwmB0Gqhgb44Q"  # Same as in settings
    }
    return render(request, "GPSTest.html", context)

def send_notification(request):
    payload = {
        "title": "🚀 Django Push",
        "body": "Your web push notification is working perfectly!",
        "icon": "/static/icons/notification.png"
    }

    subs = PushSubscription.objects.all()
    if not subs.exists():
        return JsonResponse({"error": "No subscriptions found"}, status=404)

    for sub in subs:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }
                },
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": "mailto:kowshikgarapati@gmail.com"
                }
            )
            print(f"✅ Push sent to: {sub.endpoint[:40]}...")
        except WebPushException as e:
            print(f"❌ Push failed for {sub.endpoint[:40]}: {repr(e)}")
            if e.response and e.response.json():
                print("Response:", e.response.json())

    return JsonResponse({"status": "Notifications sent"})

def save_info(request):
    if request.method == 'POST':
        try:
            subscription_data = json.loads(request.body)

            endpoint = subscription_data['endpoint']
            keys = subscription_data.get('keys', {})

            # Save the subscription in your database (no user here)
            PushSubscription.objects.update_or_create(
                endpoint=endpoint,
                defaults={
                    'auth': keys.get('auth', ''),
                    'p256dh': keys.get('p256dh', '')
                }
            )
            return JsonResponse({'status': 'Subscription saved'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def save_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        endpoint = data.get("endpoint")
        keys = data.get("keys", {})

        if endpoint and "auth" in keys and "p256dh" in keys:
            PushSubscription.objects.update_or_create(
                endpoint=endpoint,
                defaults={
                    "auth": keys["auth"],
                    "p256dh": keys["p256dh"]
                }
            )
            return JsonResponse({"status": "saved"})
        else:
            return JsonResponse({"error": "Missing keys"}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)


@csrf_exempt
def save_information(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # You can log this or save it however you want
        print("Subscription data:", data)
        
        # Save logic here, or just acknowledge
        return JsonResponse({"status": "Subscription saved"})
    return JsonResponse({"error": "Invalid method"}, status=400)

def service_worker(request):
    sw_path = os.path.join(settings.BASE_DIR, r"routes\static\service-worker.js")
    return FileResponse(open(sw_path, "rb"), content_type="application/javascript")