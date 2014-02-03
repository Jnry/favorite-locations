// Models
var Place, User;
var test_obj;
$(function() {
    // Include attrs: username, password
    User = Backbone.Model.extend({
        defaults: function() {
            return {
                username: "",
                password: ""
            };
        },

        toggle: function() {
        }
    })
    
    // Include attrs: name, address, lat, lng
    // Location is reserved by js
    Place = Backbone.Model.extend({
        urlRoot: "/api/locations",
        defaults: function() {
            return {
                id: null,
                user_id: null,
                name: "a place",
                address: "",
                lat: 0,
                lng: 0
            };
        }
    })

    var PlaceList = Backbone.Collection.extend({
        model: Place,
        url: "/api/locations"
    });

    // Views
    var PlaceListView = Backbone.View.extend({
        tagName: "ul",
        initialize: function() {
            var that = this;
            this.listenTo(this.model, 'add', this.render);
        },
        render: function (e) {
            $(this.el).empty();
            _.each(this.model.models, function(location) {
                $(this.el).append(new PlaceListItemView({model:location}).render().el);
            }, this);
            return this;
        },

        close: function() {
            $(this.el).unbind();
            $(this.el).remove();
        }
    });

    var PlaceListItemView = Backbone.View.extend({
        tagName: "li",
        template: _.template($('#tpl-location-list-item').html()),
        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.close);
        },
        events: {
            "click .view-map": "toggleDetails"
        },
        toggleDetails: function(e) {
            if (app.placeView && app.placeView.model === this.model) {
                app.placeView.close();
                $(e.target).html('View');
            } else {
                app.placeView = new PlaceView({model:this.model});
                $('#location-info').html(app.placeView.render().el);
                $(e.target).html('Hide');
            }
        },
        render: function(e) {
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        close: function() {
            $(this.el).unbind();
            $(this.el).remove();
        }
    });

    var PlaceView = Backbone.View.extend({
        template:_.template($("#tpl-location-details").html()),
        initialize: function() {
            this.listenTo(this.model, 'destroy', this.close);
        },
        render: function(e) {
            $(this.el).html(this.template(this.model.toJSON()));
            map.removeMarker();
            map.placeMarker(null, this.model.get('lat'), this.model.get('lng'));
            return this;
        },
        events: {
            "click .save": "savePlace",
            "click .delete": "deletePlace"
        },
        savePlace: function() {
            var address = $('#location-address').val();
            var that = this;
            $.getJSON('http://maps.googleapis.com/maps/api/geocode/json', {address: address, sensor: false},
                      function(data) {
                          if (data.status != "OK") {
                              alert("Google geocode can not location this address! Please try another.");
                              return false;
                          }
                          if (data.results.length > 1) {
                              that.$('#address-box').empty();
                              that.$('#address-box').append('Please choose a formatted address from the list.');
                              for (var i = 0; i < data.results.length; ++i) {
                                  var address = data.results[i].formatted_address;
                                  that.$("#address-box")
                                      .append(new PlaceResultView().render({address: address}).el);
                              }
                              return false;
                          }
                          var latlng = data.results[0].geometry.location;
                          $("#location-lat").val(latlng.lat);
                          $("#location-lng").val(latlng.lng);
                          that.model.set({
                              name: $("#location-name").val(),
                              address: $("#location-address").val(),
                              lat: $("#location-lat").val(),
                              lng: $("#location-lng").val()
                          });
                          if (that.model.isNew()) {
                              app.locList.create(that.model);
                          } else {
                              that.model.save();
                          }
                          return false;
                      });
        },
        deletePlace: function() {
            this.model.destroy();
        },
        close: function() {
            if (app.placeView === this) {
                app.placeView = undefined;
            }

            $(this.el).unbind();
            $(this.el).empty();
        }
    });

    var PlaceResultView = Backbone.View.extend({
        template:_.template($('#tpl-place-result').html()),
        events: {
            "click .select-this": "selectThis"
        },
        selectThis: function(e) {
            $('#location-address').val($(e.target).html());
        },
        render: function(data) {
            $(this.el).html(this.template(data));
            return this;
        },
    });
    
    var PlaceHeaderView = Backbone.View.extend({
        template: _.template($('#tpl-location-header').html()),
        events: {
            "click #add-location": "addLocation"
        },
        initialize: function() {
            this.render();
        },
        render: function(e) {
            $(this.el).html(this.template());
            return this;
        },
        addLocation: function(e) {
            app.placeView = new PlaceView({model: new Place()});
            $('#location-info').html(app.placeView.render().el);
        },
    });

    var AppRouter = Backbone.Router.extend({
        routes: {
            "locations": "listPlaces",
            "locations/new": "newPlace"
        },

        listPlaces: function() {
            $('#location-header').html(new PlaceHeaderView().render().el);
            this.locList = new PlaceList();
            var that = this;
            this.locList.fetch({
                success: function() {
                    that.locListView = new PlaceListView({model:that.locList});
                    $("#location-list").html(that.locListView.render().el);
                }
            });
        },

        newPlace: function() {
            if (app.placeView) {
                app.placeView.close();
            }
            if (!app.locList) {
                app.locList = new PlaceList();
                app.locList.fetch();
            }
            app.placeView = new PlaceView({model: new Place()});
            $('#location-info').html(app.placeView.render().el);
        }
    });

    var app = new AppRouter();
    Backbone.history.start();
});
