odoo.define("odoo_fleet_management.create.task", function (require) {
    "use strict";

    // Print out console if javascript file works
    console.log("LOADED");

    var FormController = require("web.FormController");
    var rpc = require("web.rpc");

    console.log("LOADED 1");

    FormController.include({
        _renderButtons: function () {
            this._super.apply(this, arguments);

            var self = this;
            var recordID = self.model.get(self.handle, { raw: true }).res_id;

            // Event listener to handle clicks on the Google Maps iframe
            this.$el.find("iframe").on("load", function () {
                var iframeContents = this.contentDocument || this.contentWindow.document;

                // Event listener to handle clicks on the iframe
                iframeContents.addEventListener("click", function (event) {
                    try {
                        // Get coordinates from the click event
                        var latitude = event.latLng.lat();
                        var longitude = event.latLng.lng();

                        // Fill the lat and lon fields in the form with the selected coordinates
                        self.$el.find("input[name='lat']").val(latitude);
                        self.$el.find("input[name='lon']").val(longitude);

                        // Save data to the Odoo server
                        rpc.query({
                            model: "create.task",
                            method: "write",
                            args: [[recordID], {
                                lat: latitude,
                                lon: longitude,
                            }],
                        });

                        console.log("Clicked on the map at coordinates:", latitude, longitude);

                    } catch (error) {
                        console.error("Error handling click event:", error);
                    }
                });
            });
        },
    });

    return FormController;
});