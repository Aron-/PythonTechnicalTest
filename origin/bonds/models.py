from django.db import models


class Bond(models.Model):
    objects = models.Manager()
    # Django will add a Primary Key 'id' column for us.

    # The ISIN code is a 12-character alphanumeric code that serves for uniform identification of a security through
    # normalization of the assigned National Number, where one exists, at trading and settlement.
    isin = models.CharField(max_length=12, blank=False)

    # Store numbers up to one trillion with a resolution of 10 decimal places:
    size = models.DecimalField(max_digits=22, decimal_places=10)

    # ISO 4217 assigns a three-digit code number to each currency.
    currency = models.CharField(max_length=3, blank=False)

    # Do not fill out date automatically, must be set.
    maturity = models.DateField(auto_now=False, auto_now_add=False)

    # The Legal Entity Identifier (LEI) is a 20-character, alpha-numeric code based on the ISO 17442 standard
    # developed by the International Organization for Standardization (ISO).
    lei = models.CharField(max_length=20, blank=False)

    # Should be sufficient for company name.
    legal_name = models.CharField(max_length=255, blank=False, default='')
