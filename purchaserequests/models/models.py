from odoo import api, fields, models
from odoo.exceptions import UserError

class Purchaserequest(models.Model):
    _name = 'purchase.request'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Request Name", required=True)
    user_id = fields.Many2one('res.users', required=1, default=lambda self: self.env.user)

    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date")
    # rejection_reason = fields.Text(string='Rejection Reason',)
    rejection_reason_id = fields.Many2one('purchase.request.reject.reason', string='rejection reason', tracking=True)

    total_price = fields.Float(string="Total Price ", compute='compute_sum_total')
    partner_id = fields.Many2one(comodel_name='res.partner', string="vender ", required=False)

    lines_ids = fields.One2many("purchase.request.line", "purchase_request_id")
    approved = fields.Boolean(string="approved",default=False  )
    state = fields.Selection([('draft', 'Draft'),
                              ('to be approved', 'to be approved'),
                              ('approved', 'approved'),
                              ('reject', 'reject'),
                              ('cancel', 'cancel'),
                              ('Submit for Approval', 'Submit for Approval'),

                              ],
                             )

    purchase_manager_ids = fields.Many2many(
        comodel_name='res.users',
        relation='purchase_request_purchase_manager_rel',
        column1='purchase_request_id',
        column2='user_id',
        string='Purchase Managers'
    )

    def button_submit_approval(self):
        if self.state:
            self.state = "to be approved"

    def button_cancel(self):
        if self.state:
            self.state = "to be approved"
    @api.constrains('value')
    def button_approve(self):
        if self.state != 'pending':
            raise UserError(("Purchase request must be in pending state to approve."))
        self.write({'state': 'approved'})
        template = self.env.ref('purchase_request.email_template_purchase_request_approved')
        email_to = self.env.ref('purchase.group_purchase_manager').users.filtered(lambda u: u.email)
        if email_to:
            template.with_context(purchase_request_name=self.name).send_mail(self.id, email_values={
                'email_to': email_to.mapped('email')})
        return True




    def button_reject(self):
        button = self.env.ref('purchaserequests.wizard_action').read()[0]
        return button
        print('12321323213123')

    # def action_confirm(self):
    #     purchaserequests_rejection_reason = self.rejection_reason
    #     return

    # @api.depends('lines_ids', 'lines_ids.total')
    def compute_sum_total(self):
        for record in self:
            total_p = 0.0
            for line in record.lines_ids:
                total_p += line.total
            record.total_price = total_p
            # record.update({'total_price': total_p})

            # self.env['purchase.request'].search_count([('lines_id', '=', self.id)])


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    product_id = fields.Many2one('product.product', required=1)
    description = fields.Char(string="Description")
    quantity = fields.Float(string='quantity', default=1)
    cost_price = fields.Float(string='cost price', readonly=1, related="product_id.standard_price")
    total = fields.Float(string='Total', readonly=1, compute="_get_price_total")
    purchase_request_id = fields.Many2one("purchase.request")

    @api.depends('cost_price', 'quantity')
    def _get_price_total(self):
        for record in self:
            record.total = record.quantity * record.cost_price
