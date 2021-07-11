from PIL import Image as pilIm
from PySide6.QtGui import QImage, qRgb


# Default sizes for images
ORIG_SCALED_SIZE = (250, 250)
CROPPED_SCALED_SIZE = (250, 250)

KNOWN_CONCENTRATION = -1
UNITS = ''


# A class that stores the entries of an image
class Image:

    UNSPECIFIED_IMAGE = "UNSPECIFIED"
    BLANK_VOLUME = "BLANK_VOLUME"
    STANDARD_VOLUME = "STANDARD_VOLUME"

    MOST_RECENT_MAX_X = -1
    MOST_RECENT_MIN_X = -1
    MOST_RECENT_MAX_Y = -1
    MOST_RECENT_MIN_Y = -1

    def __init__(self, file_name, volume=0):
        self.file_name = file_name

        self.min_x = Image.MOST_RECENT_MIN_X
        self.min_y = Image.MOST_RECENT_MIN_Y
        self.max_x = Image.MOST_RECENT_MAX_X
        self.max_y = Image.MOST_RECENT_MAX_Y

        self.volume = volume

        self.avg_value = (-1, -1, -1)

    def set_coordinates(self, min_x, min_y, max_x, max_y):
        if min_x >= max_x or min_y >= max_y:
            raise ValueError
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        Image.MOST_RECENT_MAX_Y = max_y
        Image.MOST_RECENT_MIN_Y = min_y
        Image.MOST_RECENT_MAX_X = max_x
        Image.MOST_RECENT_MIN_X = min_x
        self.compute_avg_color()

    def is_valid_coordinates(self):
        im = pilIm.open(self.file_name)
        return 0 <= self.min_x < self.max_x < im.size[1] and 0 <= self.min_y < self.max_y < im.size[0]

    def set_volume(self, volume):
        self.volume = volume

    def compute_avg_color(self):
        im = pilIm.open(self.file_name)
        cropped = im.crop((self.min_x, self.min_y, self.max_x, self.max_y))

        pixels = cropped.load()
        red = 0
        green = 0
        blue = 0
        for i in range(cropped.size[0]):
            for j in range(cropped.size[1]):
                red += pixels[i, j][0]
                green += pixels[i, j][1]
                blue += pixels[i, j][2]

        pix_count = cropped.size[0] * cropped.size[1]
        self.avg_value = (red / pix_count, green / pix_count, blue / pix_count)

    def get_original(self):
        return pilIm.open(self.file_name)

    def get_marked_scaled_original(self):
        if not self.is_valid_coordinates():
            return self.get_scaled_original()
        else:
            orig = self.get_original()
            scaled = self.get_scaled_original()
            pix = scaled.load()

            max_x = int(self.max_x / orig.size[1] * scaled.size[1])
            min_x = int(self.min_x / orig.size[1] * scaled.size[1])

            max_y = int(self.max_y / orig.size[0] * scaled.size[0])
            min_y = int(self.min_y / orig.size[0] * scaled.size[0])

            for i in range(scaled.size[1]):
                pix[min_x, i] = (0, 0, 0)
                pix[max_x, i] = (0, 0, 0)
            for j in range(scaled.size[0]):
                pix[j, min_y] = (0, 0, 0)
                pix[j, max_y] = (0, 0, 0)
            return scaled

    def get_cropped(self):
        if not self.is_valid_coordinates():
            return self.get_original()
        else:
            return self.get_original().crop((self.min_x, self.min_y, self.max_x, self.max_y))

    def get_scaled_original(self, scale=ORIG_SCALED_SIZE):
        im = self.get_original()
        scaling_factor = max(im.size[0], im.size[1])
        scaled_x = scale[0] * im.size[0] // scaling_factor
        scaled_y = scale[1] * im.size[1] // scaling_factor
        return im.resize((scaled_x, scaled_y))

    def get_scaled_cropped(self, scale=CROPPED_SCALED_SIZE):
        im = self.get_cropped()
        scaling_factor = max(im.size[0], im.size[1])
        scaled_x = scale[0] * im.size[0] // scaling_factor
        scaled_y = scale[1] * im.size[1] // scaling_factor
        return im.resize((scaled_x, scaled_y))


blank = Image.UNSPECIFIED_IMAGE
standard = Image.UNSPECIFIED_IMAGE
mid_images = []


def clear_images():
    global blank
    global standard
    global mid_images
    blank = Image.UNSPECIFIED_IMAGE
    standard = Image.UNSPECIFIED_IMAGE
    mid_images = []


def add_blank(image):
    global blank
    blank = image


def add_standard(image, concentration, units):
    global standard
    global KNOWN_CONCENTRATION
    global UNITS

    standard = image
    KNOWN_CONCENTRATION = concentration
    UNITS = units


def add_image(image):
    global mid_images
    mid_images.append(image)


def get_pix_map(image):
    pix = image.load()
    q_image = QImage(image.size[0], image.size[1], QImage.Format_RGB32)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            value = qRgb(pix[i, j][0], pix[i, j][1], pix[i, j][1])
            q_image.setPixel(i, j, value)
    return q_image


def get_state():
    if not mid_images:
        return "No images other than your blank and standard have been added."
    else:
        ret_str = ""
        for i in range(len(mid_images)):
            sub_str = 'Image ' + str(i + 1) + ':\t'
            sub_str += 'Concentration:\t' + str(mid_images[i].volume) + '\t'
            sub_str += 'File Name:\t' + mid_images[i].file_name
            ret_str += sub_str
            if i + 1 < len(mid_images):
                ret_str += '\n'
        return ret_str


# GENERATE CROPPED:
#         cropped = im.crop((self.min_x, self.min_y, self.max_x, self.max_y))
# GENERATE SCALED:
#         scaling_factor = max(im.size[0], im.size[1])
#         scaled_orig_x = ORIG_SCALED_SIZE[0] * im.size[0] // scaling_factor
#         scaled_orig_y = ORIG_SCALED_SIZE[1] * im.size[1] // scaling_factor
#         scaled_orig = im.resize((scaled_orig_x, scaled_orig_y))
# GENERATE SCALED CROPPED:
# Like, both at once dummy
