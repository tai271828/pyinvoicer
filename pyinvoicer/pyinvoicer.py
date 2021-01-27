import argparse

import pyinvoicer.invoice
import pyinvoicer.renderer


def main():
    parser = argparse.ArgumentParser()

    default_format = "pdf"
    default_output = "./invoice.format"

    parser.add_argument("content", help="invoice content file (see examples)", type=str)
    parser.add_argument(
        "--output",
        help=f"output file name and path (default: {default_output})",
        type=str,
    )
    parser.add_argument(
        "--format",
        help=f"output file format (default: {default_format})",
        type=str,
        default=default_format,
        choices=["html", "pdf"],
    )

    args = parser.parse_args()

    invoice_content = pyinvoicer.invoice.SimpleInvoice(args.content)

    if args.format == "pdf":
        invoice_rendered = pyinvoicer.renderer.PDFRenderer(invoice_content)
    else:
        invoice_rendered = pyinvoicer.renderer.HTMLRenderer(invoice_content)

    if args.output:
        invoice_rendered.dump(args.output)
    else:
        invoice_rendered.dump()


if __name__ == "__main__":
    main()
