# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DateReportWizard(models.TransientModel):
    _name = "covid_19.date.report.wizard"
    _description = "Report between date and by country"
    
    
    start_date=fields.Date('Start Date',required=True)
    end_date=fields.Date('End Date',required=True)
    country_ids = fields.Many2many(
                                    "res.country", 
                                    string="Countries", 
                                    help="Countries you want to generate the report"
                                    )

    def print_report(self):
        Covid19=self.env['covid.covid_19']
        domain= [
                ('date','>=',self.start_date),
                ('date','<=',self.end_date)
                ]
        if self.country_ids:
            domain.append(('country_id','in',self.country_ids.ids))
        covidField=[
                'source',
                'date',
                'country_id',
                'infected',
                'recovered',
                'deseaced',
                ]
        CovidRecords=Covid19.search_read(domain,covidField)
        data={
            #~ 'doc_ids': self.ids,
            #~ 'doc_model': self.env['covid_19.date.report.wizard'],
            #~ 'docs': self,
            'CovidRecords':CovidRecords,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'country_ids': self.country_ids,
                }
        return self.env.ref('covid-19.report_DateReportExternalayout').report_action(self, data=data)
