from odoo import api, fields, models
from odoo.api import ondelete
from odoo.tools.populate import compute


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_names_search = ['reference','patient_id']
    _rec_name = 'patient_id'

    reference = fields.Char(string="Reference", default='New')
    patient_id = fields.Many2one('hospital.patient', string="Patient",
                                 required = False, ondelete='restrict')
    date_appointment = fields.Date(string="Time")
    note = fields.Text(string="Note")
    state = fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('ongoing','Ongoing'),
        ('done','Done'),
        ('cancel','Cancelled'),
                              ], default = 'draft', tracking = True)
    appointment_line_ids = fields.One2many('hospital.appointment.line',
                                           'appointment_id', string="Lines")
    total_qty = fields.Float(compute = '_compute_total_qty',
                             string="Total Quantity", store=True)
    date_of_birth = fields.Date(related='patient_id.date_of_birth',store = True, groups="om_hospital.group_hospital_doctors")



    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference']=='New':
                vals['reference']=self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    @api.depends('appointment_line_ids','appointment_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:   #rec.total_qty = sum(rec.appointment_line_ids.mapped('qty'))
            total_qty = 0
            for line in rec.appointment_line_ids:
                total_qty = total_qty + line.qty # total_qty+=line.qty
            rec.total_qty = total_qty

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}]{rec.patient_id.name}"

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    product_id = fields.Many2one('product.product', string="Product", required = True)
    qty = fields.Float(string="Quantity")