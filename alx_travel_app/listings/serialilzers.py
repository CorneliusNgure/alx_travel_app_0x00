"""
Serializers for the listings app.

Includes serializers for:
- Listing
- Booking

These serializers transform model instances to JSON and validate
incoming request data for the API.
"""

from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.

    Fields:
        - listing_id, host, title, description, price_per_night,
          location, created_at.
    """

    host = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "listing_id",
            "host",
            "title",
            "description",
            "price_per_night",
            "location",
            "created_at",
        ]


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.

    Includes nested Listing data for better context.
    Fields:
        - booking_id, listing, user, check_in, check_out,
          status, created_at.
    """

    listing = ListingSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "booking_id",
            "listing",
            "user",
            "check_in",
            "check_out",
            "status",
            "created_at",
        ]

