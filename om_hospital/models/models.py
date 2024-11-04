from pickle import FALSE

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char(string="Name",required=True, tracking=True)
    date_of_birth = fields.Date(string="DOB", tracking=True)
    age = fields.Integer(string="Age", compute='_compute_age')
    gender = fields.Selection([('male','Male'),('female','Female')],string="Gender", tracking=True)
    tag_ids = fields.Many2many('patient.tag','patient_tag_rel'
                               'patient_id','tag_id',string="Tags")
    is_minor = fields.Boolean(string="Minor")
    guardian = fields.Char(string="Guardian")
    weight = fields.Float(string="Weight")



    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0



    def action_test(self):
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Click Successful',
                    'type': 'rainbow_man',
                }
            }


    # @api.ondelete(at_uninstall = False)
    # def _check_patient_appointments(self):
    #     for rec in self:
    #         domain = [('patient_id','=', rec.id)]
    #         appointments = self.env['hospital.appointment'].search(domain)
    #         if appointments:
    #             raise ValidationError(_("You Can Not Delete The Patient Now ,\n Appointment Existing"))
    #     return super().unlink()

    def unlink(self):
        # You can perform anything here
        for rec in self:
            domain = [('patient_id','=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
               # raise ValidationError(_("You Can Not Delete The Patient Now ,\n Appointment Existing :%s"% rec.name))
                raise UserError(_("You Can Not Delete The Patient Now ,\n Appointment Existing :%s"% rec.name))
        return super().unlink()