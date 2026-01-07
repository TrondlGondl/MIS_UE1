from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from PatientPortalApp.models import Patient, Practitioner, Questionaire_Template
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser



def perform_register(request): #nur Patienten Login!!
    registration_status = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        svnr = request.POST.get("svnr")
        birthday_str = request.POST.get("birthday")
        # Validierung der Eingaben
        if not username or not password or not email or not svnr or not birthday_str:
            registration_status = "Bitte fülle alle Felder aus."
        elif User.objects.filter(username=username).exists():
            registration_status = "Benutzername existiert bereits."
        else:
            
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user.is_active = False  # muss vom Admin aktiviert werden
            user.save()

            # Patient erstellen
            Patient.objects.create(
                user=user,
                SVNR=svnr,
                birthday=birthday_str
            )

            registration_status = (
                "Registrierung erfolgreich! Dein Konto muss von einem Admin aktiviert werden."
            )

    return render(
        request,
        "register.html",
        {
            "registration_status": registration_status,
        },
    )


def perform_register_practitioner(request): 
    registration_status = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        specialization = request.POST.get("specialization")

        # Eingabeprüfung
        if not username or not password or not email or not specialization:
            registration_status = "Bitte fülle alle Felder aus."
        elif User.objects.filter(username=username).exists():
            registration_status = "Benutzername existiert bereits."
        else:
            # User erstellen
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            user.is_active = False  # muss von Admin aktiviert werden
            user.save()

            # Practitioner erstellen
            Practitioner.objects.create(
                user=user,
                specialization=specialization
            )

            registration_status = (
                "Registrierung erfolgreich! Dein Konto muss von einem Admin aktiviert werden."
            )

    return render(
        request,
        "register_staff.html",
        {"registration_status": registration_status},
    )



def perform_login(request: HttpRequest): 
    login_status = ""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user: AbstractUser | None = authenticate(request, username=username, password = password)
        
        
        if user is not None:
            login(request, user)
            login_status = "SUCCESFULL" 
            return redirect("/dashboard")  #wird direkt umgeleitet zum Dashboard
        else:
            login_status = "Failed"
    
    


    return render(request, "login.html", context={"login_status": login_status})


def perform_logout(request: HttpRequest): 
    logout(request)
    return redirect("/login")


def dashboard(request: HttpRequest):
   
    return render(request, "dashboard.html")


def practitioner_assigned(request: HttpRequest):
    
    if(Patient.practitioner is not None):
        practitioner = None

    else: 
        practitioner = Patient.practitioner


    return render(request, "login.html", context={"login_status": practitioner})





from django.shortcuts import render
from .models import Practitioner, Patient

def dashboard(request):
    # 🚫 Wenn Benutzer nicht eingeloggt ist → Template mit Warnung zeigen
    if not request.user.is_authenticated:
        return render(request, "dashboard.html", {"not_logged_in": True})

    practitioners = Practitioner.objects.all()
    patients = Patient.objects.all()
    status_message = ""

    # Admin kann Zuweisungen vornehmen
    if request.user.is_superuser and request.method == "POST":
        practitioner_id = request.POST.get("practitioner_id")
        patient_id = request.POST.get("patient_id")

        if practitioner_id and patient_id:
            practitioner = Practitioner.objects.get(id=practitioner_id)
            patient = Patient.objects.get(id=patient_id)
            patient.practitioner = practitioner
            patient.save()
            status_message = f"Patient '{patient.user.username}' wurde '{practitioner.user.username}' zugewiesen."

    # Practitioner-Ansicht
    practitioner_patients = None
    practitioner = Practitioner.objects.filter(user=request.user).first()
    if practitioner:
        practitioner_patients = Patient.objects.filter(practitioner=practitioner)

    # Patient-Ansicht
    patient_fragebogen = None
    assigned_practitioner = None
    patient = Patient.objects.filter(user=request.user).first()
    if patient:
        patient_fragebogen = patient.questionare_completed
        assigned_practitioner = patient.practitioner

    return render(
        request,
        "dashboard.html",
        {
            "practitioners": practitioners,
            "patients": patients,
            "status_message": status_message,
            "practitioner_patients": practitioner_patients,
            "patient_fragebogen": patient_fragebogen,
            "assigned_practitioner": assigned_practitioner,
        },
    )





def fill_questionaire(request):
    patient = Patient.objects.filter(user=request.user).first()
    if not patient:
        return redirect("dashboard")

    template = Questionaire_Template.objects.filter(is_active=True).order_by('-version').first()
    if not template:
        return render(request, "questionaire.html", {"error": "Kein aktiver Fragebogen vorhanden."})

    # Variable initialisieren
    answers = {}

    if request.method == "POST":
        for i, question in enumerate(template.questions):
            selected_answer = request.POST.get(f"question_{i}")
            if selected_answer:
                answers[question["question"]] = selected_answer
            else:
                answers[question["question"]] = None  # falls Frage unbeantwortet
        # Antworten im Patient speichern
        patient.questionare_data = answers
        patient.questionare_completed = True
        patient.save()
        return redirect("dashboard")

    return render(request, "questionaire.html", {"template": template})



def crash(request: HttpRequest):
    raise Exception(500)