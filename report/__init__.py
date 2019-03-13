import markdown_generator as mg
import re
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os
import yaml
import copy

class ReportGenerator:
    def __init__(self, **kwargs):
        self.report_file = kwargs.get('ReportFile')
        self.unique_id = kwargs.get('UniqueId')
        self.tokens = {}
        self.data = {}
        self.report_folder = '{}/{}'.format(
            kwargs.get('ReportFolder', 'report_output'),
            self.unique_id)
        if not os.path.exists(self.report_folder):
            os.makedirs(self.report_folder)
            os.makedirs('{}/images'.format(self.report_folder))
        with open('config.yaml', 'r') as f:
            self.config = yaml.load(f)
        self.pillars = {}

    def process_data(self):
        ids = ['arn', 'certificate_arn', 'id']
        data = copy.deepcopy(self.data)
        for res in data.keys():
            for k in data[res]:
                for id in ids:
                    if k == id:
                        self.data[res]['u_id'] = self.data[res][k]
                        break


    def is_in_pillar(self, res, key):
        r_type = res.split('.')[0]
        key_name = key.split('.')[-1]
        for p in self.config.keys():
            if p not in self.pillars.keys():
                self.pillars[p] = []
            resources = self.config[p]['resources']
            for r in resources:
                if isinstance(r, str):
                    if r == r_type:
                        return p, res, ''
                else:
                    for t in r.keys():
                        if key_name in r[t]:
                            return p, res, key_name
        return '', '', ''

    def import_data(self):
        with open(self.report_file, "r") as f:
            is_json = False
            is_outputs = False
            for line in f:
                if is_json:
                    if line.strip() == '}':
                        val = val + '}'
                        is_json = False
                        self.data[res][key] = val
                    else:
                        val = val + line
                    continue
                if line.startswith('data') or line.startswith('null'):
                    continue
                m = re.match("^([^[].*):$", line)
                if m:
                    if 'data' in line.split('.'):
                        continue
                    if line.startswith('Outputs:'):
                        is_outputs = True
                        continue
                    else:
                        is_outputs = False
                    res = m.groups()[0]
                    self.data[res] = {}
                    continue
                if is_outputs:
                    continue
                m = re.match('(.*)\s=\s({)$', line)
                if m:
                    key = m.groups()[0].strip()
                    val = m.groups()[1].strip()
                    is_json = True
                    continue

                m = re.match('(.*)\s=\s(.*)$', line)
                if m:
                    key = m.groups()[0].strip()
                    val = m.groups()[1].strip()
                    if key[-1:] in ['%', '#'] or val == "0" or len(val) == 0:
                        continue
                    self.data[res][key] = val
                    if key in ('id', 'name'):
                        self.add_token(res, val)
                    p, r, k = self.is_in_pillar(res, key)
                    if p:
                        if (r, k) not in self.pillars[p]:
                            print('Adding {}, {}'.format(r,k))
                            self.pillars[p].append((r, k))
                    continue
                m = re.match

    def generate(self):
        with open('{}/report.md'.format(self.report_folder), 'w') as f:
            writer = mg.Writer(f)
            for p in self.pillars.keys():
                writer.write_heading(p)
                unordered = mg.List()
                print(self.pillars['security'])
                for k in self.pillars[p]:
                    unordered.append('.'.join(k))
                writer.write(unordered)
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
                    val = self.data[res][key]
                    if val.strip().startswith('{'):
                        continue
                    table.append(display_key, val)
                writer.write(table)
                for key in self.data[res]:
                    val = self.data[res][key]
                    if not val.strip().startswith('{'):
                        continue
                    writer.write_heading(key, 2)
                    code = mg.Code()
                    code.append(val)
                    writer.write(code)
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
