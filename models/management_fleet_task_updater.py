from odoo import models, fields, api

class TaskStatusUpdater(models.Model):
    _name = "task.status.updater"
    _description = "Task status updater in hause fleet management"

    def update_task_status(self):
        for task in self:
            current_datetime = fields.Datetime.now()
            if task.start_time <= current_datetime <= task.end_time:
                task.task_status = 'ongoing'
            elif current_datetime > task.end_time:
                task.task_status = 'done'
            else:
                task.task_status = 'unassigned'
                
    def check_task_status(self):
        for record in self:
            if not record.assign_to and (
                record.start_time < record.end_time
                or record.start_time <= fields.Datetime.now() <= record.end_time
            ):
                record.task_status = 'unassigned'
            elif (
                record.assign_to
                and record.start_time <= fields.Datetime.now() <= record.end_time
            ):
                record.task_status = 'ongoing'
            elif record.assign_to and record.end_time < fields.Datetime.now():
                record.task_status = 'done'
            else:
                record.task_status = 'failed'
