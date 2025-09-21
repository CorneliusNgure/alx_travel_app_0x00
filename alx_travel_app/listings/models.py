"""
Models for listings: Listing, Booking and Review.

Each model uses a UUID primary key and enforces the constraints
specified in the instructions:
- Foreign keys to the project user model (settings.AUTH_USER_MODEL).
- Non-null constraints on essential fields.
- Booking status choices and basic validation.
- Review rating validation (1..5).
"""

import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Listing(models.Model):
    """
    A property listing hosted by a user.

    Fields:
        listing_id (UUIDField): Primary key, unique and indexed.
        host (ForeignKey): User hosting the listing.
        title (CharField): Short title, required.
        description (TextField): Full description, required.
        price_per_night (DecimalField): Price per night, required.
        location (CharField): Location text, required.
        created_at (DateTimeField): When the listing was created.
    """

    listing_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    location = models.CharField(max_length=255, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Human readable representation of the listing.
        """
        return f"{self.title} ({self.listing_id})"

    class Meta:
        """
        Database options for Listing.
        """
        indexes = [
            models.Index(fields=["host"]),
        ]


class Booking(models.Model):
    """
    A booking made by a user for a listing.

    Fields:
        booking_id (UUIDField): Primary key, unique and indexed.
        listing (ForeignKey): The listing that is booked.
        user (ForeignKey): The user who made the booking.
        check_in (DateField): Booking start date.
        check_out (DateField): Booking end date.
        status (CharField): One of pending, confirmed, canceled.
        created_at (DateTimeField): When the booking was created.

    Constraints:
        - Foreign keys on listing and user.
        - Status limited to defined choices.
        - check_in must be before check_out.
    """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    ]

    booking_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bookings",
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    check_in = models.DateField()
    check_out = models.DateField()

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Validate booking dates.

        Ensures check_in is strictly before check_out.
        """
        if self.check_in and self.check_out:
            if self.check_in >= self.check_out:
                raise ValidationError(
                    {"check_out": "check_out must be after check_in."}
                )

    def save(self, *args, **kwargs):
        """
        Run full clean before saving to enforce validations.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Human readable representation of the booking.
        """
        return f"Booking {self.booking_id} for {self.listing}"


class Review(models.Model):
    """
    A user review for a listing.

    Fields:
        review_id (UUIDField): Primary key, unique.
        listing (ForeignKey): The listing being reviewed.
        user (ForeignKey): The user who left the review.
        rating (IntegerField): Value between 1 and 5 (inclusive).
        comment (TextField): Optional textual comment.
        created_at (DateTimeField): When the review was created.

    Constraints:
        - Foreign keys on listing and user.
        - Rating must be an integer between 1 and 5.
    """

    review_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="reviews"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Validate rating value before saving.

        Rating must be between 1 and 5 inclusive.
        """
        if not 1 <= int(self.rating) <= 5:
            raise ValidationError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Human readable representation of the review.
        """
        return f"Review {self.review_id} - {self.rating} stars"

    class Meta:
        """
        Database options for Review.
        """
        indexes = [
            models.Index(fields=["listing"]),
        ]
