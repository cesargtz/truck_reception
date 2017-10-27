# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    truck_reception_ids = fields.One2many('truck.reception', 'contract_id', 'No de contrato')

    def truck_reception(self):     
        self.ensure_one()
        try:
            form_id = self.env['ir.model.data'].get_object_reference('truck_reception', 'truck_reception_form_view')[1]
        except ValueError:
            form_id = False

        ctx = dict()
        ctx.update({
            'default_contract_id': self.ids[0],
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'truck.reception',
            'views': [(form_id, 'form')],
            'view_id': form_id,
            #'target': 'new',
            'context': ctx,
        }
