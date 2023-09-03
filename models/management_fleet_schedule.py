from odoo import models, fields, api

class ScheduleTask(models.Model):
    _name="schedules.task"
    _description="Schedule tasks in hause fleet management"
    
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
    schedule_name = fields.Char(string="Schedule Name", required=True)
    assign_to = fields.Selection(
        [
            ("farhan haris","Farhan Haris"),
            ("nurul fajri","Nurul Fajri"),
            ("dian","Dian"),
            ("rifqi zaidan","Rifqi Zaidan"),
            ("rizal zeri","Rizal Zeri"),
        ]
    )
    repeat_every = fields.Selection(
        [
            ("day","Day"),
            ("week","Week"),
            ("month","Month"),
            ("by date","By Date"),
        ],
        string="Repeat Every",
        required=True
    )
    active_from = fields.Datetime(string='Active From', widget='time',required=True)
    active_to = fields.Datetime(string='Active To', widget='time',required=True)
    date_selection = fields.Date(string="Date")
    days_selection = fields.Selection(
        [
            ("monday","Monday"),
            ("tuesday","Tuesday"),
            ("wednesday","Wednesday"),
            ("thursday","Thursday"),
            ("friday","Friday"),
            ("saturday","Saturday"),
            ("sunday","Sunday"),
        ],
        string="Days",
        required=True
    )
    hour_selection = fields.Datetime(string="Hour",widget='time',required=True)
    
    # validation active 
    @api.constrains("active_from", "active_to")
    def check_date_and_duedate_valid(self):
        for record in self:
            if record.active_from > record.active_to:
                raise ValueError("Due date must be greater than date")
