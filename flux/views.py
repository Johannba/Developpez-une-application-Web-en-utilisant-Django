from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField, Q
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

from itertools import chain

from . import forms
from . import models
from .forms import ReviewForm, TicketForm
from .models import Ticket, Review
from follower.models import Follow


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == "POST":
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("flux")
    return render(request, "flux/image_upload.html", context={"form": form})


@login_required
def create_review(request):
    form = forms.ReviewForm()
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("review_form")
    return render(request, "flux/create_review.html", context={"form": form})

@login_required
def post(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)

    tickets = tickets.annotate(contente_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(contente_type=Value("REVIEW", CharField()))

    posts = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)
    return render(request, "flux/posts.html", context={"posts": posts})

@login_required
def flux(request):
    following = Follow.objects.filter(user__exact=request.user)
    tickets = models.Ticket.objects.filter(
        Q(user=request.user) | Q(user__id__in=following.values_list("followed_user"))
    )
    reviews = models.Review.objects.filter(
        Q(user=request.user) | Q(user__id__in=following.values_list("followed_user"))
    )

    tickets = tickets.annotate(contente_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(contente_type=Value("REVIEW", CharField()))

    posts = sorted(chain(tickets, reviews), key=lambda x: x.time_created, reverse=True)
    return render(request, "flux/flux.html", context={"posts": posts})

@login_required
def review_flux(request):
    reviews = models.Review.objects.all()
    return render(request, "flux/review_form.html", context={"reviews": reviews})

@login_required
def response_ticket(request, ticket_id):
    form = forms.ReviewForm()
    ticket = models.Ticket.objects.get(pk=ticket_id)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            ticket.is_reviewed = True
            ticket.save()
            review.ticket = ticket
            review.save()
            return redirect("flux")
    return render(
        request, "flux/create_review.html", context={"form": form, "post": ticket}
    )

@login_required
def ticket_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST, request.FILES)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.is_reviewed = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("flux")
    context = {
        "ticket_form": ticket_form,
        "review_form": review_form,
    }
    return render(request, "flux/ticket_review.html", context=context)


class EditReview(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "flux/edit_review.html"
    success_url = reverse_lazy("posts")

    def dispatch(self, request, *args, **kwargs):
        review = Review.objects.get(id__exact=kwargs['pk'])
        if review.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id__exact=review_id)
    if review.user == request.user:
        ticket = review.ticket
        ticket.is_reviewed = False
        ticket.save()
        review.delete()
        return redirect("posts")
    return HttpResponseForbidden()

@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id__exact=ticket_id)
    if ticket.user == request.user:
        ticket.delete()
        return redirect("posts")
    return HttpResponseForbidden()


class EditTicket(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "flux/edit_ticket.html"
    success_url = reverse_lazy("posts")

    def dispatch(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id__exact=kwargs['pk'])
        if ticket.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
