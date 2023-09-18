from odoo import models, fields, api
from odoo.exceptions import ValidationError

# from management_fleet_schedule import ScheduleTask


class CreateTask(models.Model):
    _name = "create.task"
    _description = "Create tasks in hause fleet management"

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
    
    assign_to = fields.Selection(
        [
            ("farhan haris", "Farhan Haris"),
            ("nurul fajri", "Nurul Fajri"),
            ("dian", "Dian"),
            ("rifqi zaidan", "Rifqi Zaidan"),
            ("rizal zeri", "Rizal Zeri"),
        ],
        string="Assign To",
    )

    start_time = fields.Datetime(string="Start Time", widget="time", required=True)
    end_time = fields.Datetime(string="End Time", widget="time", required=True)

    task_status = fields.Selection(
        [
            ("unassigned", "Unassigned"),
            ("ongoing", "Ongoing"),
            ("done", "Done"),
            ("failed", "Failed"),
        ]
    )
    
    action = fields.Char(string="Action")
    
    # maps_link = fields.Char(string="Maps Link", compute="_compute_maps_link")
    lat = fields.Float(string="Latitude", digits=(16, 5))
    lon = fields.Float(string="Longitude", digits=(16, 5))
    # lat2 = fields.Float(string="Longitude", digits=(16, 5))
    # lon2 = fields.Float(string="Longitude", digits=(16, 5))
    
    sample_google_map= fields.Char(string="Sample Google Map", widget="google_map")
    
    # @api.depends('lat', 'lon')
    # def _compute_maps_link(self):
    #     for record in self:
    #         # Check if both lat and lon fields have values
    #         if record.lat and record.lon:
    #             api_key = 'AIzaSyBbR235E758eQZ09yh85k-KIFr4s0P6zyM'
    #             latitude = record.lat
    #             longitude = record.lon
    #             # Construct the Google Maps link based on lat and lon
    #             url = f'https://www.google.com/maps/embed/v1/place?key={api_key}&q={latitude},{longitude}'
    #             record.maps_link = url
    #         else:
    #             record.maps_link = ''
    
    def get_google_maps_url(self, lat, lon):
        api_key = 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
        return f'https://www.google.com/maps/embed/v1/place?key={api_key}&q={lat},{lon}'
    
    # Fungsi aksi untuk membuka pop-up Google Maps
    def action_open_google_maps(self):
        # Pastikan latitude dan longitude tersedia
        if self.lat1 and self.lon1:
            return {
                'type': 'ir.actions.client',
                'tag': 'open_google_maps_popup',
                'params': {
                    'lat': self.lat1,
                    'lon': self.lon1,
                },
            }
        else:
            # Latitude dan longitude tidak tersedia, berikan pesan kesalahan
            raise ValidationError("Latitude and Longitude are not available.")
    
     # Fungsi aksi untuk memperbarui koordinat
    # def action_update_coordinates(self):
    #     for record in self:
    #         # Di sini Anda dapat mengambil latitude dan longitude yang baru dari elemen peta (misalnya, menggunakan JavaScript Google Maps API).
    #         # Gantilah kode berikut dengan cara yang sesuai untuk mendapatkan koordinat yang baru.
    #         new_latitude = 123.456  # Gantilah dengan nilai latitude yang benar
    #         new_longitude = 789.012  # Gantilah dengan nilai longitude yang benar

    #         # Setelah mendapatkan koordinat yang baru, perbarui nilai lat dan lon dalam rekaman
    #         record.write({
    #             'lat': new_latitude,
    #             'lon': new_longitude,
    #         })

    #         # Tambahan: Jika Anda ingin melakukan tindakan lain setelah memperbarui koordinat, Anda dapat melakukannya di sini.

    #     # Setelah selesai, Anda dapat memberikan pesan sukses atau mengambil tindakan lain yang sesuai.
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': 'Coordinates Updated',
    #             'message': 'Coordinates have been updated successfully.',
    #             'type': 'success',
    #         },
    #     }
    
    # validation date
    @api.constrains("start_time", "end_time")
    def check_date_and_duedate_valid(self):
        for record in self:
            if record.start_time > record.end_time:
                raise ValueError("Due date must be greater than date")

    @api.model
    def compute_task_status(self):
        # Inisialisasi waktu saat ini
        current_time = fields.Datetime.now()

        # Update status tugas dari "Unassigned" ke "Ongoing"
        tasks_to_update_ongoing = self.search(
            [("start_time", "<=", current_time), ("task_status", "=", "unassigned")]
        )
        tasks_to_update_ongoing.write({"task_status": "ongoing"})

        # Update status tugas dari "Ongoing" ke "Done"
        tasks_to_update_done = self.search(
            [("end_time", "<=", current_time), ("task_status", "=", "ongoing")]
        )
        tasks_to_update_done.write({"task_status": "done"})


    # @api.model
    # def open_google_maps(self):
    # # Ensure that this method takes 'self' as its first parameter
    #     self.ensure_one()

    #     return {
    #         "type": "ir.actions.act_url",
    #         "url": "https://maps.google.com/maps?q=-7.057785,110.429039&amp;z=15&amp;output=embed&amp;key=AIzaSyBbR235E758eQZ09yh85k-KIFr4s0P6zyM",
    #         "target": "new",
    #     }

    @api.constrains("assign_to", "task_status", "start_time", "end_time")
    def _check_task_status(self):
        current_time = fields.Datetime.now()
        for task in self:
            if (
                not task.assign_to
                and not task.task_status
                and current_time < task.start_time
            ):
                task.task_status = "unassigned"
            elif (
                not task.task_status
                and task.start_time <= current_time <= task.end_time
                and (task.assign_to or not task.assign_to)
            ):
                task.task_status = "ongoing"
            elif (
                task.assign_to and not task.task_status and current_time > task.end_time
            ):
                raise ValidationError(
                    "Cannot create a record with assignee and no status beyond end time."
                )

        if (
            task.assign_to
            and task.task_status
            and task.start_time <= current_time <= task.end_time
        ):
            if task.task_status != "ongoing":
                task.task_status = "ongoing"
        elif task.assign_to and task.task_status and current_time > task.end_time:
            raise ValidationError(
                "Cannot create a record with assignee and status beyond end time."
            )

    @api.model
    def show_success_prompt(self):
        # Display a success prompt
        for record in self:
            record.env.user.notify_success("This is a success message.")
