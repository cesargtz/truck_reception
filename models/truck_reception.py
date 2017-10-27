# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions
import requests
import json

class TruckReception(models.Model):
    _inherit = ['truck', 'vehicle.reception', 'mail.thread']
    _name = 'truck.reception'

    name = fields.Char('Truck reception reference', required=True, select=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('reg_code'), help="Unique number of the Truck reception")

    state = fields.Selection([
        ('analysis', 'Analisis'),
        ('weight_input', 'Peso de Entrada'),
        ('weight_output', 'Pesos de Salida'),
        ('done', 'Hecho'),
    ], default='analysis')

    flete = fields.Selection([
        ('0', '0'),
        ('70', '70'),
        ('80', '80'),
        ('90', '90'),
        ('100', '100'),
    ], 'Flete', default='0')



    @api.one
    @api.depends('contract_id')
    def _compute_product_id(self):
        product_id = False
        for line in self.contract_id.order_line:
            product_id = line.product_id.id
            break
        self.product_id = product_id

    @api.one
    @api.depends('contract_id', 'clean_kilos')
    def _compute_delivered(self):
        self.delivered = sum(record.clean_kilos for record in self.contract_id.truck_reception_ids) / 1000

    @api.one
    def fun_unload(self):
        self.state = 'weight_output'

    @api.one
    def humidity_update(self):
    	url = 'http://nvryecora.ddns.net:1723'
    	response = requests.get(url)
    	json_data = json.loads(response.text)
    	self.humidity_rate = float(json_data['humedad'].strip())
    	self.density = float(json_data['densidad'])
    	self.temperature = float(json_data['temperatura'].strip())
        self.write({'state': 'analysis'}, 'r')

    @api.one
    def weight_input(self):
        url = 'http://nvryecora.ddns.net:8081'
        response = requests.get(url)
        json_data = json.loads(response.text)
        if json_data['id'] == self.name[-3:]:
            self.input_kilos = float(json_data['peso_entrada'])
            self.write({'state': 'weight_output'}, 'r')
        else:
            raise exceptions.ValidationError('Id de la bascula no coincide')
    @api.one
    def weight_output(self):
        url = 'http://nvryecora.ddns.net:8081'
        response = requests.get(url)
        json_data = json.loads(response.text)
        if json_data['id'] == self.name[-3:]:
            if float(json_data['peso_salida']) > 1:
                self.output_kilos = float(json_data['peso_salida'])
                self.write({'state': 'done'}, 'r')
            else:
                raise exceptions.ValidationError('Revisar el id de bascula')
        else:
            raise exceptions.ValidationError('Id de la bascula no coincide')

    @api.multi
    def write(self, vals, recursive=None):
        if not recursive:
            if self.state == 'analysis':
                self.write({'state': 'weight_input'}, 'r')
            elif self.state == 'weight_input':
                self.write({'state': 'weight_output'}, 'r')
            elif self.state == 'weight_output':
                self.write({'state': 'done'}, 'r')

        res = super(TruckReception, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        vals['state'] = 'weight_input'
        res = super(TruckReception, self).create(vals)
        return res

    @api.multi
    def copy(self):
        raise exceptions.ValidationError('No es posible duplicar.')
