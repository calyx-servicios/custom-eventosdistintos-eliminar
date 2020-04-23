odoo.define('report_web_preview_print.ReportPreview', function (require) {
  "use strict";

  var Session = require('web.Session');
  var core = require('web.core');
  var rpc = require('web.rpc')
  var ajax = require('web.ajax');


  // Session
  Session.include({

    get_file: function (options) {
      var token = new Date().getTime();
      options.session = this;
      var params = _.extend({}, options.data || {}, { token: token });
      var url = options.session.url(options.url, params);

      if (url.indexOf('report/download') == -1) {
        return this._super.apply(this, arguments);
      }

      var preview = "";
      var pattern = options.data["data"];
      pattern = pattern.replace("[", "")
      pattern = pattern.replace("]", "")
      pattern = pattern.split(",")
      pattern = pattern[0]
      var reportname = pattern.split("/report/pdf/")[1].split("?")[0]
      reportname = reportname.replace('"', '')
      if (reportname.indexOf('/') != -1) {
        reportname = reportname.split("/")
      }

      rpc.query({
        model: "ir.actions.report",
        method: "get_report_from_name",
        args: [reportname],
      }).then(function (res) {
        preview = res[0]["preview"];
        if (preview == false) {
          return ajax.get_file(options);
        } else {
          if (options.complete) { options.complete(); }

          var w = window.open(url);
          w.print();
          if (!w || w.closed || typeof w.closed === 'undefined') {
            // popup was blocked
            return false;
          }
        }
      });
      return true;

    },
  });

});
