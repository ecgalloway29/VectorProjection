import ImageManager as IM
from math import sqrt
from matplotlib import pyplot as plt
from datetime import datetime

def subtract(c1, c2):
    return c1[0] - c2[0], c1[1] - c2[1], c1[2] - c2[2]


def magnitude(c):
    return sqrt(c[0] * c[0] + c[1] * c[1] + c[2] * c[2])


def dot(c1, c2):
    return c1[0] * c2[0] + c1[1] * c2[1] + c1[2] * c2[2]


def generate_graph():

    VPM = []
    volumes = []

    B_vec = subtract(IM.standard.avg_value, IM.blank.avg_value)

    print(B_vec)

    B_mag = magnitude(B_vec)

    concentration = IM.KNOWN_CONCENTRATION

    plt.xlabel("Volume (Drops)")
    plt.ylabel("Concentration (Drops)")

    for image in IM.mid_images:
        A_vec = subtract(image.avg_value, IM.blank.avg_value)
        A_mag = magnitude(A_vec)

        VPM.append(A_mag / B_mag * concentration)
        volumes.append(image.volume)

    plt.plot(volumes, VPM)
    plt.show()

    return VPM, volumes

def generate_csv():
    VPM = []
    volumes = []
    im_names = []

    B_vec = subtract(IM.standard.avg_value, IM.blank.avg_value)


    B_mag = magnitude(B_vec)

    concentration = IM.KNOWN_CONCENTRATION


    for image in IM.mid_images:
        A_vec = subtract(image.avg_value, IM.blank.avg_value)
        A_mag = magnitude(A_vec)

        VPM.append(A_mag / B_mag * concentration)
        volumes.append(image.volume)
        im_names.append(image.file_name)

    now = datetime.now()

    output_file = open(now.strftime("%m%d%y%H%M%S.csv"), 'w')

    line = "{image:35s},{volume:.3f},{VPM:.5f}\n"

    output_file.write("Image,Volume,Concentration\n")

    for v in range(len(VPM)):
        output_file.write(line.format(image=im_names[v], volume=volumes[v], VPM=VPM[v]))

    output_file.close()

    return VPM, volumes
