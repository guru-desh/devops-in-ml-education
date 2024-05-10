import argparse

import pdfkit


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Convert HTML to PDF")

    # Add the arguments
    parser.add_argument("--html_file", type=str, help="The path to the input HTML file")
    parser.add_argument("--pdf_file", type=str, help="The path for the output PDF file")

    # Parse the command line arguments
    args = parser.parse_args()

    # Options for PDF generation
    options = {
        "page-size": "Letter",
        "orientation": "Landscape",
        "enable-local-file-access": "",
    }

    # Convert the HTML file to PDF with the specified options
    pdfkit.from_file(args.html_file, args.pdf_file, options=options)

    print(f"PDF generated successfully: {args.pdf_file}")


if __name__ == "__main__":
    main()
