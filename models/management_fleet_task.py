from odoo import models, fields, api
# from management_fleet_schedule import ScheduleTask

class CreateTask(models.Model):
    _name="create.task"
    _description="Create tasks in hause fleet management"
    
    #declare field
    task_flow = fields.Selection(
        [
            ("field canvassing","Field Canvassing"),
            ("field sales","Field Sales"),
            ("home cleaning","Home Cleaning"),
            ("delivery","Delivery"),
        ],
        string="Flow",
        required=True
    )
    customer_name = fields.Char(strings="Customer Name", required=True)
    customer_address = fields.Char(strings="Customer Address", required=True)
    assign_to = fields.Selection(
        [
            ("farhan haris","Farhan Haris"),
            ("nurul fajri","Nurul Fajri"),
            ("dian","Dian"),
            ("rifqi zaidan","Rifqi Zaidan"),
            ("rizal zeri","Rizal Zeri"),
        ], 
        string="Assign To",
        required=True
    )

    start_time = fields.Datetime(string='Start Time', widget='time',required=True)
    end_time = fields.Datetime(string='End Time', widget='time',required=True)
    
    record_task_count = fields.Integer(compute='_compute_task_count', string='Total Tasks:')
    
    
    # validation date
    @api.constrains("start_time", "end_time")
    def check_date_and_duedate_valid(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValueError("Due date must be greater than date")
            
    # def _compute_task_count(self):
    #     for record in self:
    #         record.task_count = self.env['create.task'].search_count([('task_flow', '=', record.task_flow)])
            
# count records in create task
# record_count= self.env['create.task'].search_count([])