import krpc
conn = krpc.connect(name='Sub-Orbital flight script')

vessel = conn.space_center.active_vessel

#Prepare the rocket for launch
vessel.auto_pilot.target_pitch_and_heading(90,90) #set pitch and heading
vessel.auto_pilot.engage()
vessel.control.throttle = 1 #set full power
import time
time.sleep(1) #wait 1 sec

#Lift-off!
print('Launch!')
vessel.control.activate_next_stage()

#While loop checks remaining solid fuel until > 0.1 remains
while vessel.resources.amount('SolidFuel') > 0.1:
	time.sleep(1)

#And we activate the next stage
print('Booster separation')
vessel.control.activate_next_stage()

#Reaching Apoapsis
while vessel.flight().mean_altitude < 10000:
	time.sleep(1)
print('Gravity turn')
vessel.auto_pilot.target_pitch_and_heading(60,90)
while vessel.orbit.apoapsis_altitude < 100000:
	time.sleep(1)
print('Launch stage separation')
vessel.control.throttle = 0
time.sleep(1)
vessel.control.activate_next_stage()
vessel.auto_pilot.disengage()

#Returning Safely to Kerbin
while vessel.flight().surface_altitude > 1000:
	time.sleep(1)
vessel.control.activate_next_stage()

#Print the altitude out live until speed reaches 0
while vessel.flight(vessel.orbit.body.reference_frame).vertical_speed < -0.1:
	print('Altitude = %.1f meters' % vessel.flight().surface_altitude)
time.sleep(1)
print('Landed!')

