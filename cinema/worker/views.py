from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from .forms import MovieModelForm, ShowtimeModelForm, ReservationModelForm, TicketTypeModelForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.forms.formsets import formset_factory

# https://stackoverflow.com/questions/10275164/django-generic-views-using-decorator-login-required
# Jeśli klasy listview, detailview itd rozszerzają tę klasę, to wejście pod adres jest niemożliwe bez logowania
from django.contrib.auth.mixins import LoginRequiredMixin


# aby dostac się do strony wymagane jest zalogowanie, jeśli user nie jest zalogowany,
# to przekierowuje do templatki, która jest podana w settings.py jako LOGIN_URL
@login_required()
def panel(request):
    return render(request, 'worker/panel.html', context={})


# jesli zalogowany user wejdzie na strone logowania, to prekierowuje do panelu,
# w przeciwnym wypadku pozwala się zalogować
def main(request):
    if request.user.is_authenticated:
        return redirect('panel')
    else:
        return render(request, 'main.html', context={})


# typy biletów
class TicketTypeListView(LoginRequiredMixin, ListView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/typy_lista.html'
    paginate_by = 10
    # sortowanie asc po id, czyli wg kolejnosci dodania
    ordering = ['ticket_id']


class TicketTypeCreateView(LoginRequiredMixin, CreateView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/dodaj_typ.html'
    form_class = TicketTypeModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class TicketTypeDetailView(LoginRequiredMixin, DetailView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/szczegoly_typu.html'


class TicketTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/dodaj_typ.html'
    form_class = TicketTypeModelForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.TicketType, ticket_id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class TicketTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TicketType
    template_name = 'worker/typy_biletow/usun_typ.html'
    success_url = reverse_lazy('tickettype-list-worker')


# rezerwacje
class ReservationListView(LoginRequiredMixin, ListView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/rezerwacje_lista.html'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = models.Reservation
    template_name = 'worker/rezerwacje/dodaj_rezerwacje.html'
    form_class = ReservationModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


# seanse
class ShowtimeListView(LoginRequiredMixin, ListView):
    model = models.Showtime
    paginate_by = 10
    ordering = ['-showtime_id']
    template_name = 'worker/seanse/seans_lista.html'


class ShowtimeDetailView(LoginRequiredMixin, DetailView):
    model = models.Showtime
    template_name = 'worker/seanse/szczegoly_seansu.html'

    # w templatce polazuje tylko rezerwacje na konkretny seans + bilety, ktore byly zakupione w ramach rezerwacji
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = models.Reservation.objects.filter(showtime_id=self.get_object())
        context['tickets'] = models.Ticket.objects.filter(showtime_id=self.get_object())
        return context


class ShowtimeCreateView(LoginRequiredMixin, CreateView):
    model = models.Showtime
    template_name = 'worker/seanse/dodaj_seans.html'
    form_class = ShowtimeModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ShowtimeUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Showtime
    template_name = 'worker/seanse/dodaj_seans.html'
    form_class = ShowtimeModelForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.Showtime, showtime_id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ShowtimeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Showtime
    template_name = 'worker/seanse/usun_seans.html'
    success_url = reverse_lazy('showtime-list-worker')


# filmy
class MovieListView(LoginRequiredMixin, ListView):
    model = models.Movie
    template_name = 'worker/filmy/lista_filmow.html'
    paginate_by = 10
    # sortowanie asc po id, czyli wg kolejnosci dodania
    ordering = ['movie_id']


class MovieDetailView(LoginRequiredMixin, DetailView):
    model = models.Movie
    template_name = 'worker/filmy/szczegoly_filmu.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = models.Movie
    template_name = 'worker/filmy/dodaj_film.html'
    form_class = MovieModelForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Movie
    template_name = 'worker/filmy/dodaj_film.html'
    form_class = MovieModelForm

    # dane obecnego obiektu przeniesione do formularza
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(models.Movie, movie_id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Movie
    template_name = 'worker/filmy/usun_film.html'
    success_url = reverse_lazy('movie-list-worker')
