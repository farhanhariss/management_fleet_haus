// odoo.define("odoo_fleet_management.create.task", function (require) {
//     "use strict";

//     // Print out console if javascript file works
//     console.log("LOADED");

//     var FormController = require("web.FormController");
//     var rpc = require("web.rpc");

//     console.log("LOADED 1");

//     FormController.include({
//         _renderButtons: function () {
//             this._super.apply(this, arguments);

//             var self = this;
//             var recordID = self.model.get(self.handle, { raw: true }).res_id;

//             // Event listener to handle clicks on the Google Maps iframe
//             this.$el.find("iframe").on("load", function () {
//                 var iframeContents = this.contentDocument || this.contentWindow.document;

//                 // Event listener to handle clicks on the iframe
//                 iframeContents.addEventListener("click", function (event) {
//                     try {
//                         // Get coordinates from the click event
//                         var latitude = event.latLng.lat();
//                         var longitude = event.latLng.lng();

//                         // Fill the lat and lon fields in the form with the selected coordinates
//                         self.$el.find("input[name='lat']").val(latitude);
//                         self.$el.find("input[name='lon']").val(longitude);

//                         // Save data to the Odoo server
//                         rpc.query({
//                             model: "create.task",
//                             method: "write",
//                             args: [[recordID], {
//                                 lat: latitude,
//                                 lon: longitude,
//                             }],
//                         });

//                         console.log("Clicked on the map at coordinates:", latitude, longitude);

//                     } catch (error) {
//                         console.error("Error handling click event:", error);
//                     }
//                 });
//             });
//         },
//     });

//     return FormController;
// });


odoo.define('odoo_fleet_management.create_task', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');

    var _t = core._t;

    FormController.include({
        events: _.extend({}, FormController.prototype.events, {
            'click .oe_button_open_google_maps': '_onOpenGoogleMaps',
            'click .oe_button_update_coordinates': '_onUpdateCoordinates'
        }),

        // ...

        _onOpenGoogleMaps: function () {
            var self = this;
            var recordData = this.model.get(this.handle).data;

            // Pastikan latitude dan longitude tersedia
            if (recordData.lat && recordData.lon) {
                var latitude = recordData.lat;
                var longitude = recordData.lon;

                // Konstruksi URL Google Maps berdasarkan koordinat
                var url = 'https://www.google.com/maps?q=' + latitude + ',' + longitude;

                // Buka jendela pop-up dengan Google Maps
                Dialog.confirm(this, _t("Open Google Maps?"), {
                    confirm_callback: function () {
                        var popup = window.open(url, 'Google Maps', 'width=800,height=600');
                        if (!popup || popup.closed || typeof popup.closed == 'undefined') {
                            alert('Silakan nonaktifkan pemblokir popup Anda dan coba lagi.');
                        }
                    },
                });
            } else {
                alert('Latitude dan Longitude tidak tersedia.');
            }
        },

        // _onUpdateCoordinates: function () {
        //     var self = this;

        //     var newLatitude = recordData.lat; // Gantilah dengan nilai latitude yang benar
        //     var newLongitude = recordData.lon; // Gantilah dengan nilai longitude yang benar

        //     // Panggil RPC untuk memperbarui nilai lat dan lon
        //     this.model.call('write', [[self.handle], {
        //         lat: newLatitude,
        //         lon: newLongitude,
        //     }]).then(function (result) {
        //         if (result) {
        //             // Sukses, lat dan lon diperbarui di server.
        //             // Refresh tampilan jika perlu.
        //             self.reload();
        //         } else {
        //             // Gagal, tampilkan pesan kesalahan jika diperlukan.
        //             alert('Gagal memperbarui koordinat.');
        //         }
        //     });
        // },
    });

    return FormController;
});