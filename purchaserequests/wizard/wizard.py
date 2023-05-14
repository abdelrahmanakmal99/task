# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Wizard(models.TransientModel):
    _name = 'purchase.wizard'
    _inherit = 'mail.thread'
    _description = 'Purchase Wizard'

    reject1_id = fields.Many2one('purchase.request.reject.reason')
    rejection_reason = fields.Text(string='Rejection Reason')

    def button_reject(self):
        # get purchase.request id
        pr_id = self.env.context.get("active_id", False)
        pr = self.env['purchase.request'].browse(pr_id)
        pr.rejection_reason_id = self.reject1_id.id
