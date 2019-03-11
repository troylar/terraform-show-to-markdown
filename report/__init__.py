import markdown_generator as mg
import re
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os


class ReportGenerator:
    def __init__(self, **kwargs):
        self.report_file = kwargs.get('ReportFile')
        self.tokens = {}
        self.data = {}
        self.report_folder = kwargs.get('ReportFolder', 'report_ouput')
        if not os.path.exists(self.report_folder):
            os.makedirs(self.report_folder)
            os.makedirs('{}/images'.format(self.report_folder))

    def import_data(self):
        with open(self.report_file, "r") as f:
            for line in f:
                if line.startswith('data') or line.startswith('null'):
                    continue
                m = re.match("^([^[].*):$", line)
                if m:
                    res = m.groups()[0]
                    self.data[res] = {}
                else:
                    m = re.match('(.*)\s=\s(.*)$', line)
                    if m:
                        key = m.groups()[0].strip()
                        val = m.groups()[1].strip()
                        if key[-1:] in ['%', '#'] or val == "0" or len(val) == 0:
                            continue
                        self.data[res][key] = val
                        if key in ('id', 'name'):
                            self.add_token(res, val)
                    else:
                        continue

    def generate(self):
        with open('{}/report.md'.format(self.report_folder), 'w') as f:
            writer = mg.Writer(f)
            i = 1
            for res in self.data:
                self.create_icon(str(i))
                writer.write_heading('![{}](./images/{}.png) {}'.format(
                    res, i, res))
                table = mg.Table()
                table.add_column('')
                table.add_column('')
                for key in self.data[res]:
                    if '.' in key:
                        keys = key.split('.')
                        root_keys = map(lambda x: '**{}**'.format(x), keys[:-1])
                        sub_key = '*{}*'.format(keys[-1])
                        display_key = '{}.{}'.format('.'.join(root_keys), sub_key)
                    else:
                        display_key = '**{}**'.format(key)
                    table.append(display_key, self.data[res][key])
                writer.write(table)
                i = i + 1

    def add_token(self, key, token):
        if key not in self.tokens.keys():
            self.tokens[key] = []
        self.tokens[key].append(token)

    def create_icon(self, id):
        font = ImageFont.truetype('OpenSans-Bold.ttf', 18)
        w, h = font.getsize(id)
        width, height = (w+20, 25)
        img = Image.new("RGBA", (width, height), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, width, height), fill="black")
        msg = id
        draw.text(((width-w)/2, ((height-h)/2)-2), msg, font=font)
        img.save('{}/images/{}.png'.format(self.report_folder, id), "PNG")
