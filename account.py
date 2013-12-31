from openerp.osv import fields,osv
from openerp import tools
 
class account_invoice(osv.osv):
    _name = "account.tax.vat_report"
    _description = "VAT Report"
    _auto = False
    _columns = {
	'journal_id': fields.many2one('account.journal','Journal Name'),
	'invoice_number': fields.char('Invoice Number',size=32,readonly=True),
	'account_id': fields.many2one('account.account','Account Name'),
	'date_invoice': fields.date('Date',readonly=True),
        'month':fields.selection([('01', 'January'), ('02', 'February'), \
                                  ('03', 'March'), ('04', 'April'),\
                                  ('05', 'May'), ('06', 'June'), \
                                  ('07', 'July'), ('08', 'August'),\
                                  ('09', 'September'), ('10', 'October'),\
                                  ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
	'invoice_type': fields.char('Invoice Type',size=32,readonly=True),
	'partner_id': fields.many2one('res.partner','Partner Name'),
	'vat': fields.char('Resp Name',size=32,readonly=True),
	'base_amount': fields.float('Base Amount',readonly=True,group_operator="sum",digits=(16,2)),
	'tax_amount': fields.float('Tax Amount',readonly=True,group_operator="sum",digits=(16,2)),
	'amount': fields.float('Amount',readonly=True,group_operator="sum",digits=(16,2)), 
	}
 
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'account_tax_vat_report')
	cr.execute("""
		create or replace view account_tax_vat_report as (
		select a.id as id,d.id as journal_id,c.number as invoice_number,b.id as account_id,
			c.date_invoice as date_invoice,
                        to_char(c.date_invoice, 'YYYY') as year,
                        to_char(c.date_invoice, 'MM') as month,
                        to_char(c.date_invoice, 'YYYY-MM-DD') as day,
			c.type as invoice_type,
			e.id as partner_id,e.vat as vat,
			a.base_amount as base_amount, a.tax_amount as tax_amount, a.amount as amount
			from account_invoice_tax a
				inner join account_account b on a.account_id = b.id
				inner join account_invoice c on a.invoice_id = c.id
				inner join account_journal d on c.journal_id = d.id
				inner join res_partner e on c.partner_id = e.id
				)
	""")	
 
account_invoice()

"""
class afip_document_type(osv.osv):
    _name = "afip.document.type"
    _inherit = "afip.document.type"

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
                    ids = [ids]
        reads = self.read(cr, uid, ids, ['name'], context=context)
        res = []
        for record in reads:
            name = record['name']
            res.append((record['id'], name))
        return res

afip_document_type()
"""
