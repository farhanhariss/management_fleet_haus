from odoo import models, fields, api

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
    assign_to = fields.Selection(
        [
            ("farhan haris","Farhan Haris"),
            ("nurul fajri","Nurul Fajri"),
            ("dian","Dian"),
            ("rifqi zaidan","Rifqi Zaidan"),
            ("rizal zeri","Rizal Zeri"),
        ]
    )

    start_time = fields.Datetime(string='Start Time', widget='time',required=True)
    end_time = fields.Datetime(string='End Time', widget='time',required=True)
    
    
    # validation date
    @api.constrains("start_time", "end_time")
    def check_date_and_duedate_valid(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValueError("Due date must be greater than date")
    
    

    
    
    
    
    