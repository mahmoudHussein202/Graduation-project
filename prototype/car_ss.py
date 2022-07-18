def callback_fn(message):
        global speed
        global new_speed
        global old_speed
        global direction_flag
        speed = message.data
        if speed == 40 :
                new_speed = 100
                left_wheel.start(new_speed)
                GPIO.output(20, True)
                GPIO.output(16, False)
                old_speed = 100
        elif speed == 25 :
                new_speed = 70 
                left_wheel.start(new_speed)
                GPIO.output(20, True)
                GPIO.output(16, False)
                old_speed = 70
        elif speed == 0 :
