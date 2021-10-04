from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from .models import CustomUser, Predmeti, Upisi
from .forms import StudentForm, UserRegisterForm, UserAuthenticationForm, PredmetForm

# Create your views here.


def test(request):
    return render(request, 'test.html', {'title': 'Home'})


def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data['password1']
            account = authenticate(email=email, password=raw_password)
            print(email, raw_password)
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return HttpResponseRedirect(reverse('login'))
        else:
            context['registration_form'] = form
    else:
        form = UserRegisterForm()
        context['registration_form'] = form
    context['title'] = 'Register'

    return render(request, 'register.html', context)


# def login_view(request):
#     context = {}
#     user = request.user


#     if user.is_authenticated:
#         return HttpResponseRedirect(reverse('home'))

#     if request.POST:
#         form = UserAuthenticationForm(request.POST)
#         print(form.is_valid())
#         if form.is_valid():
#             email = request.POST['email']
#             password = request.POST['password']
#             print(email, password)
#             user = authenticate(email=email, password=password)
#             print(user)
#             if user:
#                 login(request, user)
#                 if request.user.role.naziv == "Mentor":
#                     return HttpResponseRedirect(reverse('mentor'))
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = UserAuthenticationForm()

#     context['login_form'] = form
#     context['title'] = 'Login'
#     return render(request, 'login.html', context)


def logout_view(request):
    logout(request)

    context = {}
    context['title'] = 'Logout'
    return render(request, 'logout.html', context)


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.POST:
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if(user.role.naziv == "Mentor"):
                    return HttpResponseRedirect(reverse('mentor'))
                elif(user.role.naziv == "Admin"):
                    return HttpResponseRedirect(reverse('admin'))

                return HttpResponseRedirect(reverse('home'))
    else:
        form = UserAuthenticationForm()

    context['login_form'] = form
    context['title'] = 'Login'
    return render(request, 'login.html', context)


@login_required
def student_view_pk(request, pk):
    context = {}
    user = CustomUser.objects.get(pk=pk)
    upisi = Upisi.objects.all()
    predmeti = Predmeti.objects.all()
    upisi_filtered = set()
    predmeti_filtered = set()
    counter_redovni = 0
    counter_izvaredni = 0
    redovni_polozeni = 0
    izvanredni_polozeni = 0
    if request.user.role.naziv == "Student" and request.user.id != user.id:
        return HttpResponseRedirect(reverse('home'))

    flag = True
    for predmet in predmeti:
        if predmet.sem_redovni == 1 or predmet.sem_redovni == 2:
            counter_redovni = counter_redovni + 1
        if predmet.sem_izvanredni == 3 or predmet.sem_izvanredni == 4:
            counter_izvaredni = counter_izvaredni + 1
        for upis in upisi:
            if predmet.id == upis.predmet_id and user.id == upis.student_id:
                upisi_filtered.add(predmet)
                flag = False

        if flag:
            predmeti_filtered.add(predmet)
        flag = True

    if request.POST:
        for predmet in predmeti_filtered:
            if request.POST.get(str(predmet)):
                new = Upisi(student=user, predmet=predmet, status="nepolozen")
                new.save()
                messages.success(request, "Upisano: " + predmet.ime)
        for upis_f in upisi_filtered:
            if request.POST.get(str(upis_f)):
                for upis in upisi:
                    if upis_f.id == upis.predmet_id and user.id == upis.student_id:
                        if request.POST.get(str(upis_f)) == "not_passed":
                            upisi.filter(pk=str(upis.id)).update(
                                status="nepolozen")
                            messages.success(
                                request, "Nije položeno: " + upis_f.ime)

                        elif request.POST.get(str(upis_f)) == "passed" and request.user.role.naziv == "Mentor":
                            upisi.filter(pk=str(upis.id)).update(
                                status="polozen")
                            messages.success(
                                request, "Položeno: " + upis_f.ime)
                        elif request.POST.get(str(upis_f)) == "remove":
                            upis.delete()
                            messages.success(
                                request, "Ispisano: " + upis_f.ime)
        return HttpResponseRedirect('/student/' + str(pk) + '/')

    upisi_html = ""
    br_sem = 0

    if user.status == "redovni":
        br_sem = 6
    elif user.status == "izvanredni":
        br_sem = 8

    for i in range(br_sem):
        upisi_html += "<div class='semestar'>"
        upisi_html += "<p>Semestar " + str(i+1) + ":</p>"
        upisi_html += "<table>"
        for upis in upisi:
            predmet = predmeti.get(pk=str(upis.predmet_id))
            if user.id == upis.student_id:
                if user.status == "redovni" and predmet.sem_redovni == i+1:
                    if upis.status == "polozen":
                        upisi_html += "<tr><td></td><td><button type='submit' class='add-btn' name='" + \
                            str(predmet) + \
                            "' value='not_passed'>&#10004;</button></td>"
                    elif upis.status == "nepolozen":
                        if request.user.role.naziv == "Mentor":
                            upisi_html += "<tr><td><button type='submit' class='add-btn' name='" + \
                                str(predmet) + \
                                "' value='passed'>&#10004;</button></td>"
                        upisi_html += "<td><button type='submit' class='add-btn' name='" + \
                            str(predmet) + \
                            "' value='remove'>&#10006;</button></td>"
                    upisi_html += "<td>" + predmet.ime + "</td></tr>"
                elif user.status == "izvanredni" and predmet.sem_izvanredni == i+1:
                    if upis.status == "polozen":
                        upisi_html += "<tr><td></td><td><button class='add-btn' type='submit' name='" + \
                            str(predmet) + \
                            "' value='not_passed'>&#10004;</button></td>"
                    elif upis.status == "nepolozen":
                        if request.user.role.naziv == "Mentor":
                            upisi_html += "<tr><td><button type='submit' class='add-btn' name='" + \
                                str(predmet) + \
                                "' value='passed'>&#10004;</button></td>"
                        upisi_html += "<td><button type='submit' class='add-btn' name='" + \
                            str(predmet) + \
                            "' value='remove'>&#10006;</button></td>"
                    upisi_html += "<td>" + predmet.ime + "</td></tr>"
        upisi_html += "</table>"
        upisi_html += "</div>"
    if user.status == "redovni":
        for upis in upisi:
            temp_predmet = Predmeti.objects.get(pk=upis.predmet_id)
            # print(temp_predmet.sem_redovni)
            if upis.student_id == user.id and (temp_predmet.sem_redovni == 1 or temp_predmet.sem_redovni == 2) and upis.status == "polozen":
                redovni_polozeni = redovni_polozeni + 1
    else:
        for upis in upisi:
            temp_predmet = Predmeti.objects.get(pk=upis.predmet_id)
            print(temp_predmet.sem_redovni)
            if upis.student_id == user.id and (temp_predmet.sem_izvanredni == 3 or temp_predmet.sem_izvanredni == 4) and upis.status == "polozen":
                izvanredni_polozeni = izvanredni_polozeni + 1

    context = {
        'user': user,
        'predmeti': predmeti_filtered,
        'upisi': upisi_html,
        'title': user.email,
        'redovni_polozeni': redovni_polozeni,
        'counter_redovni': counter_redovni,
        'counter_izvaredni': counter_izvaredni,
    }
    print(counter_redovni)
    print(redovni_polozeni)

    return render(request, 'student.html', context)


@login_required
def mentor_view(request):
    print(request.user.role.naziv)
    if request.user.role.naziv != "Mentor":
        print(request.user.role.naziv)
        return HttpResponseRedirect(reverse('home'))
    context = {}
    context['title'] = str(request.user.email)
    return render(request, 'mentor.html', context)


@login_required
def mentor_studenti_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'mentor_studenti.html', context)


@login_required
def admin_studenti_redovni_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_studenti_redovni.html', context)


@login_required
def admin_studenti_izvanredni_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_studenti_izvanredni.html', context)


@login_required
def mentor_predmeti_view(request):
    print(request)
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    predmeti = Predmeti.objects.filter(nositelj=request.user.id)
    #predmeti = Predmeti.objects.all()
    for predmet in predmeti:
        print(predmet.nositelj)
    if request.POST:
        for predmet in predmeti:
            if request.POST.get(str(predmet)) == 'delete':
                messages.success(request, "Izbrisano: " + str(predmet.ime))
                predmet.delete()
                return HttpResponseRedirect(reverse('mentor_predmeti'))
            elif request.POST.get(str(predmet)) == 'edit':
                return HttpResponseRedirect(reverse('mentor_predmeti_edit', args=(predmet.id,)))
    context = {
        'predmeti': predmeti,
        'title': str(request.user.email),
    }
    return render(request, 'mentor_predmeti.html', context)


@login_required
def mentor_predmeti_add_view(request):
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = PredmetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Predmet has been created!')
            return HttpResponseRedirect(reverse('mentor_predmeti'))
        else:
            context['predmet_add_form'] = form
    else:
        form = PredmetForm()
        context['predmet_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'mentor_predmeti_add.html', context)


@login_required
def mentor_predmeti_edit_view(request, pk):
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    predmet = Predmeti.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = PredmetForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Predmet has been edited!')
            return HttpResponseRedirect(reverse('mentor_predmeti'))
        else:
            context['predmet_edit_form'] = form
    else:
        form = PredmetForm(instance=predmet)
        context['predmet_edit_form'] = form
    context['predmet'] = predmet
    context['title'] = str(request.user.email)

    return render(request, 'mentor_predmeti_edit.html', context)


@login_required
def mentor_view(request):
    print(request.user.role.naziv)
    if request.user.role.naziv != "Mentor":
        print(request.user.role.naziv)
        return HttpResponseRedirect(reverse('home'))
    context = {}
    context['title'] = str(request.user.email)
    return render(request, 'mentor.html', context)


@login_required
def admin_studenti_add_view(request):
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student has been created!')
            return HttpResponseRedirect(reverse('mentor_studenti'))
        else:
            context['student_add_form'] = form
    else:
        form = StudentForm()
        context['student_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'admin_studenti_add.html', context)


@login_required
def admin_studenti_edit_view(request, pk):
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    student = CustomUser.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student has been edited!')
            return HttpResponseRedirect(reverse('mentor_studenti'))
        else:
            context['student_edit_form'] = form
    else:
        form = StudentForm(instance=student)
        context['student_edit_form'] = form
    context['student'] = student
    context['title'] = str(request.user.email)

    return render(request, 'admin_studenti_edit.html', context)


@login_required
def admin_mentori_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_mentori.html', context)


@login_required
def admin_view(request):
    print(request.user.role.naziv)
    if request.user.role.naziv != "Admin":
        print(request.user.role.naziv)
        return HttpResponseRedirect(reverse('home'))
    context = {}
    context['title'] = str(request.user.email)
    return render(request, 'admin.html', context)


@login_required
def admin_studenti_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_studenti.html', context)


@login_required
def admin_predmeti_view(request):
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    predmeti = Predmeti.objects.all()

    if request.POST:
        for predmet in predmeti:
            if request.POST.get(str(predmet)) == 'delete':
                messages.success(request, "Izbrisano: " + str(predmet.ime))
                predmet.delete()
                return HttpResponseRedirect(reverse('admin_predmeti'))
            elif request.POST.get(str(predmet)) == 'edit':
                return HttpResponseRedirect(reverse('admin_predmeti_edit', args=(predmet.id,)))
    context = {
        'predmeti': predmeti,
        'title': str(request.user.email),
    }
    return render(request, 'admin_predmeti.html', context)


@login_required
def admin_predmeti_edit_view(request, pk):

    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    predmet = Predmeti.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = PredmetForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            messages.success(request, f'Predmet has been edited!')
            return HttpResponseRedirect(reverse('admin_predmeti'))
        else:
            context['predmet_edit_form'] = form
    else:
        form = PredmetForm(instance=predmet)
        context['predmet_edit_form'] = form
    context['predmet'] = predmet
    context['title'] = str(request.user.email)

    return render(request, 'admin_predmeti_edit.html', context)


@login_required
def admin_predmeti_add_view(request):
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = PredmetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Predmet has been created!')
            return HttpResponseRedirect(reverse('admin_predmeti'))
        else:
            context['predmet_add_form'] = form
    else:
        form = PredmetForm()
        context['predmet_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'admin_predmeti_add.html', context)


@login_required
def admin_predmeti_studenti_view(request, pk):
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    predmet = Predmeti.objects.get(pk=pk)
    print(predmet.ime)
    users = CustomUser.objects.filter(role=3)
    upisi = Upisi.objects.filter(predmet=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for upis in upisi:
        for user in users:
            if upis.student.id == user.id:
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'admin_predmeti_studenti.html', context)


@login_required
def mentor_predmeti_studenti_view(request, pk):
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    predmet = Predmeti.objects.get(pk=pk)
    print(predmet.ime)
    users = CustomUser.objects.filter(role=3)
    upisi = Upisi.objects.filter(predmet=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for upis in upisi:
        for user in users:
            if upis.student.id == user.id:
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)
    context['predmet'] = predmet

    return render(request, 'mentor_predmeti_studenti.html', context)


@login_required
def mentor_studenti_neplozeni_view(request, pk):
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    predmet = Predmeti.objects.get(pk=pk)
    print(predmet.ime)
    users = CustomUser.objects.filter(role=3)
    upisi = Upisi.objects.filter(predmet=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for upis in upisi:
        for user in users:
            if upis.student.id == user.id and upis.status == "nepolozen":
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'mentor_studenti_nepolozeni.html', context)


@login_required
def mentor_studenti_polozeni_view(request, pk):
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    predmet = Predmeti.objects.get(pk=pk)
    print(predmet.ime)
    users = CustomUser.objects.filter(role=3)
    upisi = Upisi.objects.filter(predmet=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for upis in upisi:
        for user in users:
            if upis.student.id == user.id and upis.status == "polozen":
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'mentor_studenti_polozeni.html', context)


@login_required
def mentor_studenti_ispisani_view(request, pk):
    if request.user.role.naziv != "Mentor":
        return HttpResponseRedirect(reverse('home'))
    predmet = Predmeti.objects.get(pk=pk)
    print(predmet.ime)
    users = CustomUser.objects.filter(role=3)
    upisi = Upisi.objects.filter(predmet=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for upis in upisi:
        for user in users:
            if upis.student.id == user.id and upis.status == "ispisan":
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'mentor_studenti_ispisani.html', context)


@login_required
def admin_studenti_zadnja_godina_view(request):
    if request.user.role.naziv != "Admin":
        return HttpResponseRedirect(reverse('home'))
    users = CustomUser.objects.filter(role=3)
    #upisi = Upisi.objects
    upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for upis in upisi:
        temp_predmet = Predmeti.objects.get(pk=upis.predmet_id)
        for user in users:
            if upis.student.id == user.id and ((temp_predmet.sem_redovni == 5 or temp_predmet.sem_redovni == 6) or (temp_predmet.sem_izvanredni == 7 or temp_predmet.sem_izvanredni == 8)):
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'admin_studenti_zadnja_god.html', context)
