from __future__ import division, absolute_import
from . import _file, _redcap

import csv

METADATA_HEADER = ('field_name', 'form_name', 'section_header', 'field_type',
                   'field_label', 'choices', 'field_note',
                   'text_validation_type', 'text_validation_min',
                   'text_validation_max', 'identifier',
                   'branching_logic', 'required', 'custom_alignment',
                   'question_number', 'matrix_group_name')


def parse_filename(filename):
    return filename.split('.')[0].split('_')[0]


class Client(_file.Client):
    @property
    def file_handler(self):
        f = open(self.file_path, 'rU')
        # Skip the header
        next(f)
        return f

    @property
    def reader(self):
        return csv.DictReader(self.file_handler, fieldnames=METADATA_HEADER)

    def project(self):
        return {
            'name': self.file_name,
            'path': self.file_path,
        }

    def forms(self):
        "Collects all unique form names while maintaining the order."
        reader = self.reader
        forms = []
        unique = set()

        for row in reader:
            form_name = row['form_name']
            if form_name not in unique:
                forms.append({
                    'name': form_name
                })
                unique.add(form_name)
        return forms

    def sections(self, form_name):
        reader = self.reader
        sections = [{'name': 'default'}]
        unique = set()
        for row in reader:
            # Filter by form_name
            if row['form_name'] != form_name or not row['section_header']:
                continue
            name = row['section_header']
            if name not in unique:
                sections.append({'name': name})
                unique.add(name)
        return sections

    def fields(self, form_name, section_name):
        reader = self.reader
        fields = []
        current_section = 'default'

        for row in reader:
            # Filter by form_name
            if row['form_name'] != form_name:
                continue
            # Filter by section_name
            current_section = row['section_header'] or current_section
            if current_section != section_name:
                continue

            identifier = row['identifier'].lower() == 'y' and True or False
            required = row['required'].lower() == 'y' and True or False

            fields.append({
                'name': row['field_name'],
                'label': row['field_label'],
                'type': row['field_type'],
                'note': row['field_note'],
                'choices': row['choices'].replace(' | ', ' \\n '),
                'display_logic': row['branching_logic'],
                'validation_type': row['text_validation_type'],
                'validation_min': row['text_validation_min'],
                'validation_max': row['text_validation_max'],
                'identifier': identifier,
                'required': required,
                'header': row['section_header'],
                'alignment': row['custom_alignment'],
                'survey_num': row['question_number'],
                'matrix': row['matrix_group_name'],
            })
        return fields


# Exported classes for API
Origin = _redcap.Project
