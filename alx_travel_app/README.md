# alx\_travel\_app\_0x00

A Django-based travel booking application that allows users to create property **listings**, make **bookings**, and leave **reviews**.

---

## Features

* **User Authentication** – Each listing, booking, and review is tied to a registered user.
* **Listings** – Hosts can create and manage property listings.
* **Bookings** – Guests can book available listings with defined check-in and check-out dates.
* **Reviews** – Guests can leave reviews (rating + comments) for listings.
* **Seeder Command** – Pre-populate the database with sample listings for quick testing.

---

## Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/alx_travel_app_0x00.git
   cd alx_travel_app_0x00/alx_travel_app
   ```

2. **Create Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Models Overview

### Listing

* `listing_id` (UUID, primary key)
* `host` (ForeignKey → User)
* `title`, `description`, `price_per_night`, `location`
* `created_at`

### Booking

* `booking_id` (UUID, primary key)
* `listing` (ForeignKey → Listing)
* `user` (ForeignKey → User)
* `check_in`, `check_out`
* `status` (pending, confirmed, canceled)
* `created_at`

### Review

* `review_id` (UUID, primary key)
* `listing` (ForeignKey → Listing)
* `user` (ForeignKey → User)
* `rating` (1–5)
* `comment`
* `created_at`

---

## Seeding Data

The project includes a management command to seed the database with sample listings.

Run:

```bash
python manage.py seed
```

This will create a demo host and populate the database with a few property listings.

---

## Tech Stack

* **Backend**: Django (Python)
* **Database**: MySQL (default, configurable in `settings.py`)
* **API**: Django REST Framework (DRF)

---

## Next Steps / Improvements

* Add API endpoints for Listings, Bookings, and Reviews.
* Implement authentication (JWT / DRF auth).
* Add availability validation for bookings.
* Build frontend integration (React / Vue).

---

## Author

Developed as part of ALX Backend Python projects

