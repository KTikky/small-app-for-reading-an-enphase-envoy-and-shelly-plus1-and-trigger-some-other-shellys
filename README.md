# small-app-for-reading-an-enphase-envoy-and-shelly-plus1-and-trigger-some-other-shellys

# My particular case is a house with 33 solar panels driven by enphase envoy metered device
# Home is with water floor heating, using a tank in tank buffer Austria SISS 700/200 that has a 
# 6kW triphase water heater at it's bottom. Normally it should also receive heat from external
# water solar panels by exchanging the heat through a copper spyral inside the tank. Instead I
# use a secondary small buffer (40l of water) heated by another two triphase resistances 2 and 3kW
# respectively. For me was important to use triphase resistances because our energy supplier meters
# each phase separately - if you produce 6kW triphase and consume 6kW monophase it means in fact you
# imported 4kW  for which you have to pay and exported 4kW on the other two phases, compensated but
# not favourably - the small buffer works with the automation supposed for water solar panels.
# idea was to heat water from self production only, without electricity import.
