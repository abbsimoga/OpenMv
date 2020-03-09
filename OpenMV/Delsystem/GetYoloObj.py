import sensor, time, lcd
import KPU as kpu

lcd.init()
# sensor.skip_frames(time = 500)

classes = ["Legogubbe"]
task = kpu.load(0x600000)
anchor = (0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828)
a = kpu.init_yolo2(task, 0.75, 0.3, 5, anchor)

YOLO_ROI = [48, 8, 224, 224]

def setCamera(window_):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)

    sensor.set_contrast(-2)
    sensor.set_gainceiling(16)
    sensor.set_vflip(False)
    sensor.set_hmirror(False)

    sensor.set_windowing(window_)

    sensor.run(1)

def getYoloObjects(img_):
    # setCamera((224,224))
    # yoloObj = kpu.run_yolo2(task, img_)
    # setCamera((320,240))
    # yoloObj = kpu.run_yolo2(task, img_.copy(roi=YOLO_ROI, copy_to_fb=False))
    yoloObj = kpu.run_yolo2(task, img_.copy(roi=YOLO_ROI, copy_to_fb=False))#.to_rgb565(copy=False))
    if yoloObj:
        print(yoloObj)
    return yoloObj if yoloObj else []

def outlineObjects(img_, objects_, color_, border_, fill_):
    for object in objects_:
        img_.draw_rectangle(object.rect(), color_, border_, fill_)

# setCamera((224,224))
setCamera((320,240))

while(True):
    img = sensor.snapshot().copy(roi=YOLO_ROI, copy_to_fb=True).to_rgb565(copy=True)#.scale(x_scale = 0.5, y_scale=0.5, copy_to_fb=False)

    # legoGubbar = getYoloObjects(img)

    legoGubbar = kpu.run_yolo2(task, img)

    if not legoGubbar: legoGubbar=[]

    outlineObjects(img, legoGubbar, (0, 255, 0), 2, False)

    lcd.display(img)