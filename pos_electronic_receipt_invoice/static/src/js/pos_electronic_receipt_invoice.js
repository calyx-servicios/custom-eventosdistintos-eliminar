odoo.define('pos_electronic_receipt_invoice', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            _super_Order.initialize.apply(this, arguments);
            if (this.pos.config.pos_auto_invoice) {
                this.to_invoice = true;
            }
        },
        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.to_invoice) {
                this.to_invoice = json.to_invoice;
            }
        }
    });
    screens.ReceiptScreenWidget.include({
        print_xml: function () {
            var self = this;
            if (this.pos.config.receipt_invoice_number) {
                self.receipt_data = this.get_receipt_render_env();
                var order = this.pos.get_order();
                return rpc.query({
                    model: 'pos.order',
                    method: 'search_read',
                    domain: [['pos_reference', '=', order['name']]],
                    fields: ['invoice_id'],
                }).then(function (orders) {
                    if (orders.length > 0) {
                        if (orders[0]['invoice_id']) {
							var invoice_id = orders[0]['invoice_id'][0];
                            var invoice_number = orders[0]['invoice_id'][1];
                            self.receipt_data['order']['invoice_number'] = invoice_number;
                            rpc.query({
							     model: 'account.invoice',
							     method: 'search_read',
							     args: [[['id', '=', invoice_id]], ['afip_auth_code',
							                                        'afip_qr_code',
							                                        ]],
							}).then(function (invoices) {
							    self.receipt_data['order']['afip_auth_code'] = invoices[0]['afip_auth_code'];
							    self.receipt_data['order']['afip_qr_code'] = invoices[0]['afip_qr_code'];
							});
                        }
                    }
                    var receipt = qweb.render('XmlReceipt', self.receipt_data);
                    self.pos.proxy.print_receipt(receipt);
                });
            } else {
                this._super();
            }
        },
        render_receipt: function () {
            this._super();
            var self = this;
            var order = this.pos.get_order();
            if (!this.pos.config.iface_print_via_proxy && this.pos.config.receipt_invoice_number && order.is_to_invoice()) {
                var invoiced = new $.Deferred();
                rpc.query({
                    model: 'pos.order',
                    method: 'search_read',
                    domain: [['pos_reference', '=', order['name']]],
                    fields: ['invoice_id']
                }).then(function (orders) {
                    if (orders.length > 0 && orders[0]['invoice_id'] && orders[0]['invoice_id'][1]) {       
                        var invoice_id = orders[0]['invoice_id'][0];
                        var invoice_number = orders[0]['invoice_id'][1];
                        self.pos.get_order()['invoice_number'] = invoice_number;
                        rpc.query({
						     model: 'account.invoice',
						     method: 'search_read',
						     args: [[['id', '=', invoice_id]], ['afip_auth_code',
						                                        'afip_qr_code',
						                                        ]],
						}).then(function (invoices) {
						    self.pos.get_order()['afip_auth_code'] = invoices[0]['afip_auth_code'];
					        self.pos.get_order()['afip_qr_code'] = invoices[0]['afip_qr_code'];
							self.$('.pos-receipt-container').html(qweb.render('PosTicket', self.get_receipt_render_env()));
						});
                    }
                    invoiced.resolve();
                }).fail(function (type, error) {
                    invoiced.reject(error);
                });
                return invoiced;
            } else {
                this._super();
            }
        }
    })
});
