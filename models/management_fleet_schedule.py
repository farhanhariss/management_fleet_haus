from odoo import models, fields, api
from datetime import datetime, timedelta


class ScheduleTask(models.Model):
    _name = "schedules.task"
    _description = "Schedule tasks in hause fleet management"

    # declare field
    task_flow = fields.Selection(
        [
            ("field canvassing", "Field Canvassing"),
            ("field sales", "Field Sales"),
            ("home cleaning", "Home Cleaning"),
            ("delivery", "Delivery"),
        ],
        string="Flow",
        required=True,
    )
    customer_name = fields.Char(strings="Customer Name", required=True)
    customer_address = fields.Char(strings="Customer Address", required=True)
    schedule_name = fields.Char(string="Schedule Name", required=True)
    last_status = fields.Selection([
        ('ongoing', 'Ongoing'),
        ('success', 'Success'),
    ])
    assign_to = fields.Selection(
        [
            ("farhan haris", "Farhan Haris"),
            ("nurul fajri", "Nurul Fajri"),
            ("dian", "Dian"),
            ("rifqi zaidan", "Rifqi Zaidan"),
            ("rizal zeri", "Rizal Zeri"),
        ]
    )
    repeat_every = fields.Selection(
        [
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
            ("by date", "By Date"),
        ],
        string="Repeat Every",
        required=True,
    )
    active_from = fields.Datetime(string="Active From", widget="time")
    active_to = fields.Datetime(string="Active To", widget="time")
    date_selection = fields.Date(string="Date")
    days_selection = fields.Selection(
        [
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
            ("sunday", "Sunday"),
        ],
        string="Days",
    )
    # hour_selection = fields.Datetime(string="Hour", widget="time")
    
    hour_selection = fields.Selection(
        [
            ('00:00', '00:00'),
            ('01:00', '01:00'),
            ('02:00', '02:00'),
            ('03:00', '03:00'),
            ('04:00', '04:00'),
            ('05:00', '05:00'),
            ('06:00', '06:00'),
            ('07:00', '07:00'),
            ('08:00', '08:00'),
            ('09:00', '09:00'),
            ('10:00', '10:00'),
            ('11:00', '11:00'),
            ('12:00', '12:00'),
            ('13:00', '13:00'),
            ('14:00', '14:00'),
            ('15:00', '15:00'),
            ('16:00', '16:00'),
            ('17:00', '17:00'),
            ('18:00', '18:00'),
            ('19:00', '19:00'),
            ('20:00', '20:00'),
            ('21:00', '21:00'),
            ('22:00', '22:00'),
            ('23:00', '23:00'),
        ],
        string="Hour",
        required=True,
    )

    # validation active
    @api.constrains("active_from", "active_to")
    def check_date_and_duedate_valid(self):
        for record in self:
            if record.active_from > record.active_to:
                raise ValueError("Due date must be greater than date")
            
    #TODO : Do the scheduling in cron
    # @api.model
    # def create_tasks_from_schedule(self):
    #     task_obj = self.env['create.task']

    #     for schedule in self:
    #         if schedule.repeat_every == 'day':
    #             # logika untuk jadwal harian
    #             # mengulang tugas setiap hari pada rentang waktu tertentu
    #             current_time = schedule.active_from
    #             while current_time <= schedule.active_to:
    #                 current_hour = datetime.now().strftime('%H:%M')
    #                 if current_hour == schedule.hour_selection:
    #                     task_obj.create({
    #                         'task_flow': schedule.task_flow,
    #                         'customer_name': schedule.customer_name,
    #                         'customer_address': schedule.customer_address,
    #                         'assign_to': schedule.assign_to,
    #                         'start_time': current_time,
    #                         'end_time': current_time + timedelta(hours=1),  # Sesuaikan durasi tugas
    #                     })
    #                 current_time += timedelta(days=1)  # Tambahkan 1 hari ke waktu saat ini

    #         elif schedule.repeat_every == 'week':
    #             # logika untuk jadwal mingguan
    #             # mengulang tugas pada hari-hari tertentu dalam seminggu
    #             current_time = schedule.active_from
    #             while current_time <= schedule.active_to:
    #                 if current_time.strftime('%A').lower() == schedule.days_selection:
    #                     current_hour = datetime.now().strftime('%H:%M')
    #                     if current_hour == schedule.hour_selection:
    #                         task_obj.create({
    #                             'task_flow': schedule.task_flow,
    #                             'customer_name': schedule.customer_name,
    #                             'customer_address': schedule.customer_address,
    #                             'assign_to': schedule.assign_to,
    #                             'start_time': current_time,
    #                             'end_time': current_time + timedelta(hours=1),  # Sesuaikan durasi tugas
    #                         })
    #                 current_time += timedelta(days=1)  # Tambahkan 1 hari ke waktu saat ini

    #         elif schedule.repeat_every == 'month':
    #             # logika untuk jadwal bulanan
    #             # mengulang tugas pada tanggal-tanggal tertentu dalam sebulan
    #             current_time = schedule.active_from
    #             while current_time <= schedule.active_to:
    #                 if current_time.day == schedule.date_selection.day:
    #                     current_hour = datetime.now().strftime('%H:%M')
    #                     if current_hour == schedule.hour_selection:
    #                         task_obj.create({
    #                             'task_flow': schedule.task_flow,
    #                             'customer_name': schedule.customer_name,
    #                             'customer_address': schedule.customer_address,
    #                             'assign_to': schedule.assign_to,
    #                             'start_time': current_time,
    #                             'end_time': current_time + timedelta(hours=1),  # Sesuaikan durasi tugas
    #                         })
    #                 current_time += timedelta(days=1)  # Tambahkan 1 hari ke waktu saat ini

    #         elif schedule.repeat_every == 'by_date':
    #             # untuk jadwal berdasarkan tanggal tertentu
    #             # membuat tugas pada tanggal tertentu
    #             task_obj.create({
    #                 'task_flow': schedule.task_flow,
    #                 'customer_name': schedule.customer_name,
    #                 'customer_address': schedule.customer_address,
    #                 'assign_to': schedule.assign_to,
    #                 'start_time': schedule.date_selection,
    #                 'end_time': schedule.date_selection + timedelta(hours=1),  # Sesuaikan durasi tugas
    #             })
                
