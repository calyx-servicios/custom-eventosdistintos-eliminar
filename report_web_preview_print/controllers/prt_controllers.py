from odoo import http
from odoo.http import request, Response
from odoo.addons.web.controllers.main import ReportController, Binary
import werkzeug
import json
from odoo.http import (
    content_disposition,
    dispatch_rpc,
    request,
    serialize_exception as _serialize_exception,
    Response,
)

######################
# Report Controllers #
######################


class PrtReportController(ReportController):
    @http.route(["/report/download"], type="http", auth="user")
    def report_download(self, data, token):
        res = super(PrtReportController, self).report_download(data, token)

        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        pattern = "/report/pdf/" if type == "qweb-pdf" else "/report/text/"
        reportname = url.split(pattern)[1].split("?")[0]

        if "/" in reportname:
            reportname = reportname.split("/")

        report = request.env["ir.actions.report"]._get_report_from_name(
            reportname
        )
        preview_print = report.preview

        if preview_print:
            res.headers["Content-Disposition"] = res.headers[
                "Content-Disposition"
            ].replace("attachment", "inline")
            return res
        else:
            return res
