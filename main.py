import cv2
import sys
import numpy as np
 
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

##----------------- Setup some Dependacy and Libraries ------------------##

def selectTracker(tracker_type):
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
    tracker_type = tracker_types[tracker_type]
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
    return tracker



def main():
    print("Preparing Application")
    tracker = selectTracker(1)

    video = cv2.VideoCapture('video.mp4')#use Video.mp4
    #video = cv2.VideoCapture(0) # for using CAM
    
    if not video.isOpened():
        print("error opening video file")
        sys.exit()
    ok, frame = video.read()
    frame = cv2.resize(frame, (720, 480))
    if not ok:
        print('error reading video file')
        sys.exit()

       
    bbox = (287, 23, 86, 320)
    bbox = cv2.selectROI(frame, False)
    ok = tracker.init(frame, bbox)
    roi_selector_active = False
    lock_status="KILITLENME DURUM: PASIF"
    lock_status_c = (0, 0, 255)
    while True:
        ret, frame = video.read()
        frame = cv2.resize(frame, (720, 480))
        if not ret:
            break
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
       
        if roi_selector_active:

            bbox = cv2.selectROI(frame, True)
            ok = tracker.init(frame, bbox)

            roi_selector_active = False
        ok, bbox = tracker.update(frame)

        
        if ok:
            lock_status="Synerflight"
            lock_status_c = (0, 255, 0)
            cx = int(bbox[0] + bbox[2] / 2)  # Bonding Box x Coordinate
            cy = int(bbox[1] + bbox[3] / 2)  # Bonding Box y Coordinate
            half_size = 40 // 2  # Kare boyutunun yarı çapı
            gap = 8  # Kare ile çizgiler arasındaki boşluk
            
##----------------- DRaw some target Lines ------------------##
            
            dark_green = (0, 180, 0)
            line_thickness = 2
            cv2.line(frame, (cx - half_size, cy - half_size), (cx - half_size + gap, cy - half_size), dark_green, line_thickness)
            cv2.line(frame, (cx + half_size - gap, cy - half_size), (cx + half_size, cy - half_size), dark_green, line_thickness)
            cv2.line(frame, (cx - half_size, cy + half_size), (cx - half_size + gap, cy + half_size), dark_green, line_thickness)
            cv2.line(frame, (cx + half_size - gap, cy + half_size), (cx + half_size, cy + half_size), dark_green, line_thickness)
            cv2.line(frame, (cx - half_size, cy - half_size), (cx - half_size, cy - half_size + gap), dark_green, line_thickness)
            cv2.line(frame, (cx + half_size, cy - half_size), (cx + half_size, cy - half_size + gap), dark_green, line_thickness)
            cv2.line(frame , (cx - half_size , cy + half_size ), (cx - half_size , cy + half_size - gap ), dark_green , line_thickness )
            cv2.line(frame , (cx + half_size , cy + half_size ), (cx + half_size , cy + half_size - gap ), dark_green , line_thickness )
            cv2.line(frame , (cx , cy - half_size - gap ), (cx , 0 ), dark_green , line_thickness )
            cv2.line(frame , (cx , cy + half_size + gap ), (cx , frame.shape[0] ), dark_green , line_thickness )
            cv2.line(frame , (cx - half_size - gap , cy ), (0 , cy ), dark_green , line_thickness )
            cv2.line(frame , (cx + half_size + gap , cy ), (frame.shape[1] , cy ), dark_green , line_thickness )
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 2
            text = f'x: {cx}, y: {cy}'
            text_position = (10, 20)
            cv2.putText(frame, text, text_position, font, font_scale, dark_green, font_thickness)


        else:
            lock_status="KILITLENME DURUM: PASIF"
        height, width = frame.shape[:2]
        corner_length = 40  # Length of corner lines
        offset = 130  # Inward offset of corner lines
        cv2.line(frame, (offset, offset), (offset + corner_length, offset), (0, 0, 255), 2)  # Sol üst köşe
        cv2.line(frame, (offset, offset), (offset, offset + corner_length), (0, 0, 255), 2)
        cv2.line(frame, (width - offset, offset), (width - offset - corner_length, offset), (0, 0, 255), 2)  # Sağ üst köşe
        cv2.line(frame, (width - offset, offset), (width - offset, offset + corner_length), (0, 0, 255), 2)
        cv2.line(frame, (offset, height - offset), (offset + corner_length, height - offset), (0, 0, 255), 2)  # Sol alt köşe
        cv2.line(frame, (offset, height - offset), (offset, height - offset - corner_length), (0, 0, 255), 2)
        cv2.line(frame, (width - offset, height - offset), (width - offset - corner_length, height - offset), (0, 0, 255), 2)  # Sağ alt köşe
        cv2.line(frame, (width - offset, height - offset), (width - offset, height - offset - corner_length), (0, 0, 255), 2)
        
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        nişangah_boyutu = 20

  ##----------------- Center Target Draw ------------------##    
        cv2.line(frame, (center_x - nişangah_boyutu, center_y), 
                (center_x + nişangah_boyutu, center_y), (0, 0, 255), 2)
        cv2.line(frame, (center_x, center_y - nişangah_boyutu), 
                (center_x, center_y + nişangah_boyutu), (0, 0, 255), 2)
        
        distance = np.sqrt((cx - center_x) ** 2 + (cy - center_y) ** 2)
        threshold_distance = 25
        if distance < threshold_distance:
            text = "LOCK"
            c = (0, 255, 0)  # green color
        else:
            text = "SEARCH"
            c = (0, 0, 255)  # Red Color
        text_size1 = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text1_x = (frame.shape[1] - text_size1[0]) // 2
        text1_y = frame.shape[0] - 50  # Scroll to the bottom middle
        cv2.putText(frame, text, (text1_x, text1_y), cv2.FONT_HERSHEY_SIMPLEX, 1,c, 2)
        text_size2 = cv2.getTextSize(lock_status, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        text2_x = (frame.shape[1] - text_size2[0]) // 2
        text2_y = frame.shape[0] - 20
        cv2.putText(frame, lock_status, (text2_x, text2_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,lock_status_c, 2)
        cv2.imshow("Tracking", frame)        
        key = cv2.waitKey(1)

##----------------- Keyboard Commands ------------------##        
        if key == ord('q'): # quit
            break
        elif key == ord('e'): # Retarget
            roi_selector_active = True
            
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
