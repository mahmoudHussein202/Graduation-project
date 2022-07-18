#print("enter node")
        global v_new
        global v_old
        global s 
        global wait
        v_new=2* phrase.data
# ----------------mapping -----------------------
        #spdmx = 84 
        #spdmn = 25
        #spd_rng = spdmx-spdmn
        #spd_ratio = v_new- spdmn/spd_rng
        #stmx = 90
        #stmn = 14
        #st_rng = stmx-stmn
        #st_ratio = 1- spd_ratio
        #s= stmn + (st_ratio * st_rng)
        #speed_steering.ChangeDutyCycle(s)
#----------------drive action ----------------------
        if v_new > v_old:
            GPIO.output(fwd, True)
            GPIO.output(bkw, False)
            speed.ChangeDutyCycle(99)
            rospy.sleep(wait)
            speed.ChangeDutyCycle(v_new)

        elif v_new < v_old and v_new > 0:
            GPIO.output(fwd, False)
            GPIO.output(bkw, True)
            rospy.sleep(wait)
            GPIO.output(fwd, True)
            GPIO.output(bkw, False)
            speed.ChangeDutyCycle(v_new)

        elif v_new == 0 and v_old > 0:
            GPIO.output(fwd, True)
            GPIO.output(bkw, False)
            speed.ChangeDutyCycle(v_old)
            rospy.sleep(0.5)

        elif v_new == 0 and v_old ==0 :
            GPIO.output(fwd, True)
            GPIO.output(bkw, False)
            speed.ChangeDutyCycle(0)

        v_old = v_new