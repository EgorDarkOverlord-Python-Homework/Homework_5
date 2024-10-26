import sys
import argparse

from utils.reader import image_reader as imread, wav_reader as wavread
from utils.reader import csv_reader, bin_reader, txt_reader, json_reader
from utils.processor import histogram, wav_processing
from utils.writer import csv_writer, bin_writer, txt_writer, image_writer, json_writer, wav_writer

from utils.image_toner import stat_correction, equalization, gamma_correction


def print_args_1():
    print(type(sys.argv))
    if (len(sys.argv) > 1):
        for param in sys.argv[1:]:
            print(param, type(param))
    return sys.argv[1:]

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-img','--img_path', default ='', help='Path to image')
    parser.add_argument('-p','--path', default ='', help='Input file path')
    parser.add_argument('-cf', '--conversion_function', default ='', help='Conversion function. hist is histogram, img is image conversion')
    parser.add_argument('-icf', '--image_conversion_function', default ='', help='Image conversion function. eq is histogram equalization, gamma is gamma correction')
    parser.add_argument('-a', '--alpha', default = '2.2', help= 'Alpha for gamma correction')
    parser.add_argument('-b', '--beta', default = '50', help= 'Beta for gamma correction')
    parser.add_argument('-o', '--output', help='Save file path')
    parser.add_argument('-wav','--wav_path', default ='', help='Path to wav file')

    return parser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args(sys.argv[1:])

    if (args.wav_path != ''):
        wav_data = wavread.read_data(args.wav_path)
        data = wav_data[-1]
        d_type = wav_data[-2]
        hist = wav_processing.wav_histogram(data, d_type)
        wav_writer.write_data(args.output, hist, d_type)
        exit(0)

    image = None
    image = imread.read_data(args.img_path)
    res_image = None

    match args.conversion_function:
        case 'hist':
            hist_template = None
            file_type = args.path.split('.')[-1]
            match file_type:
                case 'img':
                    img2 = imread.read_data(args.path)
                    hist_template = histogram.image_processing(img2)
                case 'csv':
                    hist_template = csv_reader.read_data(args.path)
                case 'bin':
                    hist_template = bin_reader.read_data(args.path)
                case 'txt':
                    hist_template = txt_reader.read_data(args.path)
                case 'json':
                    hist_template = json_reader.read_data(args.path)
                case _:
                    pass
            res_image = stat_correction.processing(hist_template, image)
        case 'img':
            match args.image_conversion_function:
                case 'eq':
                    res_image = equalization.histogram_equalization(image)
                case 'gamma':
                    alpha = float(args.alpha)
                    beta = float(args.beta)
                    res_image = gamma_correction.correction(image, alpha, beta)
            pass
 
    image_writer.write_data(args.output, res_image)

# Подсчет гистограммы
# py test_readers.py --img .\input_data\sar_1_gray.jpg -cf hist -p .\input_data\txt_test.txt -o .\output_data\res.jpg

# Эквивализация гистограммы
# py test_readers.py --img .\input_data\sar_1_gray.jpg -cf img -icf eq -o .\output_data\res.jpg

# Гамма коррекция
# py test_readers.py --img .\input_data\sar_1_gray.jpg -cf img -icf gamma -o .\output_data\res.jpg
# py test_readers.py --img .\input_data\sar_1_gray.jpg -cf img -icf gamma -a 2.2 -b 50 -o .\output_data\res.jpg

# Звук
# py test_readers.py -wav .\input_data\sample.wav -o .\output_data\result.wav