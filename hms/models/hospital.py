from odoo import models, fields ,api
from datetime import datetime

class HmsDoctors(models.Model):
    _name = 'hms.doctors'
    _description = 'HMS Doctors'
    _rec_name='first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Binary(string='Image')


class HmsPatients(models.Model):
    _name = 'hms.patients'
    _description = 'HMS Patients'

    name = fields.Char(string='Name', required=True)
    department_id = fields.Many2one('hms.department', string='Department')
    doctors_ids = fields.Many2many('hms.doctors', string='Doctors')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')
    pcr = fields.Boolean(string='PCR')
    cr_ratio = fields.Float(string='CR Ratio')
    history = fields.Text(string='History')
    age = fields.Integer(string='Age')
    email = fields.Char(string='Email', unique=True)
    birth_date = fields.Date(string='Birth Date')
    partner_id = fields.Many2one('res.partner', string='Partner')


    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.birth_date:
                delta = today.year - patient.birth_date.year
                if (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day):
                    delta -= 1
                patient.age = delta
            else:
                patient.age = 0


    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr:
            self.cr_ratio = 0.0
            return {'warning': {'title': 'Warning', 'message': 'PCR checked. CR Ratio is mandatory.'}}

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'Warning', 'message': 'PCR checked automatically due to age < 30.'}}

    @api.constrains('department_id')
    def _check_department_opened(self):
        for patient in self:
            if patient.department_id and not patient.department_id.is_opened:
                raise UserError('You cannot choose a closed department.')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.doctor_ids = False
        if self.department_id:
            self.doctor_ids = [(6, 0, self.department_id.doctor_ids.ids)]

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctor_ids = [(6, 0, self.department_id.doctor_ids.ids)]
            self.doctor_ids.readonly = False

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr:
            self.cr_ratio = 0.0
            return {'warning': {'title': 'Warning', 'message': 'PCR checked. CR Ratio is mandatory.'}}

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'Warning', 'message': 'PCR checked automatically due to age < 30.'}}

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctor_ids = [(6, 0, self.department_id.doctor_ids.ids)]
            self.doctor_ids.readonly = False

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr:
            self.cr_ratio = 0.0
            return {'warning': {'title': 'Warning', 'message': 'PCR checked. CR Ratio is mandatory.'}}

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'Warning', 'message': 'PCR checked automatically due to age < 30.'}}

    @api.constrains('email')
    def _check_email(self):
        for patient in self:
            if patient.email:
                if not self._is_valid_email(patient.email):
                    raise ValidationError("Invalid email address")

    @staticmethod
    def _is_valid_email(email):
        return bool(email)

    @api.constrains('department_id')
    def _check_department_opened(self):
        for patient in self:
            if patient.department_id and not patient.department_id.is_opened:
                raise ValidationError('You cannot choose a closed department.')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctors_ids = [(6, 0, self.department_id.doctor_ids.ids)]

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 50:
            self.history = False

    _sql_constraints = [
        ('name_not_null', 'CHECK(name IS NOT NULL)', 'Name cannot be empty.'),
        ('pcr_cr_ratio_check', 'CHECK((NOT pcr) OR (pcr AND cr_ratio IS NOT NULL))',
         'CR Ratio is mandatory if PCR is checked.'),
    ]


# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#
#     website = fields.Char(string='Website')
#     tax_id = fields.Char(string='Tax ID', required=True)
#     # hms_patient_ids = fields.One2many('hms.patient', 'partner_id', string='Patients')
#
#     @api.constrains('email')
#     def _check_unique_email(self):
#         for partner in self:
#             existing_patient = self.env['hms.patient'].search([('email', '=', partner.email)])
#             if existing_patient:
#                 raise ValidationError("This email is already associated with a patient. Please choose a different email.")
#
#     @api.depends('hms_patient_ids')
#     def _compute_has_patient(self):
#         for partner in self:
#             partner.has_patient = bool(partner.hms_patient_ids)
#
#     has_patient = fields.Boolean(compute='_compute_has_patient', string='Has Patient', store=True)
#
#     @api.model
#     def unlink(self):
#         for partner in self:
#             if partner.hms_patient_ids:
#                 raise ValidationError("You cannot delete a customer linked to a patient.")
#         return super(ResPartner, self).unlink()
class HmsPatientHistory(models.Model):
    _name = 'hms.patient.history'
    _description = 'Patient History'

    patient_id = fields.Many2one('hms.patient', string='Patient')
    created_by = fields.Char(string='Created By')
    date = fields.Datetime(string='Date', default=datetime.now())
    description = fields.Text(string='Description')

class HmsDepartment(models.Model):
    _name = 'hms.department'
    _description = 'HMS Department'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    is_opened = fields.Boolean(string='Is Opened')
    patient_ids = fields.One2many('hms.patients', 'department_id', string='Patients')

