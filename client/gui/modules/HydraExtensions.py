import re

def HydraExtensionModule(content):
    ### auto color
    content = re.sub(r"\.autocolor\(([0-9|.]+), ([0-9|.]+), ([0-9|.]+), ([0-9|.]+)\)",
                     r""".color(()=>\4+a.fft[0,2]*\1,
                     ()=>\4+a.fft[3,5]*\2,
                     ()=>\4+a.fft[6,7]*\3)""",
                     content)

    ### quick audio
    # single bin: a0 --> a.fft[0]
    content = re.sub(r"\ba([0-7])(?!,)\b", r"a.fft[\1]", content)
    # multi bin: a0,7 --> a.fft[0,7]
    content = re.sub(r"\ba([0-7]),([0-7])\b", r"a.fft[\1, \2]", content)

    ### square scale
    # no scale param
    content = re.sub(r"\.sscale\(\)",
                     r".scale(width/height, height/width)",
                     content)
    # scale param
    content = re.sub(r"\.sscale\((-?[.|0-9]+)\)",
                     r".scale(width/height, height/width).scale(\1)",
                     content)

    # quick import image
    content = re.sub(r"\.loadimg\(\"(.*)\"\)",
                     r""".initImage("file:/Users/default/Desktop/ /Hydra/imports/\1")""",
                     content)

    return content
