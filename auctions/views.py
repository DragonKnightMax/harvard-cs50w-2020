from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import re

from .models import User, Listing, Watchlist, Comment, Category

# ================================FORMS===================================
class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    starting_bid = forms.DecimalField(max_digits=None, decimal_places=2, label="Starting Bid")
    image_url = forms.URLField(max_length=200, label="Image URL (Optional)", required=False, empty_value=None)
    category = forms.ModelChoiceField(queryset=Category.objects.order_by("category"))

class CommentForm(forms.Form):
    comment = forms.CharField(label="", widget=forms.Textarea)

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=None, label="Bid")

# ===============================LISTING===================================
def index(request):
    listings = Listing.objects.filter(status="Active")
    return render(request, "auctions/index.html", {
        "listings": listings
    })


# To view all details about the listing
def details(request, listing_id):
    # Query the Listing models using listing_id
    listing = Listing.objects.get(id=listing_id)

    # sort comment by datetime (-[column] for reverse)
    comments = Comment.objects.filter(listing=listing).order_by("-date_time")

    if request.user.is_authenticated:
        # check if the user is the owner of the listing
        # decide whether user can see 'Close Auctions' button or not
        owner = listing.owner
        user = User.objects.get(id=request.user.id)
        if owner == user:
            owner = True

        # check if the listing already exist in user watchlist
        # decide which button is displayed(Add to Watchlist/Remove from Watchlist)
        already_in_watchlist = True
        try:
            watchlist_item = Watchlist.objects.get(listing=listing)
        except Watchlist.DoesNotExist:
            already_in_watchlist = False
        return render(request, "auctions/details.html", {
            "listing": listing,
            "BidForm": BidForm(),
            "CommentForm": CommentForm(),
            "comments": comments,
            "already_in_watchlist": already_in_watchlist,
            "owner": owner
        })
    # for not authenticated user (not login)
    return render(request, "auctions/details.html", {
            "listing": listing,
            "comments": comments
        })


@login_required
def create_listing(request):
    # handle post request
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        
        if form.is_valid():
            # create a Listing objects with the submitted form data
            listing = Listing(
                owner= User.objects.get(id=request.user.id),
                title= form.cleaned_data["title"],
                description= form.cleaned_data["description"],
                price= form.cleaned_data["starting_bid"],
                image_url= form.cleaned_data["image_url"],
                category= form.cleaned_data["category"]
            )

            # insert the Listing object into database models
            listing.save()
            message = "Listing created successfully!"
            return render(request, "auctions/details.html", {
                "listing": listing,
                "BidForm": BidForm(),
                "CommentForm": CommentForm(),
                "comments": Comment.objects.filter(listing=listing).order_by("-date_time"),
                "already_in_watchlist": False,
                "owner": True,
                "winner": listing.winner,
                "message": message
            })
        
        # if form is invalid, return the form submitted back to user
        else:
            return render(request, "auctions/create.html", {
                "CreateListingForm": CreateListingForm(form)
            })

    return render(request, "auctions/create.html", {
        "CreateListingForm": CreateListingForm()
    })


@login_required
def bid_item(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        
        if form.is_valid():
            new_price = form.cleaned_data["bid"]
            user = User.objects.get(id=request.user.id)
            listing = Listing.objects.get(id=listing_id)
            last_price = listing.price

            owner = listing.owner
            if owner == user:
                owner = True

            already_in_watchlist = True
            try:
                watchlist_item = Watchlist.objects.get(listing=listing)
            except Watchlist.DoesNotExist:
                already_in_watchlist = False

            # only update when bid proce is greater than last price
            if new_price >= last_price:
                listing.price = new_price
                listing.winner = user
                listing.save()
                message = "Bade Successfully!"
            else:
                # bid is not successful as bid is less than last price
                message = "Failed to bid! Make sure your bid is at least as large as current bid!"
            
            return render(request, "auctions/details.html", {
                "listing": listing,
                "BidForm": BidForm(),
                "CommentForm": CommentForm(),
                "comments": Comment.objects.filter(listing=listing).order_by("-date_time"),
                "already_in_watchlist": already_in_watchlist,
                "owner": owner,
                "message": message
            })
    return HttpResponseRedirect(reverse(index))
    

@login_required
def close_auction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.status = "Closed"
        listing.save()
    
        return render(request, "auctions/message.html", {
            "winner_message": f"Auction closed successfully! The winner is {listing.winner}!"
        })
    return HttpResponseRedirect(reverse("index"))


@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():       
            user_comment = Comment(
                listing=Listing.objects.get(id=listing_id),
                user=User.objects.get(id=request.user.id),
                comment=comment_form.cleaned_data["comment"]
                )
            user_comment.save()
            return HttpResponseRedirect(reverse("details", args=[listing_id]))  
        else:
            return render(request, "auctions/details.html", {
                "CommentForm": CommentForm(comment_form)
            })
    return HttpResponseRedirect(reverse("details", args=[listing_id]))

# ==============================WATCHLIST==============================
@login_required
def watchlist(request):
    user = User.objects.get(id=request.user.id)
    listing_items = Watchlist.objects.filter(user=user)
    
    watchlist = []
    for item in listing_items:
        #index = re.findall(r'\d+', str(listing_id.listing))
        #watchlist.append(Listing.objects.get(id=int(index[0])))
        watchlist.append(Listing.objects.get(id=item.listing.id))
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


@login_required
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        ItemToAdd = Watchlist(user=User.objects.get(id=request.user.id), listing=listing)
        ItemToAdd.save()
        message = "Listing has been added to your watchlist!"

        owner = listing.owner
        user = User.objects.get(id=request.user.id)
        if owner == user:
            owner = True
        return render(request, "auctions/details.html", {
            "listing": listing,
            "BidForm": BidForm(),
            "CommentForm": CommentForm(),
            "comments": Comment.objects.filter(listing=listing).order_by("-date_time"),
            "already_in_watchlist": True,
            "owner": owner,
            "winner": listing.winner,
            "message": message
        })
    return HttpResponseRedirect(reverse("index"))


@login_required
def remove_watchlist(request, listing_id):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        watchlist_items = Watchlist.objects.filter(user=user)
        listing = Listing.objects.get(id=listing_id)

        for item in watchlist_items:
            if item.listing == listing:
                item.delete()
                message = "Listing has been removed from your watchlist!"
                
                owner = listing.owner
                if owner == user:
                    owner = True

                return render(request, "auctions/details.html", {
                    "listing": listing,
                    "BidForm": BidForm(),
                    "CommentForm": CommentForm(),
                    "comments": Comment.objects.filter(listing=listing).order_by("-date_time"),
                    "already_in_watchlist": False,
                    "owner": owner,
                    "message": message
                })

    return HttpResponseRedirect(reverse("index"))

# ================================CATEGORIES======================================
def categories(request):
    # sort category alphabetically
    categories = Category.objects.order_by("category")
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def filterByCategory(request, category):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category, status="Active"),
        "filter_by_category": category
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")