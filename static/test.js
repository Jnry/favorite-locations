module("About location models");
test("Can be created with default values for the attributes of places", function() {
    expect(2);
    var place = new Place();
    equal(place.get("name"), "a place");
    equal(place.get("address"), "");
});
