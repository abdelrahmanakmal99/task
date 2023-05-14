# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseRequestRejectReason(models.Model):
    _name = 'purchase.request.reject.reason'

    name = fields.Char("Reason")
