import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("Models/best.pt")


# @markdown For that we use our function (short and simple) which allows us to display the bounding boxes with the label and the score :
def box_label(image, box, label="", color=(128, 128, 128), txt_color=(255, 255, 255)):
    lw = max(round(sum(image.shape) / 2 * 0.003), 2)
    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    cv2.rectangle(image, p1, p2, color, thickness=lw, lineType=cv2.LINE_AA)
    if label:
        tf = max(lw - 1, 1)  # font thickness
        w, h = cv2.getTextSize(label, 0, fontScale=lw / 3, thickness=tf)[
            0
        ]  # text width, height
        outside = p1[1] - h >= 3
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        cv2.rectangle(image, p1, p2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(
            image,
            label,
            (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
            0,
            lw / 3,
            txt_color,
            thickness=tf,
            lineType=cv2.LINE_AA,
        )


def plot_bboxes(image, boxes, labels=[], colors=[], score=True, conf=None):
    if labels == []:
        labels = {0: "Null", 1: "disease"}
    # Define colors
    if colors == []:
        colors = [(255, 0, 0)]

    # plot each boxes
    for box in boxes:
        # add score in label if score=True
        if score:
            label = (
                labels[int(box[-1]) + 1]
                + " "
                + str(round(100 * float(box[-2]), 1))
                + "%"
            )
        else:
            label = labels[int(box[-1]) + 1]
        # filter every box under conf threshold if conf threshold setted
        if conf:
            if box[-2] > conf:
                color = colors[int(box[-1])]
                box_label(image, box, '', color)
        else:
            color = colors[int(box[-1])]
            box_label(image, box, '', color)


def predict_disease_boxes(img_path, outdirPath):
    img = cv2.imread(img_path)
    results = model.predict(source=img, save=False, save_txt=False)
    plot_bboxes(img, results[0].boxes.data, score=False)

    cv2.imwrite(outdirPath, img)
    print(f"Img saved successfully at: {outdirPath}")


if __name__ == "__main__":
    img_path = "Tests_images/test.jpeg"
    outdirPath = "Tests_images/test___testOUT.jpeg"
    predict_disease_boxes(img_path, outdirPath)
