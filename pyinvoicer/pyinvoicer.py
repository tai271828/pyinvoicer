import argparse
import invoice
import renderer


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("content", help="invoice content file", type=str)
    parser.add_argument("--output", help="output file name without extension suffix", type=str, default="invoice")
    parser.add_argument("--format", help="output file format", type=str, default="html", choices=["html", "pdf"])

    args = parser.parse_args()

    invoice_content = invoice.SimpleInvoice(args.content)

    if args.format == "pdf":
        invoice_rendered = renderer.PDFRenderer(invoice_content)
    else:
        invoice_rendered = renderer.HTMLRenderer(invoice_content)

    invoice_rendered.dump()


if __name__ == "__main__":
    main()
