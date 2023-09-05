from odoo import models, fields, api

# from management_fleet_schedule import ScheduleTask


class CreateTask(models.Model):
    _name = "create.task"
    _description = "Create tasks in hause fleet management"

    # declare field
    task_flow = fields.Selection(
        [
            ('field canvassing', 'Field Canvassing'),
            ('field sales', 'Field Sales'),
            ('home cleaning', 'Home Cleaning'),
            ('delivery', 'Delivery'),
        ],
        string="Flow",
        required=True,
    )
    customer_name = fields.Char(strings="Customer Name", required=True)
    customer_address = fields.Char(strings="Customer Address", required=True)
    assign_to = fields.Selection(
        [
            ('farhan haris', 'Farhan Haris'),
            ('nurul fajri', 'Nurul Fajri'),
            ('dian', 'Dian'),
            ('rifqi zaidan', 'Rifqi Zaidan'),
            ('rizal zeri', 'Rizal Zeri'),
        ],
        string="Assign To",
    )

    start_time = fields.Datetime(string="Start Time", widget="time", required=True)
    end_time = fields.Datetime(string="End Time", widget="time", required=True)

    task_status = fields.Selection(
        [
            ('unassigned', 'Unassigned'),
            ('ongoing', 'Ongoing'),
            ('done', 'Done'),
            ('failed', 'Failed'),
        ]
        #  compute="_compute_task_status" # error nanti dia bakal overload servernya
    )
    
    action = fields.Char(string="Action")
    # action = fields.Char(string="Action", compute="_compute_action")

    # # @api.depends('task_status')  # Gunakan field yang sesuai
    # def _compute_action(self):
    #     for record in self:
    #         # Logika untuk menentukan apakah tombol harus ditampilkan atau tidak
    #         if record.task_status == 'ongoing':
    #             record.action = "Do Task"  # Label tombol
    #         else:
    #             record.action = False  # Tidak menampilkan tombol jika tidak memenuhi syarat
    
    # validation date
    @api.constrains("start_time", "end_time")
    def check_date_and_duedate_valid(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValueError("Due date must be greater than date")

    @api.constrains('start_time', 'end_time')
    def _compute_task_status(self):
        for task in self:
            current_datetime = fields.Datetime.now()
            if task.start_time <= current_datetime <= task.end_time:
                task.task_status = 'ongoing'
                task.action = "Do Task"
            elif current_datetime > task.end_time:
                task.task_status = 'done'
            else:
                task.task_status = 'unassigned'
                
    # validation status
    # @api.constrains("assign_to, start_time, end_time")
    # def check_task_status(self):
    #     for record in self:
    #         if not record.assign_to and (
    #             record.start_time < record.end_time
    #             or record.start_time <= fields.Datetime.now() <= record.end_time
    #         ):
    #             record.task_status = 'unassigned'
    #         elif (
    #             record.assign_to
    #             and record.start_time <= fields.Datetime.now() <= record.end_time
    #         ):
    #             record.task_status = 'ongoing'
    #         elif record.assign_to and record.end_time < fields.Datetime.now():
    #             record.task_status = 'done'
    #         else:
    #             record.task_status = 'failed'
    